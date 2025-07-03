import os
from openai import OpenAI
import json
import graphene
from django.contrib.auth.hashers import make_password
from .models import User, Word, Language
from .tasks import save_word_task
from .types import UserType, WordType
from graphql_jwt.utils import jwt_encode, jwt_payload
from .utils.openai_utils import build_openai_prompt
from graphene.types.generic import GenericScalar

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 

class CreateWord(graphene.Mutation):
    word = graphene.Field(WordType)
    definition = graphene.String()
    sentences = graphene.List(graphene.String)
    translations = GenericScalar()
    awarded_points = graphene.Int()
    class Arguments:
        text = graphene.String(required=True)
        language_code = graphene.String(required=True)
        user_id = graphene.ID(required=True)
        translations = graphene.List(graphene.String, required=False)

    def mutate(self, info, text, language_code, user_id, translations=None):
        # Call OpenAI API synchronously
        translations = translations or []
        try:
            language = Language.objects.get(code=language_code)
        except Language.DoesNotExist:
            raise Exception("Language not found.")
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Exception("User not found.")
        existing_word = Word.objects.filter(
            text__iexact=text,
            language=language,
            user=user
        ).first()

        if existing_word:
            # Word exists — return it immediately without calling OpenAI
            return CreateWord(word=existing_word)

        # Word does NOT exist — call OpenAI to generate data
        prompt = build_openai_prompt(text, language_code, translations)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
        )
        openai_text = response.choices[0].message.content.strip()
    # Parse JSON response safely
        try:
            openai_data = json.loads(openai_text)
        except json.JSONDecodeError:
            raise Exception("Failed to parse OpenAI response JSON.")

        definition = openai_data.get("definition", '')
        sentences = openai_data.get("sentences", [])
        translations_data = openai_data.get("translations", {})
        user.points += 5
        user.save()
        awarded_points = 5
        save_word_task.delay(text, definition, language_code, user_id, sentences, translations_data)
        return CreateWord(word=None, definition=definition, sentences=sentences, translations=translations_data, awarded_points=awarded_points)
   
    



class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, email, password):
        if User.objects.filter(username=username).exists():
            raise Exception('Username already taken.')
        if User.objects.filter(email=email).exists():
            raise Exception("Email already registered.")
        user = User(
            username=username,
            email=email,
            password=make_password(password)
        )
        user.save()
        payload = jwt_payload(user)
        token = jwt_encode(payload)
        return CreateUser(user=user, token=token)
    


