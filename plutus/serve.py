from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from plutus.api.expenses import router as expenses_router

app = FastAPI()
app.include_router(expenses_router)

# Serve the built React app in production
dist = Path(__file__).parent / "web" / "dist"
if dist.is_dir():
    app.mount("/", StaticFiles(directory=str(dist), html=True), name="static")
