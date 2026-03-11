from fastapi import FastAPI
from .routers import ai, files, terminal

app = FastAPI()

app.include_router(ai.router)
app.include_router(files.router)
app.include_router(terminal.router)

@app.get("/")
async def root():
    return {"message": "DroidIDE Backend"}
