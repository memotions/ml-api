import os
import uvicorn
from transformers import TFBertModel

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from app.core.logging_config import setup_logging
from app.services.predict import predict_service
from app.services.feedback import feedback_service
from app.schemas.schema import JournalSchema
from app.core.models import load_model, unload_model

load_dotenv()
env = os.getenv("ENVIRONMENT", "production")
logger, log_config = setup_logging(env)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # task execute when startup
    logger.info("Load Model")

    model_predict = await load_model("./app/core/models/memotions.keras")


    app.state.model_predict = model_predict

    logger.info(f"Model stored in app state : {app.state.model_predict}")
    yield

    # task execute when shutdown
    await unload_model(app.state.model_predict)
    app.state.model_predict = None


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index():
    return {"message": "Hello Memothians"}


@app.post("/predict")
async def predict(journal: JournalSchema, request: Request):
    model_predict = request.app.state.model_predict
    result = await predict_service(journal, model_predict)
    return result


@app.post("/feedback")
async def feedback(journal: JournalSchema, request: Request):
    result = await feedback_service(journal)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_config=log_config)
