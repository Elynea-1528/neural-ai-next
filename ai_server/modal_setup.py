import subprocess
import sys


# Segédfüggvény a parancsokhoz
def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError:
        print(f"❌ Hiba: {command}")
        sys.exit(1)


# Modal ellenőrzése
try:
    import modal
except ImportError:
    run_command(f"{sys.executable} -m pip install modal")

print("🔧 Szerver kód FRISSÍTÉSE (Robust Proxy + Logging)...")

# --- ÚJ, JAVÍTOTT SZERVER KÓD ---

import os
import subprocess
import time
import modal
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx

# --- MODELLEK ---
MODELS = [
    "mychen76/qwen3_cline_roocode:32b",
    "mychen76/qwen3_cline_roocode:14b",
    "mychen76/qwen2.5_cline_roocode:32b"
]

APP_NAME = "roo-code-final-server"
VOLUME_NAME = "ollama-models"

# Image: zstd + curl + Ollama
image = (
    modal.Image.debian_slim()
    .apt_install("curl", "zstd")  
    .run_commands("curl -fsSL https://ollama.com/install.sh | sh")
    .pip_install("httpx", "fastapi", "uvicorn")
)

app = modal.App(APP_NAME)
vol = modal.Volume.from_name(VOLUME_NAME, create_if_missing=True)
web_app = FastAPI()

# --- SEGÉDFÜGGVÉNYEK ---
def wait_for_ollama():
    for _ in range(60):
        try:
            subprocess.check_call(["ollama", "list"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except:
            time.sleep(1)
    return False

# --- TELEPÍTŐ ---
@app.function(
    image=image,
    volumes={"/root/.ollama": vol},
    gpu="L4",
    timeout=7200
)
def setup_models():
    print("⏳ Ollama indítása...")
    subprocess.Popen(["ollama", "serve"])
    
    for _ in range(30):
        try:
            subprocess.check_call(["curl", "-s", "http://127.0.0.1:11434"], stdout=subprocess.DEVNULL)
            break
        except:
            time.sleep(1)

    print("🔍 Modellek ellenőrzése...")
    try:
        installed = subprocess.check_output(["ollama", "list"]).decode()
    except:
        installed = ""

    for model in MODELS:
        if model in installed:
            print(f"✅ {model} -> OK")
        else:
            print(f"⬇️ {model} -> LETÖLTÉS INDUL...")
            try:
                subprocess.run(["ollama", "pull", model], check=True)
                print(f"✅ {model} -> KÉSZ")
            except Exception as e:
                print(f"❌ HIBA {model}: {e}")

# --- SZERVER (PROXY JAVÍTVA) ---
@app.cls(
    image=image,
    gpu="L4",
    volumes={"/root/.ollama": vol},
    scaledown_window=300,
    timeout=3600,
)
class OllamaServer:
    @modal.enter()
    def start(self):
        # Env vars - 128k context
        os.environ["OLLAMA_KV_CACHE_TYPE"] = "q4_0"
        os.environ["OLLAMA_FLASH_ATTENTION"] = "1"
        os.environ["OLLAMA_NUM_CTX"] = "131072"
        os.environ["OLLAMA_HOST"] = "127.0.0.1:11434"
        os.environ["OLLAMA_ORIGINS"] = "*"
        
        print("🚀 Ollama indítása...")
        subprocess.Popen(["ollama", "serve"])
        
        # Ping check
        for _ in range(30):
            try:
                subprocess.check_call(["curl", "-s", "http://127.0.0.1:11434"], stdout=subprocess.DEVNULL)
                break
            except:
                time.sleep(1)
        print("✅ Szerver ONLINE.")

    @modal.asgi_app()
    def api(self):
        return web_app

@web_app.post("/v1/chat/completions")
async def chat_endpoint(request: Request):
    body = await request.json()
    model_name = body.get("model", "unknown")
    print(f"📩 ÚJ KÉRÉS ÉRKEZETT: {model_name}") # Ez látszik majd a Modal logban

    async def proxy_stream():
        async with httpx.AsyncClient(timeout=None) as client:
            try:
                # Streaming request az Ollamának
                async with client.stream("POST", "http://127.0.0.1:11434/v1/chat/completions", json=body) as response:
                    # Fejlécek és státusz logolása debug célból
                    print(f"DEBUG: Ollama válasz status: {response.status_code}")
                    
                    async for chunk in response.aiter_bytes():
                        # Itt küldjük vissza a chunkokat
                        yield chunk
            except Exception as e:
                print(f"❌ PROXY HIBA: {str(e)}")
                yield f'{{"error": "{str(e)}"}}'.encode()
    
    # Kényszerített headers a stabilitásért
    return StreamingResponse(
        proxy_stream(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no" # Nginx/Proxy buffering tiltása
        }
    )
"""

with open("ollama_server.py", "w", encoding="utf-8") as f:
    f.write(server_code)

print("🚀 Szerver kód frissítve.")
print("🔄 Újraindítás (Deploy)...")
run_command("python start.py")
