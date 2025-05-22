# app/main.py
from fastapi import FastAPI
from src.auth.routers import graphql_app

# Khởi tạo FastAPI app
app = FastAPI(title="GraphQL Gateway")

# Thêm GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "GraphQL Gateway is running. Access /graphql for the GraphiQL interface"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
