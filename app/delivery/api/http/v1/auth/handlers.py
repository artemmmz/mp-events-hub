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

from bootstrap.settings import Settings
from delivery.api.http.v1.auth.schemas import (
    RegisterInSchema,
    RegisterOutSchema,
    LoginInSchema,
    LoginOutSchema, ConfirmInSchema, ConfirmOutSchema,
)
from modules.auth.application.use_cases.confirm import (
    ConfirmRegisterUseCase,
    ConfirmRegisterCommand,
)
from modules.auth.application.use_cases.register import (
    RegisterUseCase,
    RegisterCommand,
)
from modules.auth.application.use_cases.login import (
    LoginUseCase,
    LoginCommand,
)
from modules.auth.domain.aggregate.user import User
from seedwork.domain.value_objects.jwt import JwtTokenValue


router = APIRouter(
    prefix="/auth",
    route_class=DishkaRoute,
)


@router.post(
    path="/register",
    response_model=RegisterOutSchema,
    status_code=HTTP_200_OK,
    summary="Request register a new user account",
)
@inject
async def register(
    schema: RegisterInSchema,
    use_case: FromDishka[RegisterUseCase],
    settings: FromDishka[Settings],
) -> RegisterOutSchema:
    command = RegisterCommand(
        name=schema.name,
        second_name=schema.second_name,
        group_number=schema.group_number,
        email=str(schema.email),
        password=schema.password,
        confirm_code_ttl=settings.auth.confirm_code_ttl_sec,
    )

    user: User = await use_case.act(command=command)

    return RegisterOutSchema(
        user_uid=user.id.value,
    )


@router.post(
    path="/confirm",
    response_model=ConfirmOutSchema,
    status_code=HTTP_201_CREATED,
    summary="Confirm user registration and receive JWT token",
)
async def confirm(
    schema: ConfirmInSchema,
    response: Response,
    use_case: FromDishka[ConfirmRegisterUseCase],
) -> ConfirmOutSchema:
    command =ConfirmRegisterCommand(
        user_id=schema.user_id,
        confirm_code=schema.confirm_code,
    )

    token: JwtTokenValue = await use_case.act(command=command)

    schema = ConfirmOutSchema(jwt_auth_token=token.value)

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
    summary="Authenticate user and receive JWT token",
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

    schema = LoginOutSchema(jwt_auth_token=token.value)

    return schema