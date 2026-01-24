import subprocess
import sys

# --- A VÁLASZTOTT MODELL ---
# Ez a jelenlegi legjobb tool-use modell 14B méretben.
# Gyors, pontos, és nem hallucinál felesleges szöveget.
MODEL_NAME = "hhao/qwen2.5-coder-tools:14b"

APP_NAME = "roo-code-pro-server"
VOLUME_NAME = "ollama-models"


def run_command(cmd):
    try:
        subprocess.check_call(cmd, shell=True)
    except:
        print(f"❌ Kritikus hiba: {cmd}")
        sys.exit(1)


# 1. KÖRNYEZET ELLENŐRZÉSE
print("🔧 Rendszer diagnosztika...")
try:
    import modal
except ImportError:
    print("📦 Modal telepítése...")
    run_command(f"{sys.executable} -m pip install modal")

# 2. SZERVER KÓD GENERÁLÁSA
print("📝 Professional Server kód generálása...")

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
MODEL_NAME = "{MODEL_NAME}"

# Image: Debian alap + Zstd (tömörítéshez) + Curl + Ollama
image = (
    modal.Image.debian_slim()
    .apt_install("curl", "zstd", "procps")  # procps kell a pkill-hez
    .run_commands("curl -fsSL https://ollama.com/install.sh | sh")
    .pip_install("httpx", "fastapi", "uvicorn")
)

app = modal.App(APP_NAME)
vol = modal.Volume.from_name(VOLUME_NAME, create_if_missing=True)
web_app = FastAPI()

# --- SEGÉDFÜGGVÉNYEK ---
def wait_for_ollama():
    # Várakozás, amíg a port elérhető
    for _ in range(60):
        try:
            subprocess.check_call(["curl", "-s", "http://127.0.0.1:11434"], stdout=subprocess.DEVNULL)
            return True
        except:
            time.sleep(1)
    return False

# --- TELEPÍTŐ FUNKCIÓ ---
@app.function(
    image=image,
    volumes={{"/root/.ollama": vol}},
    gpu="L4",
    timeout=3600
)
def setup_environment():
    print("🧹 Tisztítás...")
    subprocess.run("pkill ollama", shell=True)

    print("⏳ Ollama indítása karbantartáshoz...")
    subprocess.Popen(["ollama", "serve"])
    if not wait_for_ollama():
        raise Exception("Ollama nem indult el.")

    print(f"🔍 Modell ellenőrzése: {{MODEL_NAME}}")
    try:
        # Listázzuk a modelleket
        installed = subprocess.check_output(["ollama", "list"]).decode()
    except:
        installed = ""

    if MODEL_NAME in installed:
        print("✅ A modell már telepítve van. (Skipping download)")
    else:
        print("⬇️ Modell letöltése... (Ez eltarthat pár percig)")
        try:
            subprocess.run(["ollama", "pull", MODEL_NAME], check=True)
            print("✅ Letöltés sikeres.")
        except Exception as e:
            print(f"❌ Hiba a letöltésnél: {{e}}")
            raise e

# --- SZERVER FUNKCIÓ ---
@app.cls(
    image=image,
    gpu="L4",
    volumes={{"/root/.ollama": vol}},
    scaledown_window=300, # 5 perc után leáll (költséghatékony)
    timeout=3600,
    concurrency_limit=10,
)
class OllamaServer:
    @modal.enter()
    def start(self):
        # --- PROFI KONFIGURÁCIÓ ---
        # 1. Context: 128k (Hatalmas fájlokhoz)
        # 2. Flash Attention: Bekapcsolva (Sebesség)
        # 3. KV Cache: q4_0 (Memória optimalizáció, hogy ne fagyjon le)

        os.environ["OLLAMA_NUM_CTX"] = "131072"
        os.environ["OLLAMA_KV_CACHE_TYPE"] = "q4_0"
        os.environ["OLLAMA_FLASH_ATTENTION"] = "1"
        os.environ["OLLAMA_HOST"] = "127.0.0.1:11434"
        os.environ["OLLAMA_ORIGINS"] = "*"

        print(f"🚀 Szerver indítása (Modell: {{MODEL_NAME}})...")
        subprocess.Popen(["ollama", "serve"])

        if wait_for_ollama():
            print("✅ Szerver ONLINE és fogadja a kéréseket.")
        else:
            print("❌ Hiba: Szerver timeout.")

    @modal.asgi_app()
    def api(self):
        return web_app

@web_app.post("/v1/chat/completions")
async def chat_endpoint(request: Request):
    body = await request.json()

    # Kényszerítjük a modellt, hogy biztosan a jót használja
    body["model"] = MODEL_NAME

    # Logolás a Modal Dashboardra (Debug)
    print(f"📩 Kérés érkezett. Tool use check...")

    async def proxy_stream():
        async with httpx.AsyncClient(timeout=None) as client:
            try:
                async with client.stream("POST", "http://127.0.0.1:11434/v1/chat/completions", json=body) as response:
                    async for chunk in response.aiter_bytes():
                        yield chunk
            except Exception as e:
                print(f"❌ Proxy Hiba: {{e}}")
                yield f'{{"error": "{{str(e)}}"}}'.encode()

    return StreamingResponse(
        proxy_stream(),
        media_type="text/event-stream",
        # Fontos header-ek, hogy a Roo Code ne szakadjon meg
        headers={{"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}}
    )
"""

with open("ollama_server.py", "w", encoding="utf-8") as f:
    f.write(server_code)

# 3. MODELL LETÖLTÉSE (Ha kell)
print("📥 Modell szinkronizálása a felhőbe...")
run_command("modal run ollama_server.py::setup_environment")

# 4. VEZÉRLŐK
print("🛠️ Start/Stop scriptek generálása...")

with open("start.py", "w", encoding="utf-8") as f:
    f.write(
        'import os\nprint("🚀 Indítás...")\nos.system("modal deploy ollama_server.py")\nprint("✅ KÉSZ! URL fent.")'
    )

with open("stop.py", "w", encoding="utf-8") as f:
    f.write(
        f'import os\nprint("🛑 Leállítás...")\nos.system("modal app stop {APP_NAME}")\nprint("✅ Leállítva.")'
    )

print("\n" + "=" * 50)
print("🎉 TELEPÍTÉS KÉSZ! Ez a legprofibb setup.")
print("=" * 50)
print("1. Indítás: python start.py")
print("2. Roo Code beállítás (KÖTELEZŐ!):")
print(f"   - Model ID: {MODEL_NAME}")
print("   - Max Output Tokens: 8192 (NE hagyd -1-en!)")
print("   - Temperature: 0 (Teljesen balra)")
print("=" * 50)
