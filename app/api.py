import asyncio
from typing import AsyncGenerator, List

import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry.subscriptions import GRAPHQL_TRANSPORT_WS_PROTOCOL, GRAPHQL_WS_PROTOCOL
from strawberry.types import Info


@strawberry.type
class Query:

    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


@strawberry.type
class Message:
    id: strawberry.ID
    message: str


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 100) -> AsyncGenerator[int, None]:
        for i in range(target):
            yield i
            await asyncio.sleep(5)

    # @strawberry.subscription
    # async def connect_to_chat(self, info: Info, guid: strawberry.ID) -> AsyncGenerator[List[Message], None]:
    #     connection_params: dict = info.context.get("connection_params")
    #     token: str = connection_params.get(
    #         "authToken"
    #     )  # equal to "Bearer I_AM_A_VALID_AUTH_TOKEN"
    #     if not authenticate_token(token):
    #         raise Exception("Forbidden!")
    #
    #     while True:
    #         check_for_new_msgs = DB.check_for_new_msg(guid)
    #
    #         if check_for_new_msgs:
    #             yield check_for_new_msgs
    #
    #         await asyncio.sleep(5)


schema = strawberry.Schema(Query, subscription=Subscription)

graphql_router = GraphQLRouter(
    schema,
    subscription_protocols=[
        GRAPHQL_TRANSPORT_WS_PROTOCOL,
        GRAPHQL_WS_PROTOCOL,
    ],
)

app = FastAPI()
app.include_router(graphql_router, prefix="/graphql")
