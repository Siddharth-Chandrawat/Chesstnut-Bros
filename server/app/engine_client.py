"""
Dispatches the slow minimax search to a fresh, isolated subprocess per
call. This sidesteps two problems at once:

  1. Python's GIL — a subprocess gets a genuinely separate core;
     threads would only contend for one.
  2. Chesstnut's global rules-engine state (see chess_bridge.py) — a
     brand-new interpreter has fresh globals, so nothing can leak
     between two different games' searches even without patching
     readFen. (You should still patch it — see chess_bridge.py — but
     this file's correctness doesn't depend on that patch.)

Bounded by a semaphore sized to (cpu_count - 1) by default: at most
that many searches run at once, no matter how many move requests
arrive. Everything past that limit simply awaits its turn — this does
NOT block the event loop, so fast-path requests for other games keep
being served the whole time.
"""
import asyncio
import json
import sys
from pathlib import Path

from .config import settings

_SEARCH_SLOTS = asyncio.Semaphore(settings.max_search_workers)


class EngineError(Exception):
    pass


class EngineTimeoutError(EngineError):
    pass


async def compute_engine_move(fen: str, depth: int | None = None) -> dict:
    depth = depth or settings.engine_depth
    worker_path = Path(settings.engine_worker_path).resolve()

    async with _SEARCH_SLOTS:
        proc = await asyncio.create_subprocess_exec(
            sys.executable, str(worker_path), fen, str(depth),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=settings.search_timeout_seconds
            )
        except asyncio.TimeoutError:
            # A stuck/hung search must not hold its slot forever — kill it
            # and free the slot for the next queued request.
            proc.kill()
            await proc.wait()
            raise EngineTimeoutError(
                f"Search exceeded {settings.search_timeout_seconds}s and was killed"
            )

    if proc.returncode != 0:
        raise EngineError(f"engine_worker.py failed: {stderr.decode(errors='replace')}")

    try:
        result = json.loads(stdout.decode())
    except json.JSONDecodeError as exc:
        raise EngineError(f"Could not parse engine output: {stdout!r}") from exc

    return result  # expected shape: {"move": [from, to], "eval": <float>}
