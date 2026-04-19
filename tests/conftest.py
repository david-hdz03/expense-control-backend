import os

os.environ.setdefault(
    "JWT_SECRET_KEY",
    "test-secret-key-for-unit-tests-only-do-not-use-in-production",
)
os.environ.setdefault("DATABASE_URL", "")
