import os
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from app.services.predict import predict_service
from app.services.feedback import feedback_service
from app.schemas.schema import JournalSchema
from app.core.models import load_model, unload_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    # task execute when startup
    load_dotenv()
    model_predict = await load_model(os.getenv('PREDICT_MODEL_URL'))
    # model_feedback = await load_model(os.getenv('FEEDBACK_MODEL_URL'))
    
    app.state.model_predict = model_predict
    # app.state.model_feedback = model_feedback 
    
    yield
    
    # task execute when shutdown
    await unload_model(app.state.model_predict, app.state.model_feedback)
    app.state.model_predict = None
    # app.state.model_feedback = None

app = FastAPI(lifespan=lifespan)
print("Current Working Directory:", os.getcwd())

@app.get('/')
async def index():
    return {"message": "Hello Memothians"}

@app.post('/predict')
async def predict(journal: JournalSchema, request: Request):
    model_predict = request.app.state.model_predict
    result = await predict_service(journal, model_predict)
    return result

@app.post('/feedback')
async def feedback(journal: JournalSchema, request: Request):
    model_feedback = request.app.state.model_feedback
    result = await feedback_service(journal, model_feedback)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)