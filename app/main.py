from endpoints import posting_matching_result
from fastapi import FastAPI
from endpoints import matching

app = FastAPI()
app.include_router(matching.router, prefix="/matching")
app.include_router(posting_matching_result.router, prefix="/matching")
