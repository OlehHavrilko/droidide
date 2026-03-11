from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

class File(BaseModel):
    content: str

@router.get("/files")
async def list_files(path: str = "."):
    try:
        return os.listdir(path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Directory not found")

@router.get("/files/content")
async def get_file_content(path: str):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

@router.post("/files")
async def create_file(path: str):
    try:
        with open(path, "w") as f:
            f.write("")
        return {"message": "File created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/files")
async def update_file(path: str, file: File):
    try:
        with open(path, "w") as f:
            f.write(file.content)
        return {"message": "File updated"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

@router.delete("/files")
async def delete_file(path: str):
    try:
        os.remove(path)
        return {"message": "File deleted"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
