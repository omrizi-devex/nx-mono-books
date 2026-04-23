from fastapi import FastAPI
from common import greet
from ozlogger import get_logger

app = FastAPI()
logger = get_logger(__name__)

@app.get("/hello/{name}")
def greet_endpoint(name: str) -> dict:
    logger.info("Greeting %s", name)
    return {"message": greet(name)}

@app.get("/bye/{name}")
def farewell_endpoint(name: str) -> dict:
    logger.info("Farewell %s", name)
    return {"message": f"Goodbye, {name}!"}
