import os
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from app.services.predict import predict_service
from app.services.feedback import feedback_service
from app.schemas.schema import JournalSchema
from app.core.models import load_model, unload_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    # task execute when startup
    load_dotenv()
    model = await load_model(os.getenv('MODEL_URL'))
    app.state.model = model  # Store model in app's state for global access
    
    yield
    
    # task execute when shutdown
    await unload_model(model)

app = FastAPI(lifespan=lifespan)

@app.get('/')
async def index():
    return {"message": "Hello Memothians"}

@app.post('/predict')
async def predict(journal: JournalSchema):
    result = await predict_service(journal)
    return result

@app.post('/feedback')
async def feedback(journal: JournalSchema):
    result = await feedback_service(journal)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)