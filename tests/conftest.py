import pytest
import tempfile
import os
from unittest.mock import Mock
from src.data.probe_repository import ProbeRepository
from src.service.probe_service import ProbeService

@pytest.fixture
def temp_json_file():
  file_descriptor, path = tempfile.mkstemp(suffix='json')
  os.close(file_descriptor)
  yield path
  os.unlink(path)

@pytest.fixture
def probe_repository(temp_json_file):
  return ProbeRepository(json_file=temp_json_file)

@pytest.fixture
def probe_service():
  service = ProbeService()
  service.repository = Mock()
  return service

@pytest.fixture
def sample_probe_data():
  return {
    "id": "probe123",
    "x": 2,
    "y": 3,
    "direction": "NORTH",
    "limits": {"x": 5, "y": 5}
  }