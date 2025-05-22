# Schema definitions
import strawberry


# @strawberry.type
# class User:
#     id: str
#     name: str
#     email: str


# Định nghĩa User type với @key directive
@strawberry.federation.type(keys=["id"])
class User:
    id: strawberry.ID
    name: str
    email: str

    # Resolver để tìm User theo ID (cần thiết cho Federation)
    @classmethod
    def resolve_reference(cls, id: strawberry.ID):
        # Trong thực tế, bạn sẽ truy vấn database ở đây
        return User(id=id, name=f"User {id}", email=f"user{id}@example.com")