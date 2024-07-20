from falcon import Request, Response, HTTP_200
from iu_datamodels import SourceShort
from iu_subhouse.cache import redis_client
from .utils import httperr_on_validate, httperr_on_error
from iu_subhouse.client import request_client, ENDPOINTS
from json import dumps, loads
from loguru import logger


class SourcesResource:
    @httperr_on_validate
    @httperr_on_error
    async def on_post(self, req: Request, resp: Response):
        raw = bytes(await req.stream.read())
        SourceShort.model_validate_json(raw)
        data = loads(raw)
        response = await request_client.post(
            ENDPOINTS.CARRIGE_CREATE_SOURCE,
            content=raw
        )
        created_id = response.json()['created_id']
        await redis_client.rpush(
            f'iu_subhouse:unused_sources:{data["vein_id"]}',
            created_id
        )
        await redis_client.set(f'iu_subhouse:source_vein:{created_id}', data['vein_id'])
        resp.text = dumps({
            'status': 'ok'
        })

    @httperr_on_error
    async def on_get(self, req: Request, resp: Response):
        vein_id = req.get_param_as_int('vein_id')
        source_id = await redis_client.rpop(f'iu_subhouse:unused_sources:{vein_id}')
        resp.status = HTTP_200
        if not source_id:
            resp.text = dumps(
                {'source_id': -1}
            )
        else:
            resp.text = dumps(
                {"source_id": source_id.decode()}
            )

    @httperr_on_error
    async def on_put(self, req: Request, resp: Response):
        data = loads((await req.stream.read()).decode())
        source_id = data['source_id']
        vein_id = (await redis_client.get(f'iu_subhouse:source_vein:{source_id}')).decode()
        await redis_client.rpush(f'iu_subhouse:unused_sources:{vein_id}', source_id)
        resp.status = HTTP_200
