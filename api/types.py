from graphene_django.types import DjangoObjectType
from .models import User, Word, Language


class UserType(DjangoObjectType):
    class Meta:
        model = User


class LanguageType(DjangoObjectType):
    class Meta:
        model = Language

class WordType(DjangoObjectType):
    class Meta:
        model = Word
