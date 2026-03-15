import base64
import os
import shutil
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

TEST_RUNTIME_DIR = Path("/tmp/mdland-backend-tests")
TEST_UPLOAD_DIR = TEST_RUNTIME_DIR / "uploads"
BACKEND_ROOT = Path(__file__).resolve().parents[2]

if str(BACKEND_ROOT) not in sys.path:
  sys.path.insert(0, str(BACKEND_ROOT))

os.environ["UPLOAD_DIR"] = str(TEST_UPLOAD_DIR)
os.environ["CORS_ORIGINS"] = "http://localhost:5173"

SAMPLE_PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jq7kAAAAASUVORK5CYII="
)


@pytest.fixture(scope="session")
def client() -> TestClient:
  TEST_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

  if TEST_UPLOAD_DIR.exists():
      shutil.rmtree(TEST_UPLOAD_DIR)

  from app.config import get_settings

  get_settings.cache_clear()
  from app.main import app

  with TestClient(app) as test_client:
      yield test_client


@pytest.fixture
def sample_png_bytes() -> bytes:
  return SAMPLE_PNG_BYTES
