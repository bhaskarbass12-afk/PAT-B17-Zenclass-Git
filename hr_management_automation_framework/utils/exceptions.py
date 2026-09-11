"""Custom exception types for the HR Management automation framework.

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
    (or a labeled form field) after waiting.
    """


class LoginFailedError(FrameworkError):
    """Raised when a login attempt does not result in the expected outcome."""


class UserManagementError(FrameworkError):
    """Raised when creating, searching for, or validating a system user
    does not behave as expected.
    """


class LeaveAssignmentError(FrameworkError):
    """Raised when assigning leave to an employee does not complete or
    confirm as expected.
    """


class ClaimSubmissionError(FrameworkError):
    """Raised when submitting a claim request does not complete or
    confirm as expected.
    """
