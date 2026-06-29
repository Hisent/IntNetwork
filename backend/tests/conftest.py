import os

os.environ.setdefault("SECRET_KEY", "test-secret-key-not-the-default-0123456789")
os.environ.setdefault("ADMIN_EMAIL", "trainer@test.de")
os.environ.setdefault("ADMIN_PASSWORD", "trainerpass1")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_intnetwork.db")
