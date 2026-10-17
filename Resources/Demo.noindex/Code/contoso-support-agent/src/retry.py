"""Retries for the model's rate limit.

On Tuesday, October 13, from 11:00, the model deployment answered 429 Too Many Requests for about twenty minutes, and
every chat turn in that time failed with "Something went wrong" (incidents runbook, "429 from the model"). The OpenAI
client retries twice on its own, but its backoff gives up long before a token-per-minute limit resets.

Here a call waits as long as the service asks (its retry-after header), or else 1, 2, 4, 8 seconds with jitter, for at
most five attempts and 30 seconds in all. After that the customer is better off being told to try again, or handed to
a person, than looking at "• • •".

    from src.retry import with_retry
    response = with_retry(openai.responses.create, conversation=conversation_id, input=text)
"""

from __future__ import annotations

import logging
import random
import time
from collections.abc import Callable
from typing import TypeVar

from openai import APIConnectionError, APIStatusError, APITimeoutError, RateLimitError

log = logging.getLogger(__name__)

T = TypeVar("T")

ATTEMPTS = 5
FIRST_WAIT = 1.0  # seconds, doubled after every failure
LONGEST_WAIT = 12.0  # for one wait: what the 429s on Oct 13 asked for
BUDGET = 30.0  # for all the waits of one call together
RETRYABLE = {408, 409, 429, 500, 502, 503, 504}  # 409: a conversation still busy with the previous turn


def retryable(error: BaseException) -> bool:
    """Worth another try: the rate limit, a timeout, a dropped connection or a passing server error. A 400 or a 401
    fails the same way every time, so it fails at once."""
    if isinstance(error, (RateLimitError, APITimeoutError, APIConnectionError)):
        return True
    return isinstance(error, APIStatusError) and error.status_code in RETRYABLE


def retry_after(error: BaseException) -> float | None:
    """How long the service asked us to wait, in seconds. Azure sends retry-after-ms as well as retry-after, and the
    milliseconds are the more precise of the two."""
    response = getattr(error, "response", None)
    if response is None:
        return None
    for header, per_second in (("retry-after-ms", 1000), ("retry-after", 1)):
        value = response.headers.get(header)
        if value:
            try:
                return max(float(value) / per_second, 0.0)
            except ValueError:  # an HTTP date: allowed, but no Azure service sends one
                return None
    return None


def wait_before(attempt: int, error: BaseException, rng: random.Random | None = None) -> float:
    """The pause after failed attempt number `attempt`. Up to half again of random jitter, so that the replicas
    that all failed together don't all come back together."""
    asked = retry_after(error)
    if asked is not None:
        return min(asked, LONGEST_WAIT)
    backoff = FIRST_WAIT * 2 ** (attempt - 1)
    return min(backoff * (1 + (rng or random).random() / 2), LONGEST_WAIT)


def with_retry(call: Callable[..., T], *args, sleep: Callable[[float], None] = time.sleep, **kwargs) -> T:
    """`call(*args, **kwargs)`, tried again after a pause while it fails in a way that waiting can fix.

    Raises the last error when the attempts or the time budget run out. `sleep` is there for the tests."""
    waited = 0.0
    for attempt in range(1, ATTEMPTS + 1):
        try:
            return call(*args, **kwargs)
        except Exception as error:
            if not retryable(error) or attempt == ATTEMPTS:
                raise
            pause = wait_before(attempt, error)
            if waited + pause > BUDGET:
                raise
            # The kind of error and the numbers only: never the customer's message (checklist §4).
            log.warning("model call failed with %s (attempt %d of %d), retrying in %.1f s",
                        type(error).__name__, attempt, ATTEMPTS, pause)
            sleep(pause)
            waited += pause
    raise AssertionError("unreachable: the last attempt returns or raises")
