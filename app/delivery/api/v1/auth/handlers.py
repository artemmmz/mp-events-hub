from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
    inject,
)
from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from fastapi.responses import Response

from delivery.api.v1.auth.schemas import (
    RegisterInSchema,
    RegisterOutSchema,
    LoginInSchema,
    LoginOutSchema,
)
from modules.auth.application.use_cases.register import (
    RegisterUseCase,
    RegisterCommand,
)
from modules.auth.application.use_cases.login import (
    LoginUseCase,
    LoginCommand,
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

    schema = RegisterOutSchema(token=token.value)

    response.set_cookie(
        key="access_token",
        value=token.value,
        httponly=True,
        samesite="lax",
        expires="Wed, 31 Dec 2137 23:59:59 GMT",
    )

    return schema


@router.post(
    path="/login",
    response_model=LoginOutSchema,
    status_code=HTTP_200_OK,
    summary="",
)
@inject
async def login(
    schema: LoginInSchema,
    response: Response,
    use_case: FromDishka[LoginUseCase],
) -> LoginOutSchema:
    command = LoginCommand(
        email=schema.email,
        password=schema.password,
    )

    token: JwtTokenValue = await use_case.act(command=command)

    response.set_cookie(
        key="access_token",
        value=token.value,
        httponly=True,
        samesite="lax",
        expires="Wed, 31 Dec 2137 23:59:59 GMT",
    )

    schema = LoginOutSchema(token=token.value)

    return schema