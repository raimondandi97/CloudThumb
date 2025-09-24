from fastapi import FastAPI
from .api import image_processing

app = FastAPI(title="CloudThumb Project")

app.include_router(image_processing.router, prefix='/image', tags=['image-processing'])

@app.get("/")
def read_root():
    return {"message": "Root endpoint of a simple cloud FastAPI project"}
