from fastapi import FastAPI, Query
from fastapi.openapi.docs import get_redoc_html
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Any, Dict, Union
from typing_extensions import Annotated
# from enum import Enum

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI(redoc_url=None, docs_url="/docs")

# Mount static files.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Chrome doesn't like getting the redoc js file from the normal URL, so I am hosting it as a static asset.
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    assert app.openapi_url is not None
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js"
    )

@app.get("/")
async def root():
    return {"message": "Hello World!"}

# Read a single item by its ID
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Get all items with optional additional queries... or that's the idea, at least. Learning about validations in query parameters.
# Requires that if q is provided, it must be between 3 and 50 characters... and must be the exact value "fixedquery".
# @app.get("/items/")
# async def read_items(q: Annotated[Union[str, None], Query(min_length=3, max_length=50, pattern="^fixedquery$")] = None):
#     results: Dict[str, Any] = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# Learning about receiving multiple values in query parameters.
# Imagine this URL: http://localhost:8000/items/?q=foo&q=bar
# You get this result: {"q": ["foo", "bar"]}
@app.get("/items/")
async def read_items(q: Annotated[list[str], Query()] = ["default", "list"]):
    query_items = {"q": q}
    return query_items

@app.post("/items/")
async def create_item(item: Item):
    # Creates a dict from the item specified in the request body.
    # Uses model_dump() because dict() is deprecated in Pydantic v2's BaseModel.
    item_dict = item.model_dump()
    # Adds a new member named price_with_tax to the item dict if a tax was specified in the request body.
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, queryParam1: Union[str, None] = None):
    result = {"item_id": item_id, **item.model_dump()}
    if queryParam1:
        result.update({"queryParam1": queryParam1})
    return result
