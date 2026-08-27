import re
from typing import Optional

import httpx

from .config import settings


_client: Optional[httpx.AsyncClient] = None

_SAFE_MODEL_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def get_client() -> httpx.AsyncClient:
    global _client

    if _client is None:
        _client = httpx.AsyncClient(
            base_url=settings.kv_base_url,
            timeout=5.0,
        )

    return _client


async def close_client() -> None:
    global _client

    if _client is not None:
        await _client.aclose()
        _client = None


def games_model(username: str) -> str:
    if not _SAFE_MODEL_RE.fullmatch(username):
        raise ValueError(
            f"username {username!r} isn't safe for use as a DynamicKV model name"
        )

    return f"games_{username}"


async def list_models() -> list:
    client = get_client()

    resp = await client.get("/")
    resp.raise_for_status()

    return resp.json()


async def kv_get(model: str, key: str) -> Optional[dict]:
    client = get_client()
    print("[KV] BASE URL:", settings.kv_base_url)
    print("[KV] REQUEST:", f"{settings.kv_base_url}/{model}/{key}")
    print(f"[KV] GET /{model}/{key}")

    resp = await client.get(f"/{model}/{key}")

    print("[KV] ACTUAL URL:", resp.request.url)

    print(f"[KV] RESPONSE: {resp.status_code} {resp.text}")

    if resp.status_code == 404:
        return None

    resp.raise_for_status()

    return resp.json()


async def kv_get_all(model: str) -> dict:
    """
    GET /{model}
    """

    client = get_client()

    resp = await client.get(f"/{model}")

    if resp.status_code == 404:
        return {}

    resp.raise_for_status()

    return resp.json()


async def kv_set(model: str, key: str, value: dict) -> None:
    client = get_client()

    body = {
        "key": key,
        **value,
    }

    print(f"[KV] POST /{model}")
    print(f"[KV] BODY: {body}")

    resp = await client.post(f"/{model}", json=body)

    print(f"[KV] RESPONSE: {resp.status_code} {resp.text}")

    resp.raise_for_status()

async def kv_delete(model: str, key: str) -> None:
    """
    DELETE /{model}/{key}
    """

    client = get_client()

    resp = await client.delete(f"/{model}/{key}")

    if resp.status_code not in (200, 204, 404):
        resp.raise_for_status()


async def kv_delete_model(model: str) -> None:
    """
    DELETE /{model}
    """

    client = get_client()

    resp = await client.delete(f"/{model}")

    if resp.status_code not in (200, 204, 404):
        resp.raise_for_status()


_client = httpx.AsyncClient(
    base_url=settings.kv_base_url,
    timeout=5.0,
    trust_env=False,
)