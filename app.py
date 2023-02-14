import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

import models

app = FastAPI()

SKELETON_MODEL = "skeleton"

@app.get("/video")
async def video_infer(model: str, key: str):
    if model == SKELETON_MODEL:
        return models.skeleton.infer(key)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, log_level="info")
        
