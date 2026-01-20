import subprocess
import sys

# --- A KIVÁLASZTOTT MODELL ---
# Ez a hivatalos Qwen 2.5 Coder 14B.
# - Nem gondolkodik (No thinking tokens)
# - Profi Tool Use (Eszközhasználat)
# - Gyors és stabil
SELECTED_MODEL = "qwen2.5-coder:14b"

APP_NAME = "roo-code-final-server"
VOLUME_NAME = "ollama-models"


# Segédfüggvény
def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError:
        print(f"❌ Hiba: {command}")
        sys.exit(1)


print("🔧 Környezet ellenőrzése...")
try:
    import modal
except ImportError:
    print("📦 Modal telepítése...")
    run_command(f"{sys.executable} -m pip install modal")

# ---------------------------------------------------------
# 1. SZERVER KÓD GENERÁLÁSA (14B-re optimalizálva)
# ---------------------------------------------------------
print(f"📝 Szerver kód generálása ({SELECTED_MODEL})...")

server_code = f"""
import os
import subprocess
import time
import modal
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx

APP_NAME = "{APP_NAME}"
VOLUME_NAME = "{VOLUME_NAME}"
MODEL_NAME = "{SELECTED_MODEL}"

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

# --- TELEPÍTŐ ---
@app.function(
    image=image,
    volumes={{"/root/.ollama": vol}},
    gpu="L4",
    timeout=7200
)
def setup_model():
    print("⏳ Ollama indítása...")
    subprocess.Popen(["ollama", "serve"])
    
    # Várakozás
    for _ in range(30):
        try:
            subprocess.check_call(["curl", "-s", "http://127.0.0.1:11434"], stdout=subprocess.DEVNULL)
            break
        except:
            time.sleep(1)

    print(f"🔍 {{MODEL_NAME}} keresése...")
    try:
        installed = subprocess.check_output(["ollama", "list"]).decode()
    except:
        installed = ""

    if MODEL_NAME in installed:
        print(f"✅ {{MODEL_NAME}} -> MÁR TELEPÍTVE.")
    else:
        print(f"⬇️ {{MODEL_NAME}} -> LETÖLTÉS INDUL... (Gyors lesz, kb 9GB)")
        try:
            subprocess.run(["ollama", "pull", MODEL_NAME], check=True)
            print(f"✅ {{MODEL_NAME}} -> KÉSZ.")
        except Exception as e:
            print(f"❌ HIBA: {{e}}")

# --- SZERVER ---
@app.cls(
    image=image,
    gpu="L4",
    volumes={{"/root/.ollama": vol}},
    scaledown_window=300, # 5 perc után leáll
    timeout=3600,
)
class OllamaServer:
    @modal.enter()
    def start(self):
        # ⚠️ 14B MODELL OPTIMALIZÁCIÓ
        # Mivel a 14B kicsi (9GB), az L4-en (24GB) BŐVEN elfér a 128k Context!
        # Nem kell lebutítani 32k-ra.
        
        os.environ["OLLAMA_NUM_CTX"] = "131072"  # 128k Context
        os.environ["OLLAMA_KV_CACHE_TYPE"] = "q4_0" # Memória spórolás a biztonság kedvéért
        os.environ["OLLAMA_FLASH_ATTENTION"] = "1"
        os.environ["OLLAMA_HOST"] = "127.0.0.1:11434"
        os.environ["OLLAMA_ORIGINS"] = "*"
        
        print(f"🚀 Ollama indítása (Modell: {{MODEL_NAME}}, Context: 128k)...")
        subprocess.Popen(["ollama", "serve"])
        
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
    
    # Kényszerítjük a modellt, ha a Roo Code mást küldene
    body["model"] = MODEL_NAME
    print(f"📩 KÉRÉS ÉRKEZETT (Modell kényszerítve: {{MODEL_NAME}})")

    async def proxy_stream():
        async with httpx.AsyncClient(timeout=None) as client:
            try:
                async with client.stream("POST", "http://127.0.0.1:11434/v1/chat/completions", json=body) as response:
                    async for chunk in response.aiter_bytes():
                        yield chunk
            except Exception as e:
                yield f'{{"error": "{{str(e)}}"}}'.encode()
    
    return StreamingResponse(
        proxy_stream(), 
        media_type="text/event-stream",
        headers={{"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}}
    )
"""

with open("ollama_server.py", "w", encoding="utf-8") as f:
    f.write(server_code)

# ---------------------------------------------------------
# 2. MODELL LETÖLTÉSE
# ---------------------------------------------------------
print(f"📥 {SELECTED_MODEL} letöltése a felhőbe...")
run_command("modal run ollama_server.py::setup_model")

# ---------------------------------------------------------
# 3. VEZÉRLŐK
# ---------------------------------------------------------
print("🛠️ Start/Stop scriptek generálása...")

with open("start.py", "w", encoding="utf-8") as f:
    f.write(
        'import os\nprint("🚀 Indítás...")\nos.system("modal deploy ollama_server.py")\nprint("✅ KÉSZ! URL fent.")'
    )

with open("stop.py", "w", encoding="utf-8") as f:
    f.write(
        'import os\nprint("🛑 Leállítás...")\nos.system("modal app stop roo-code-final-server")\nprint("✅ Leállítva.")'
    )

print("\n" + "=" * 50)
print("🎉 KÉSZ! Átállva a qwen2.5-coder:14b modellre.")
print("=" * 50)
print("1. Indítsd el: python start.py")
print("2. Roo Code beállítás:")
print(f"   - Model ID: {SELECTED_MODEL}")
print("   - Context: 128k mehet nyugodtan!")
