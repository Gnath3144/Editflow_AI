"""
Retry and Error Categorization Manager.
Handles exponential backoff, transient network retry loops,
and critical error classification (e.g., quota exhaustion vs retryable 5xx).
"""

import logging
import random
import time
from typing import Callable, Any, Tuple
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

# HTTP status codes that can be safely retried
RETRYABLE_STATUS_CODES = {408, 500, 502, 503, 504}


class QuotaExceededError(Exception):
    """Raised when YouTube API quota has been exhausted."""
    pass


class RetryManager:
    """Provides resilient execution wrapper with exponential backoff and jitter."""

    def __init__(self, max_retries: int = 5, base_delay_seconds: float = 2.0, max_delay_seconds: float = 60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay_seconds
        self.max_delay = max_delay_seconds

    def execute_with_retry(self, operation: Callable[[], Any], operation_name: str = "API Operation") -> Any:
        """Executes a callable with exponential backoff and jitter."""
        attempt = 0
        while True:
            try:
                attempt += 1
                return operation()
            except HttpError as http_err:
                status_code = http_err.resp.status
                error_content = http_err.content.decode("utf-8", errors="replace")

                # Check if quota exceeded
                if status_code == 403 and "quotaExceeded" in error_content:
                    logger.critical("YouTube Data API Quota Exceeded! Daily limit reached.")
                    raise QuotaExceededError("YouTube API quota exceeded. Please wait until quota resets tomorrow or request an increase.") from http_err

                # Non-retryable 4xx client errors
                if status_code < 500 and status_code not in RETRYABLE_STATUS_CODES:
                    logger.error("Non-retryable HTTP %d error in %s: %s", status_code, operation_name, error_content)
                    raise http_err

                if attempt > self.max_retries:
                    logger.error("Exceeded max retries (%d) for %s. Last error: %s", self.max_retries, operation_name, http_err)
                    raise http_err

                sleep_time = min(self.max_delay, (self.base_delay * (2 ** (attempt - 1)))) + random.uniform(0.1, 1.0)
                logger.warning(
                    "Retryable error (%d) during %s (attempt %d/%d). Retrying in %.2f seconds...",
                    status_code, operation_name, attempt, self.max_retries, sleep_time
                )
                time.sleep(sleep_time)

            except (IOError, ConnectionError, TimeoutError) as net_err:
                if attempt > self.max_retries:
                    logger.error("Exceeded max network retries (%d) for %s.", self.max_retries, operation_name)
                    raise net_err

                sleep_time = min(self.max_delay, (self.base_delay * (2 ** (attempt - 1)))) + random.uniform(0.1, 1.0)
                logger.warning(
                    "Network error during %s: %s (attempt %d/%d). Retrying in %.2f seconds...",
                    operation_name, net_err, attempt, self.max_retries, sleep_time
                )
                time.sleep(sleep_time)
