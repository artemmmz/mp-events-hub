from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
    inject,
)
from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED

from delivery.api.v1.auth.schemas import (
    RegisterInSchema,
    RegisterOutSchema,
)
from modules.auth.application.use_cases.register import (
    RegisterUseCase,
    RegisterCommand,
)
from seedwork.domain.value_objects.jwt import JwtTokenValue


router = APIRouter(
    prefix="/auth",
    route_class=DishkaRoute,
)


@router.post(
    path="/register",
    response_model=RegisterOutSchema,
    status_code=HTTP_201_CREATED,
    summary="",
)
@inject
async def register(
    schema: RegisterInSchema,
    response: Response,
    use_case: FromDishka[RegisterUseCase],
) -> RegisterOutSchema:
    command = RegisterCommand(
        name=schema.name,
        second_name=schema.second_name,
        group_number=schema.group_number,
        email=str(schema.email),
        password=schema.password,
    )

    token: JwtTokenValue = await use_case.act(command=command)

    response.set_cookie(
        key="access_token",
        value=token.value,
        httponly=True,
        secure=True,
        samesite="lax",
        expires="Wed, 31 Dec 2137 23:59:59 GMT",
    )

    return RegisterOutSchema(token="token.value")
