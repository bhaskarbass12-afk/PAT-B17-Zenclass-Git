class FrameworkError(Exception):
    """Base class for all custom exceptions raised by this framework."""


class ElementInteractionError(FrameworkError):
    """Raised when a page object cannot find or interact with an element
    after waiting, wrapping the underlying Selenium timeout/lookup error.
    """


class LoginFailedError(FrameworkError):
    """Raised when a login attempt does not result in the expected outcome
    (e.g. an error message was expected but never appeared).
    """


class CheckoutError(FrameworkError):
    """Raised when the checkout flow does not reach the expected step or
    confirmation state.
    """


class ProductNotFoundError(FrameworkError):
    """Raised when a product name expected to be present (in the catalog,
    cart, or checkout overview) cannot be located on the page.
    """
