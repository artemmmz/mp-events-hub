from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
    inject,
)
from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from fastapi.responses import Response

from bootstrap.settings import Settings
from seedwork.delivery.api.http.schemas import ErrorSchema
from modules.auth.delivery.api.http.v1.schemas import (
    RegisterInSchema,
    RegisterOutSchema,
    LoginInSchema,
    LoginOutSchema,
    ConfirmInSchema,
    ConfirmOutSchema,
    ResetPasswordInSchema,
    ResetPasswordOutSchema,
    ConfirmResetInSchema,
    ConfirmResetOutSchema,
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
from modules.auth.application.use_cases.reset_password import (
    ResetPasswordUseCase,
    ResetPasswordCommand,
)
from modules.auth.application.use_cases.confirm_reset import (
    ConfirmResetPasswordUseCase,
    ConfirmResetPasswordCommand,
)
from modules.auth.domain.aggregate.user import User
from seedwork.domain.value_objects.jwt import JwtTokenValue


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    route_class=DishkaRoute,
)


@router.post(
    path="/register",
    response_model=RegisterOutSchema,
    status_code=HTTP_200_OK,
    summary="Request register a new user account",
    responses={
        HTTP_200_OK: {"model": RegisterOutSchema, "description": "Request register user"},
        HTTP_400_BAD_REQUEST: {"model": ErrorSchema, "description": "Invalid input"},
        HTTP_401_UNAUTHORIZED: {"model": ErrorSchema, "description": "Unauthorized"},
        HTTP_404_NOT_FOUND: {"model": ErrorSchema, "description": "Resource not found"},
        HTTP_409_CONFLICT: {"model": ErrorSchema, "description": "Conflict rules"},
    }
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
    responses={
        HTTP_201_CREATED: {"model": ConfirmOutSchema, "description": "Register user"},
        HTTP_400_BAD_REQUEST: {"model": ErrorSchema, "description": "Invalid input"},
        HTTP_401_UNAUTHORIZED: {"model": ErrorSchema, "description": "Unauthorized"},
        HTTP_404_NOT_FOUND: {"model": ErrorSchema, "description": "Resource not found"},
        HTTP_409_CONFLICT: {"model": ErrorSchema, "description": "Conflict rules"},
    },
)
async def confirm(
    schema: ConfirmInSchema,
    response: Response,
    use_case: FromDishka[ConfirmRegisterUseCase],
) -> ConfirmOutSchema:
    command = ConfirmRegisterCommand(
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
    responses={
        HTTP_200_OK: {"model": LoginOutSchema, "description": "Login in profile"},
        HTTP_400_BAD_REQUEST: {"model": ErrorSchema, "description": "Invalid input"},
        HTTP_401_UNAUTHORIZED: {"model": ErrorSchema, "description": "Unauthorized"},
        HTTP_404_NOT_FOUND: {"model": ErrorSchema, "description": "Resource not found"},
        HTTP_409_CONFLICT: {"model": ErrorSchema, "description": "Conflict rules"},
    },
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


@router.post(
    path="/reset-password",
    response_model=ResetPasswordOutSchema,
    status_code=HTTP_200_OK,
    summary="Request reset password",
    responses={
        HTTP_200_OK: {"model": ResetPasswordOutSchema, "description": "Request reset password"},
        HTTP_400_BAD_REQUEST: {"model": ErrorSchema, "description": "Invalid input"},
        HTTP_401_UNAUTHORIZED: {"model": ErrorSchema, "description": "Unauthorized"},
        HTTP_404_NOT_FOUND: {"model": ErrorSchema, "description": "Resource not found"},
        HTTP_409_CONFLICT: {"model": ErrorSchema, "description": "Conflict rules"},
    },
)
@inject
async def reset_password(
    schema: ResetPasswordInSchema,
    use_case: FromDishka[ResetPasswordUseCase],
    settings: FromDishka[Settings],
) -> ResetPasswordOutSchema:
    command = ResetPasswordCommand(
        email=schema.email,
        new_password=schema.new_password,
        confirm_code_ttl=settings.auth.reset_password_ttl,
    )

    await use_case.act(command)

    return ResetPasswordOutSchema()


@router.post(
    path="/confirm-reset",
    response_model=ConfirmResetOutSchema,
    status_code=HTTP_200_OK,
    summary="Confirm reset password",
    responses={
        HTTP_200_OK: {"model": ConfirmResetOutSchema, "description": "Confirm reset password"},
        HTTP_400_BAD_REQUEST: {"model": ErrorSchema, "description": "Invalid input"},
        HTTP_401_UNAUTHORIZED: {"model": ErrorSchema, "description": "Unauthorized"},
        HTTP_404_NOT_FOUND: {"model": ErrorSchema, "description": "Resource not found"},
        HTTP_409_CONFLICT: {"model": ErrorSchema, "description": "Conflict rules"},
    },
)
@inject
async def confirm_reset(
    response: Response,
    schema: ConfirmResetInSchema,
    use_case: FromDishka[ConfirmResetPasswordUseCase],
) -> ConfirmResetOutSchema:
    command = ConfirmResetPasswordCommand(
        confirm_code=schema.confirm_code,
        email=schema.email,
    )

    token: JwtTokenValue = await use_case.act(command)

    response.set_cookie(
        key="access_token",
        value=token.value,
        httponly=True,
        samesite="lax",
        expires="Wed, 31 Dec 2137 23:59:59 GMT",
    )

    return ConfirmResetOutSchema(token=token.value)

