import modal

# --- VÁLASSZ MODELLT (Kommenteld ki azt, amelyik kell) ---

# 1. OPCIÓ: A NAGYÁGYÚ (Architect módhoz ajánlott)
# Qwen 2.5 32B AWQ - Elfér az L4 GPU-n (24GB)!
MODEL_ID = "Qwen/Qwen2.5-Coder-32B-Instruct-AWQ"
GPU_CONFIG = "l4"  # 24GB VRAM, olcsó és gyors

# 2. OPCIÓ: A GYORS (Ha spórolni akarsz a kredittel)
# MODEL_ID = "Qwen/Qwen2.5-14B-Instruct-AWQ"
# GPU_CONFIG = "t4" # Ez is elég neki, de az L4 gyorsabb

# --- KONFIGURÁCIÓ ---
# vLLM image HF Transferrel a gyors letöltésért
vllm_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.3", "huggingface_hub[hf_transfer]")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
)

app = modal.App("qwen-server")

# Perzisztens tároló (hogy ne töltse le mindig újra)
cache_volume = modal.Volume.from_name("hf-cache-qwen", create_if_missing=True)  # type: ignore[assignment]
CACHE_DIR = "/root/.cache/huggingface"


# --- 1. LETÖLTŐ FÜGGVÉNY (Csak egyszer kell futtatni) ---
@app.function(  # type: ignore[misc]
    image=vllm_image,
    volumes={CACHE_DIR: cache_volume},
    timeout=3600,
)
def download_model():
    from huggingface_hub import snapshot_download

    print(f"📥 {MODEL_ID} letöltése a Volume-ra...")
    snapshot_download(
        repo_id=MODEL_ID,
        cache_dir=CACHE_DIR,
        ignore_patterns=["*.pt", "*.bin"],  # Csak safetensors kell
    )
    print("✅ Letöltés kész! Mehet a deploy.")


# --- 2. SZERVER FÜGGVÉNY (Deploy) ---
@app.function(
    image=vllm_image,
    gpu=GPU_CONFIG,  # Itt használjuk az L4-et
    volumes={CACHE_DIR: cache_volume},
    container_idle_timeout=300,  # 5 perc után lekapcsol (SPÓROLÁS!)
    timeout=600,
    allow_concurrent_inputs=10,
)
@modal.web_server(port=8000, startup_timeout=300)
def serve():
    import subprocess

    print(f"🚀 vLLM indítása ({MODEL_ID})...")

    cmd = [
        "python",
        "-m",
        "vllm.entrypoints.openai.api_server",
        "--model",
        MODEL_ID,
        "--quantization",
        "awq",  # AWQ kötelező ezekhez a modellekhez
        "--dtype",
        "half",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        # Memória optimalizálás L4-re (32B modellnél kritikus!)
        "--gpu-memory-utilization",
        "0.95",
        "--max-model-len",
        "8192",  # Architect módhoz elég
        # --- ROO CODE TOOL SUPPORT (FONTOS!) ---
        "--enable-auto-tool-choice",
        "--tool-call-parser",
        "hermes",  # A Qwen-hez ez a legjobb
        "--trust-remote-code",
    ]

    subprocess.Popen(cmd)
