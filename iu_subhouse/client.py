from httpx import AsyncClient
from os import getenv


request_client = AsyncClient(
    base_url=getenv("CARRIGE_ENDPOINT", 'http://localhost:5000')
)


class ENDPOINTS:
    CARRIGE_CREATE_SOURCE = '/add_source'
    CARRIGE_GET_VEIN = '/get_vein'
    CARRIGE_GET_SOURCE = '/get_source'
