import os
import responses
import pytest

from .block import *
from .client import *

os.environ['http_proxy'] = '127.0.0.1:8888'
os.environ['https_proxy'] = '127.0.0.1:8888'
os.environ["REQUESTS_CA_BUNDLE"] = r"C:\Users\ian.kent\Desktop\Temp\FiddlerCerts\FiddlerRoot1.cer"

token = "62f07d5de29bb522cc818258d85fb4d60e2530c6909b44c1f1c5d75c397e512d37fdbe7d25d23d753a374f7421d6c87ed0381043d598fd570c5d6daff7acaeaa210ffb4ac4664e643b89a2e53daa"
parent_page_url = "https://www.notion.so/Smoke-Test-f51b9f0d709a490a8f7df503c2ace154"
client = NotionClient(token_v2=token)

def test_client_loading_a_page():
    parent_page = client.get_block(parent_page_url)
    cv = client.get_collection_view("https://www.notion.so/4da0503a9dfa412eaca243d5a66bae08?v=eb11d73490d94629b51cadd1172febba")
    col = cv.collection
    print(f"loaded parent page of { parent_page } containing collecdtion id { col.id }")

def test_client_creates_collection():
    parent_page = client.get_block(parent_page_url)
    cvb = parent_page.children.add_new(CollectionViewBlock)
    record_id = client.create_record("collection", parent=cvb, schema=get_collection_schema())
    assert record_id != None    
    augment_collection_with_defaultview(record_id, cvb)

def augment_collection_with_defaultview(col_record_id, col_viewblock):
    col = client.get_collection(col_record_id)
    view = client.get_collection_view(client.create_record("collection_view", parent=col_viewblock, type="table"), collection=col)
    view.set("collection_id", col.id)
    col_viewblock.set("collection_id", col.id)
    col_viewblock.set("view_ids", [view.id])
    col_viewblock.title = "test_client_creates_collection"

def get_collection_schema():
    return {
        "%9:q": {"name": "Check Yo'self", "type": "checkbox"},
        "=d{|": {
            "name": "Tags",
            "type": "multi_select",
            "options": [{
                "color": "orange",
                "id": "79560dab-c776-43d1-9420-27f4011fcaec",
                "value": "A"
            }, {
                "color": "default",
                "id": "002c7016-ac57-413a-90a6-64afadfb0c44",
                "value": "B"
            }, {
                "color": "blue",
                "id": "77f431ab-aeb2-48c2-9e40-3a630fb86a5b",
                "value": "C"
            }]},
        "=d{q": {
            "name": "Category",
            "type": "select",
            "options": [{
                "color": "orange",
                "id": "59560dab-c776-43d1-9420-27f4011fcaec",
                "value": "A"
            }, {
                "color": "default",
                "id": "502c7016-ac57-413a-90a6-64afadfb0c44",
                "value": "B"
            }, {
                "color": "blue",
                "id": "57f431ab-aeb2-48c2-9e40-3a630fb86a5b",
                "value": "C"
            }]},
        "LL[(": {"name": "Person", "type": "person"},
        "4Jv$": {"name": "Estimated value", "type": "number"},
        "OBcJ": {"name": "Where to?", "type": "url"},
        "dV$q": {"name": "Files", "type": "file"},
        "title": {"name": "Name", "type": "title"}
    }