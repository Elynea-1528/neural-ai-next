import os
import subprocess
import time

import httpx
import modal
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

APP_NAME = "roo-code-server"
VOLUME_NAME = "ollama-models"
MODELS = ["qwen2.5:14b"]

image = (
    modal.Image.debian_slim()
    .apt_install("curl", "zstd")
    # JAVÍTVA: A pontos install.sh URL-t használjuk
    .run_commands("curl -fsSL https://ollama.com/install.sh | sh")
    .pip_install("httpx", "fastapi", "uvicorn")
)

app = modal.App(APP_NAME)
vol = modal.Volume.from_name(VOLUME_NAME, create_if_missing=True)
web_app = FastAPI()


def wait_ollama():
    for _ in range(60):
        try:
            # JAVÍTVA: Port hozzáadva a curl-hez
            subprocess.check_call(
                ["curl", "-s", "http://127.0.0.1:11434"], stdout=subprocess.DEVNULL
            )
            return True
        except:
            time.sleep(1)
    return False


# --- TELEPÍTŐ ---
@app.function(image=image, volumes={"/root/.ollama": vol}, gpu="L4", timeout=3600)
def download_models():
    print("⏳ Ollama indítása...")
    # Telepítéskor nem kell KV Cache trükk
    subprocess.Popen(["ollama", "serve"])
    if not wait_ollama():
        raise Exception("Ollama hiba az indításkor")

    print("🔍 Modellek ellenőrzése a volumon...")
    try:
        installed = subprocess.check_output(["ollama", "list"]).decode()
    except:
        installed = ""

    for model in MODELS:
        if model in installed:
            print(f"✅ {model} már létezik.")
        else:
            print(f"⬇️ {model} letöltése folyamatban...")
            subprocess.run(["ollama", "pull", model], check=True)
            print(f"✅ {model} sikeresen letöltve.")

    vol.commit()


# --- SZERVER ---
@app.cls(
    image=image,
    gpu="L4",
    volumes={"/root/.ollama": vol},
    scaledown_window=120,  # JAVÍTVA: container_idle_timeout helyett 2026-ban ez kell
    timeout=3600,
)
class OllamaServer:
    @modal.enter()
    def start(self):
        # KRITIKUS: A környezeti változókat a 'serve' ELŐTT kell beállítani
        os.environ["OLLAMA_HOST"] = "127.0.0.1:11434"
        os.environ["OLLAMA_ORIGINS"] = "*"

        print("🚀 Ollama indítása KV Cache Q4 módban...")
        subprocess.Popen(["ollama", "serve"])
        wait_ollama()
        print("✅ SZERVER ONLINE.")

    @modal.asgi_app()
    def api(self):
        # JAVÍTVA: dupla { } a NameError ellen
        @web_app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
        async def proxy(request: Request, path: str):
            import json

            url = f"http://127.0.0.1:11434/{path}"
            body = await request.body()

            # Cél: A "format: json" kérés eltávolítása, hogy a modell sima szöveget adjon vissza.
            modified_body = body
            try:
                data = json.loads(body)
                if data.get("format") == "json":
                    del data["format"]
                    modified_body = json.dumps(data).encode("utf-8")
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass

            headers = {
                k: v
                for k, v in request.headers.items()
                if k.lower() not in ["host", "content-length"]
            }
            if modified_body != body:
                headers["content-length"] = str(len(modified_body))

            async def stream_response():
                async with httpx.AsyncClient(timeout=None) as client:
                    async with client.stream(
                        request.method,
                        url,
                        content=modified_body,
                        headers=headers,
                        params=dict(request.query_params),
                    ) as r:
                        async for chunk in r.aiter_bytes():
                            yield chunk

            return StreamingResponse(stream_response(), media_type="application/x-ndjson")

        return web_app
