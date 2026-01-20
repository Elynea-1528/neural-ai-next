import subprocess
import sys

TARGET_MODELS = [
    # "mychen76/qwen3_cline_roocode:32b",  # gondolkodó modell context:40K
    # "mychen76/qwen3_cline_roocode:14b",  # gondolkodó modell context:40K
    # "mychen76/qwen3_cline_roocode:8b",  # gondolkodó modell context:40K
    # "mychen76/qwen2.5_cline_roocode:32b",  # kódoló modell kontext: 128k
    # "hhao/qwen2.5-coder-tools:32b",  # kódoló modell context:32K
    # "hhao/qwen2.5-coder-tools:14b",  # kódoló modell context:32K
    # "hhao/qwen2.5-coder-tools:7b",  # kódoló modell context:32K
    "qwen2.5:14b",  # általános modell context:32K
    # "qwen2.5-coder:14b",  # általános modell context:32K
]

APP_NAME = "roo-code-server"
VOLUME_NAME = "ollama-models"


# ---------------------------------------------------------
def run_command(cmd):
    try:
        subprocess.check_call(cmd, shell=True)
    except:
        print(f"❌ Hiba: {cmd}")
        sys.exit(1)


print("🔧 Környezet ellenőrzése...")
try:
    import modal
except ImportError:
    print("📦 Modal telepítése...")
    run_command(f"{sys.executable} -m pip install modal")

try:
    import httpx
except ImportError:
    print("📦 httpx telepítése...")
    run_command(f"{sys.executable} -m pip install httpx")

# ---------------------------------------------------------
print("📝 Szerver kód generálása...")

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
MODELS = {TARGET_MODELS}

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
            subprocess.check_call(["curl", "-s", "http://127.0.0.1:11434"], stdout=subprocess.DEVNULL)
            return True
        except:
            time.sleep(1)
    return False

# --- TELEPÍTŐ ---
@app.function(
    image=image,
    volumes={{"/root/.ollama": vol}},
    gpu="L4",
    timeout=3600
)
def download_models():
    print("⏳ Ollama indítása...")
    # Telepítéskor nem kell KV Cache trükk
    subprocess.Popen(["ollama", "serve"])
    if not wait_ollama(): raise Exception("Ollama hiba az indításkor")

    print("🔍 Modellek ellenőrzése a volumon...")
    try:
        installed = subprocess.check_output(["ollama", "list"]).decode()
    except:
        installed = ""

    for model in MODELS:
        if model in installed:
            print(f"✅ {{model}} már létezik.")
        else:
            print(f"⬇️ {{model}} letöltése folyamatban...")
            subprocess.run(["ollama", "pull", model], check=True)
            print(f"✅ {{model}} sikeresen letöltve.")
    
    vol.commit()

# --- SZERVER ---
@app.cls(
    image=image,
    gpu="L4",
    volumes={{"/root/.ollama": vol}},
    scaledown_window=120, # JAVÍTVA: container_idle_timeout helyett 2026-ban ez kell
    timeout=3600
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
        # JAVÍTVA: dupla {{ }} a NameError ellen
        @web_app.api_route("/{{path:path}}", methods=["GET", "POST", "PUT", "DELETE"])
        async def proxy(request: Request, path: str):
            import json
            url = f"http://127.0.0.1:11434/{{path}}"
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

            headers = {{k: v for k, v in request.headers.items() if k.lower() not in ["host", "content-length"]}}
            if modified_body != body:
                headers["content-length"] = str(len(modified_body))

            async def stream_response():
                async with httpx.AsyncClient(timeout=None) as client:
                    async with client.stream(
                        request.method, 
                        url, 
                        content=modified_body,
                        headers=headers,
                        params=dict(request.query_params)
                    ) as r:
                        async for chunk in r.aiter_bytes():
                            yield chunk

            return StreamingResponse(stream_response(), media_type="application/x-ndjson")
        
        return web_app
"""

with open("ollama_server.py", "w", encoding="utf-8") as f:
    f.write(server_code)

# 3. FOLYAMATOK
print("\n📥 1. Lépés: Modellek biztosítása a felhőben...")
run_command("modal run ollama_server.py::download_models")

print("\n🚀 2. Lépés: Szerver deploy...")
run_command("modal deploy ollama_server.py")

print("\n🛠️ 3. Lépés: Segédfájlok frissítése...")
with open("start.py", "w", encoding="utf-8") as f:
    f.write('import os\nprint("🚀 Indítás...")\nos.system("modal deploy ollama_server.py")')

with open("stop.py", "w", encoding="utf-8") as f:
    f.write(f'import os\nprint("🛑 Leállítás...")\nos.system("modal app stop {APP_NAME}")')

print("\n✨ MINDEN KÉSZ! ✨")
