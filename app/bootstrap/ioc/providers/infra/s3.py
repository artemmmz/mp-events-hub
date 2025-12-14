from collections.abc import AsyncIterator

from aiobotocore.session import get_session, AioSession
from aiobotocore.client import AioBaseClient
from dishka import Provider, Scope, provide

from bootstrap.settings import Settings
from seedwork.application.interface.s3.client import IS3Client
from seedwork.infra.s3.impls.btcore import S3AiobotoClient
from seedwork.infra.s3.services.image_metadata import ImageMetadataService


class S3Provider(Provider):
    @provide(scope=Scope.APP)
    def s3_session(self) -> AioSession:
        session = get_session()
        return session

    @provide(scope=Scope.REQUEST)
    async def s3_client(
        self,
        s3_session: AioSession,
        settings: Settings,
    ) -> AsyncIterator[AioBaseClient]:
        async with s3_session.create_client(
            service_name='s3',
            endpoint_url=settings.minio.endpoint_url,
            aws_secret_access_key=settings.minio.aws_secret_access_key,
            aws_access_key_id=settings.minio.aws_access_key_id,
        ) as client:
            yield client

    @provide(scope=Scope.REQUEST)
    def client(self, client: AioBaseClient) -> IS3Client:
        return S3AiobotoClient(
            client=client,
        )


class S3ServicesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def image_metadata_service(self) -> ImageMetadataService:
        return ImageMetadataService()