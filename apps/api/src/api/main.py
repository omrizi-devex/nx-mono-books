from fastapi import FastAPI
from common import greet

app = FastAPI()

@app.get("/hello/{name}")
def greet_endpoint(name: str) -> dict:
    return {"message": greet(name)}
