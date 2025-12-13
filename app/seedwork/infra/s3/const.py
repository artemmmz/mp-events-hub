from enum import Enum

class Bucket(Enum):
    IMAGE = "image"
    GIF = "gif"
    VIDEO = "video"


class ClientMethod(Enum):
    GET_OBJECT = "get_object"
