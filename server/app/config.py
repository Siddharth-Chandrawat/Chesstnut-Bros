import os
from dataclasses import dataclass, field


def _int_env(name: str, default: int) -> int:
    val = os.getenv(name)
    return int(val) if val else default


def _default_workers() -> int:
    cores = os.cpu_count() or 2
    return max(1, cores - 1)


@dataclass(frozen=True)
class Settings:
    kv_base_url: str = os.getenv("KV_BASE_URL", "http://127.0.0.1:8008")

    chesstnut_dir: str = os.getenv("CHESSTNUT_DIR", "../chesstnut")
    engine_worker_path: str = os.getenv("ENGINE_WORKER_PATH", "../chesstnut/engine_worker.py")
    engine_depth: int = _int_env("ENGINE_DEPTH", 4)

    max_search_workers: int = field(
        default_factory=lambda: _int_env("MAX_SEARCH_WORKERS", 0) or _default_workers()
    )
    search_timeout_seconds: int = _int_env("SEARCH_TIMEOUT_SECONDS", 25)

    jwt_secret: str = os.getenv("JWT_SECRET", "dev-secret-change-me")
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = _int_env("JWT_EXPIRE_MINUTES", 1440)

    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = _int_env("PORT", 8000)

    client_origin: str = os.getenv("CLIENT_ORIGIN", "http://localhost:5173")


settings = Settings()