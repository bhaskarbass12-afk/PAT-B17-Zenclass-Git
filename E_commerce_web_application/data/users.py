PASSWORD = "secret_sauce"

# All six accounts published on the Sauce Demo login page itself. Only
# locked_out_user is expected to be rejected; the rest exhibit various UI
# quirks (problem_user, performance_glitch_user, error_user, visual_user)
# but should still be able to log in successfully.
PREDEFINED_USERS = [
    {"username": "standard_user", "password": PASSWORD, "should_succeed": True},
    {
        "username": "locked_out_user",
        "password": PASSWORD,
        "should_succeed": False,
        "expected_error": "Sorry, this user has been locked out.",
    },
    {"username": "problem_user", "password": PASSWORD, "should_succeed": True},
    {"username": "performance_glitch_user", "password": PASSWORD, "should_succeed": True},
    {"username": "error_user", "password": PASSWORD, "should_succeed": True},
    {"username": "visual_user", "password": PASSWORD, "should_succeed": True},
]

# A mix of invalid username/password combinations: an unrecognized user, a
# valid username with the wrong password, and missing-field cases.
INVALID_CREDENTIALS = [
    {"username": "invalid_user", "password": "wrong_password"},
    {"username": "standard_user", "password": "wrong_password"},
    {"username": "", "password": PASSWORD},
    {"username": "standard_user", "password": ""},
]
