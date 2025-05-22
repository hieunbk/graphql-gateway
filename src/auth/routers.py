import strawberry
from strawberry.fastapi import GraphQLRouter

from src.auth.schemas import User


@strawberry.federation.type
class Query:
    @strawberry.field
    async def user(self, id: str) -> User:
        # Ở đây bạn sẽ gọi đến service của user để lấy dữ liệu
        # Đây chỉ là mock data
        return User(id=id, name="Nguyen Van A", email="a@example.com")

    @strawberry.field
    async def users(self) -> list[User]:
        # Ở đây bạn sẽ gọi đến service của user để lấy danh sách
        return [
            User(id="1", name="Nguyen Van A", email="a@example.com"),
            User(id="2", name="Tran Thi B", email="b@example.com")
        ]

# Tạo schema
schema = strawberry.federation.Schema(query=Query)

# Tạo GraphQL router
graphql_app = GraphQLRouter(schema)