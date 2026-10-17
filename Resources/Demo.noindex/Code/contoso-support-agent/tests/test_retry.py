"""uv run pytest. The retries of src/retry.py against a fake model: no Azure, and no real waiting."""

import random

import httpx
import pytest
from openai import AuthenticationError, RateLimitError

from src import retry


def rate_limited(retry_after: str | None = None) -> RateLimitError:
    """The 429 the model deployment answered on October 13, with its retry-after header if any."""
    headers = {"retry-after": retry_after} if retry_after else {}
    request = httpx.Request("POST", "https://ai-contoso-k3x7q.services.ai.azure.com/openai/v1/responses")
    response = httpx.Response(429, headers=headers, request=request)
    return RateLimitError("Error code: 429 - token rate limit", response=response, body=None)


class Model:
    """Fails with the given errors, in order, then answers."""

    def __init__(self, *errors: Exception):
        self.errors = list(errors)
        self.calls = 0

    def __call__(self, **kwargs) -> str:
        self.calls += 1
        if self.errors:
            raise self.errors.pop(0)
        return "answer"


def test_waits_as_long_as_the_service_asks():
    pauses: list[float] = []
    model = Model(rate_limited("12"))

    assert retry.with_retry(model, sleep=pauses.append, input="Where's my order 50342?") == "answer"
    assert pauses == [12.0]
    assert model.calls == 2


def test_backs_off_with_jitter_when_not_told():
    rng = random.Random(4)
    waits = [retry.wait_before(attempt, rate_limited(), rng) for attempt in (1, 2, 3, 4)]

    for attempt, wait in enumerate(waits, start=1):
        assert 2 ** (attempt - 1) <= wait <= 1.5 * 2 ** (attempt - 1)


def test_gives_up_after_five_attempts():
    model = Model(*[rate_limited("1") for _ in range(6)])

    with pytest.raises(RateLimitError):
        retry.with_retry(model, sleep=lambda seconds: None)
    assert model.calls == retry.ATTEMPTS


def test_errors_that_waiting_cant_fix_fail_at_once():
    request = httpx.Request("POST", "https://ai-contoso-k3x7q.services.ai.azure.com/openai/v1/responses")
    denied = AuthenticationError("Error code: 401", response=httpx.Response(401, request=request), body=None)
    model = Model(denied)

    with pytest.raises(AuthenticationError):
        retry.with_retry(model, sleep=lambda seconds: pytest.fail("waited for a 401"))
    assert model.calls == 1


def test_stays_inside_the_time_budget():
    pauses: list[float] = []
    model = Model(*[rate_limited("12") for _ in range(4)])

    with pytest.raises(RateLimitError):
        retry.with_retry(model, sleep=pauses.append)
    assert pauses == [12.0, 12.0]  # a third 12-second wait would pass the 30 seconds
    assert sum(pauses) <= retry.BUDGET
