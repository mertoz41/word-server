import graphene
from graphene_django.types import DjangoObjectType
from .models import User, Language, Word
from .mutations import CreateUser, CreateWord
import graphql_jwt
from .types import UserType, WordType, LanguageType

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_languages = graphene.List(LanguageType)    
    all_words = graphene.List(
        WordType, 
        language_code=graphene.String(required=False),
    )

    user_by_id = graphene.Field(UserType, id=graphene.Int(required=True))
    language_by_id = graphene.Field(LanguageType, id=graphene.Int(required=True))
    word_by_id = graphene.Field(WordType, id=graphene.Int(required=True))

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()
    
    def resolve_all_languages(self, info, **kwargs):
        return Language.objects.all()
    
    def resolve_all_words(self, info, language_code=None, **kwargs):
        qs = Word.objects.all()

        if language_code is not None:
            qs = qs.filter(language__code=language_code)
        return qs
    
    def resolve_user_by_id(self, info, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
        
    def resolve_language_by_id(self, info, id):
        try:
            return Language.objects.get(pk=id)
        except Language.DoesNotExist:
            return None
        
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_word = CreateWord.Field()
    # JWT Auth mutations
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)
