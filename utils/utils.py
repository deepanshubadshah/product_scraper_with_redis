import time
from typing import Callable


def sanitize_price(raw_price: str) -> float:
    """
    Sanitize and convert the price string to a float.
    """
    # Remove non-numeric characters except for the decimal point
    sanitized_price = ''.join(char for char in raw_price if char.isdigit() or char == '.')
    return float(sanitized_price)


def retry(func: Callable, retries: int = 3, delay: int = 2, *args, **kwargs):
    """
    Retry a function in case of failure.

    Args:
        func (Callable): The function to execute.
        retries (int): The number of retry attempts.
        delay (int): The delay (in seconds) between retries.
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.

    Returns:
        Any: The return value of the function if successful.

    Raises:
        Exception: The last exception raised after all retries fail.
    """
    last_exception = None
    for attempt in range(1, retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            print(f"Attempt {attempt}/{retries} failed: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    print("All retry attempts failed.")
    raise last_exception
