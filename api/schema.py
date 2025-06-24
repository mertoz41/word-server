import graphene
from .mutations import CreateUser, CreateWord
import graphql_jwt
from .queries import UserQuery, WordQuery, LanguageQuery
class Query(UserQuery, LanguageQuery, WordQuery, graphene.ObjectType):
    pass
 
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_word = CreateWord.Field()
    # JWT Auth mutations
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)
