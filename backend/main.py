from fastapi import FastAPI
# from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.docs import get_redoc_html
from fastapi.staticfiles import StaticFiles

app = FastAPI(redoc_url=None, docs_url="/docs")

# Mount static files.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Chrome doesn't like getting the redoc js file from the normal URL, so I am hosting it as a static asset.
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js"
    )

@app.get("/")
async def root():
    return {"message": "Hello World!"}
