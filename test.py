from httpx import Client
from uuid import uuid4
from iu_datamodels import SourceShort

client = Client(
    base_url='http://127.0.0.1:8000'
)
response = client.post(
    '/source',
    json=SourceShort(
        vein_id=1,
        slug=uuid4().hex,
        source_metadata={
            'example': 'a'
        }
    ).model_dump_json()
)
print(response.status_code)
print(response.text)