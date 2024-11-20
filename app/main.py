from fastapi import FastAPI, HTTPException
from app.schemas.schema import Journal

import uvicorn

app = FastAPI()

@app.get('/')
async def index():
    return {"message": "Hello Memothians"}

@app.post('/predict')
async def feedback(journal: Journal):
    return 'for predict'

@app.post('/feedback')
async def feedback(journal: Journal):
    return 'for feedback'

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)