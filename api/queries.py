import graphene
from .types import UserType, LanguageType, WordType
from .models import User, Language, Word 

class UserQuery(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.Int(required=True))

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()
    
    def resolve_user_by_id(self, info, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
        
    
class LanguageQuery(graphene.ObjectType):
    all_languages = graphene.List(LanguageType)

    def resolve_all_languages(self, info, **kwargs):
        return Language.objects.all()
    
class WordQuery(graphene.ObjectType):
    all_words = graphene.List(WordType, language_code=graphene.String(required=False))
    word_by_text = graphene.Field(WordType, text=graphene.String(required=True))

    def resolve_all_words(self, info, language_code, **kwargs):
        qs = Word.objects.all()

        if language_code is not None:
            qs = qs.filter(language__code=language_code)
            return qs
    def resolve_word_by_text(self, info, text):
        try:
            return Word.objects.get(text=text)
        except Word.DoesNotExist:
            return None
        
