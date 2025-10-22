import functools
import warnings

def deprecated(reason: str = ""):
    """
    Decorator to mark functions as deprecated.
    It will result in a warning being emitted when the function is used.
    """
    def decorator(func):
        msg = f"The function `{func.__name__}` is deprecated."
        if reason:
            msg += f" {reason}"

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.simplefilter("always", DeprecationWarning)  # show even if filtered
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            warnings.simplefilter("default", DeprecationWarning)  # reset filter
            return func(*args, **kwargs)
        return wrapper

    return decorator