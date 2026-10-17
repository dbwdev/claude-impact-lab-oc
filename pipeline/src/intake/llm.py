"""Thin wrapper over the Anthropic SDK: typed output, usage tally, refusal check."""

import threading

import anthropic
from pydantic import BaseModel

from . import config

_client: anthropic.Anthropic | None = None
_lock = threading.Lock()
usage: dict[str, int] = {"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 0,
                         "cache_creation_input_tokens": 0, "calls": 0}


def client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(max_retries=4)
    return _client


class RefusalError(RuntimeError):
    pass


def parse[T: BaseModel](
    *, output: type[T], system, content: list, effort: str, max_tokens: int = 16000, on_start=None
) -> T:
    """on_start() fires on the first stream event, i.e. once the prompt (and its cache) is processed."""
    # Streaming so long reviews don't hit HTTP timeouts.
    with client().messages.stream(
        model=config.MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": content}],
        output_format=output,
        output_config={"effort": effort},
        thinking={"type": "adaptive"},
    ) as stream:
        if on_start:
            for _ in stream:
                on_start()
                break
        message = stream.get_final_message()
    with _lock:
        usage["calls"] += 1
        usage["input_tokens"] += message.usage.input_tokens
        usage["output_tokens"] += message.usage.output_tokens
        usage["cache_read_input_tokens"] += message.usage.cache_read_input_tokens or 0
        usage["cache_creation_input_tokens"] += message.usage.cache_creation_input_tokens or 0
    if message.stop_reason == "refusal":
        raise RefusalError(str(message.stop_details))
    if message.stop_reason == "max_tokens":
        raise RuntimeError(f"Output cut off at max_tokens={max_tokens}")
    return message.parsed_output
