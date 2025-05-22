import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry.federation.schema_directives import Key


# Định nghĩa User type như một entity từ service khác
@strawberry.federation.type(keys=["id"])
class User:
    id: strawberry.ID

    # Chúng ta sẽ mở rộng User type với posts field
    @strawberry.field
    def posts(self) -> list["Post"]:
        return [post for post in POSTS if post.author_id == self.id]


# Định nghĩa Post type
@strawberry.federation.type(keys=["id"])
class Post:
    id: strawberry.ID
    title: str
    content: str
    author_id: strawberry.ID

    @classmethod
    def resolve_reference(cls, id: strawberry.ID):
        # Trong thực tế, bạn sẽ truy vấn database ở đây
        for post in POSTS:
            if post.id == id:
                return post
        return None


# Mock database
POSTS = [
    Post(id="1", title="Federation with Strawberry", content="This is awesome!", author_id="1"),
    Post(id="2", title="GraphQL is cool", content="Indeed it is!", author_id="1"),
    Post(id="3", title="Hello World", content="My first post", author_id="2"),
]


# Định nghĩa Query type
@strawberry.federation.type
class Query:
    @strawberry.field
    def post(self, id: strawberry.ID) -> Post:
        for post in POSTS:
            if post.id == id:
                return post
        return None

    @strawberry.field
    def posts(self) -> list[Post]:
        return POSTS


# Tạo schema
schema = strawberry.federation.Schema(query=Query, types=[User, Post])

# Tạo FastAPI app
app = FastAPI()

# Tạo GraphQL router
graphql_app = GraphQLRouter(schema)

# Thêm GraphQL endpoint vào FastAPI
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001)