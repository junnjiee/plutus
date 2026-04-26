import shutil
import subprocess
import tempfile
from pathlib import Path

import typer
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from plutus.api.expenses import router as expenses_router

app = typer.Typer(help="Start the plutus web UI.", invoke_without_command=True)

fastapi_app = FastAPI()
fastapi_app.include_router(expenses_router)


@app.callback()
def serve(
    port: int = typer.Option(8000, help="Port to serve on"),
    host: str = typer.Option("127.0.0.1", help="Host to bind to"),
):
    """Start the plutus web UI."""
    if not shutil.which("node") or not shutil.which("npm"):
        typer.echo("Error: node and npm are required to run plutus serve. Install Node.js: https://nodejs.org", err=True)
        raise typer.Exit(1)

    web_dir = Path(__file__).parent / "web"

    with tempfile.TemporaryDirectory(prefix="plutus-web-") as tmp:
        tmp_web = Path(tmp) / "web"
        try:
            shutil.copytree(
                web_dir,
                tmp_web,
                ignore=shutil.ignore_patterns("node_modules", "dist", "dist-ssr"),
            )
        except Exception:
            typer.echo("Error: failed to prepare build directory.", err=True)
            raise typer.Exit(1)

        try:
            subprocess.run(["npm", "ci"], cwd=str(tmp_web), check=True)
        except subprocess.CalledProcessError:
            typer.echo("Error: npm ci failed.", err=True)
            raise typer.Exit(1)

        try:
            subprocess.run(["npm", "run", "build"], cwd=str(tmp_web), check=True)
        except subprocess.CalledProcessError:
            typer.echo("Error: React app build failed.", err=True)
            raise typer.Exit(1)

        dist = tmp_web / "dist"
        if not dist.is_dir():
            typer.echo("Error: build did not produce a dist directory.", err=True)
            raise typer.Exit(1)

        fastapi_app.mount("/", StaticFiles(directory=str(dist), html=True), name="static")

        import uvicorn

        uvicorn.run(fastapi_app, host=host, port=port)