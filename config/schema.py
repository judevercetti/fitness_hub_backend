from ariadne import ObjectType, QueryType, gql, make_executable_schema

type_defs = gql("""
    type Query {
        hello: String!
        user: User
    }           
                
    type User {
        username: String!
    }
""")

query = QueryType()

@query.field("user")
def resolve_user(_, info):
    return {"first_name": "John", "last_name": "Lennon"}


@query.field("hello")
def resolve_hello(_, info):
    request = info.context["request"]
    user_agent = request.headers.get("user-agent", "guest")
    return "Hello, %s!" % user_agent


user = ObjectType("User")

@user.field("username")
def resolve_username(obj, *_):
    return f"{obj['first_name']} {obj['last_name']}"


schema = make_executable_schema(type_defs, [query, user])