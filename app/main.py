from fastapi import FastAPI
from .api import image_processing, authentication
from .databases import Base, engine

app = FastAPI(title="CloudThumb Project")
Base.metadata.create_all(bind=engine)

app.include_router(image_processing.router, prefix='/image', tags=['image-processing'])
app.include_router(authentication.router, prefix='', tags=['authentication'])

@app.get("/")
def read_root():
    return {"message": "Root endpoint of a simple cloud FastAPI project"}
