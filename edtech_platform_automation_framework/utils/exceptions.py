"""Custom exception types for the EdTech platform automation framework.

Wrapping Selenium's built-in exceptions in these domain-specific types
keeps test failures readable (the message describes *what business
action* failed, not just "element not found") and gives the framework a
single, predictable set of exception types instead of letting raw
Selenium tracebacks leak into every test.
"""


class FrameworkError(Exception):
    """Base class for all custom exceptions raised by this framework."""


class ElementInteractionError(FrameworkError):
    """Raised when a page object cannot find or interact with an element
    after waiting.
    """


class LoginFailedError(FrameworkError):
    """Raised when a login attempt does not result in the expected outcome."""


class LogoutFailedError(FrameworkError):
    """Raised when a logout attempt does not result in the expected outcome."""


class NavigationError(FrameworkError):
    """Raised when clicking a link/button does not land on the page it is
    supposed to.
    """


class FeatureNotFoundError(FrameworkError):
    """Raised when a feature the test brief describes cannot actually be
    located anywhere on the live site after a thorough search.

    Used specifically for the "Dobby Guvi Assistant" test case: rather
    than fabricate a locator for a widget that doesn't exist, the test
    raises this with a message documenting exactly what was checked, so
    the failure is honest and immediately actionable instead of a
    misleading green pass or a generic "element not found".
    """
