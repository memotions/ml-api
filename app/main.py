from fastapi import FastAPI
import uvicorn
from app import pubsub

app = FastAPI()

@app.get("/")
async def index():
    return {"message": "Hello Memothians"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)