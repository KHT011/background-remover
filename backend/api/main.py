from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
static_dir = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse(static_dir / "index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    output = remove(image_bytes)
    return Response(content=output, media_type="image/png")