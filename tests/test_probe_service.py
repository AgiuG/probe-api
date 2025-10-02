import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from src.service.probe_service import ProbeService

class TestProbeService:
  def test_list_probes_empty(self, probe_service):
    probe_service.repository = Mock()
    probe_service.repository.list_probes.return_value = {}
    
    result = probe_service.list_probes()
    
    assert result == []
    probe_service.repository.list_probes.assert_called_once()

  def test_list_probes_with_data(self, probe_service):
      probe_service.repository.list_probes.return_value = {
          "probe1": {"x": 1, "y": 2, "direction": "NORTH"},
          "probe2": {"x": 3, "y": 4, "direction": "EAST"}
      }
      
      result = probe_service.list_probes()
      
      assert len(result) == 2
      assert result[0]["id"] == "probe1"
      assert result[0]["x"] == 1
      assert result[0]["y"] == 2
      assert result[0]["direction"] == "NORTH"
      assert result[1]["id"] == "probe2"
      assert result[1]["x"] == 3
      assert result[1]["y"] == 4
      assert result[1]["direction"] == "EAST"
  
  @patch('src.service.probe_service.random.randint')
  def test_create_environment_success(self, mock_random, probe_service):
    mock_random.return_value = 123
    probe_service.repository.create_environment.return_value = {
        "id": "probe123",
        "x": 0,
        "y": 0,
        "direction": "NORTH"
    }
    
    result = probe_service.create_environment(5, 5, "NORTH")
    
    probe_service.repository.create_environment.assert_called_once_with("probe123", 5, 5, "NORTH")
    assert result["id"] == "probe123"
    assert result["x"] == 0
    assert result["y"] == 0
    assert result["direction"] == "NORTH"
  
  @patch('src.service.probe_service.random.randint')
  def test_create_environment_different_directions(self, mock_random, probe_service):
    mock_random.return_value = 456
    directions = ["NORTH", "EAST", "SOUTH", "WEST"]
    
    for direction in directions:
        probe_service.repository.create_environment.return_value = {
            "id": "probe456",
            "x": 0,
            "y": 0,
            "direction": direction
        }
        
        result = probe_service.create_environment(3, 3, direction)
      
        assert result["direction"] == direction
  
  def test_move_probe_single_move_forward(self, probe_service):
    probe_service.repository.list_probes.return_value = {
        "probe1": {"x": 2, "y": 2, "direction": "NORTH", "limits": {"x": 5, "y": 5}}
    }
    probe_service.repository.update_probe.return_value = {
        "id": "probe1", "x": 2, "y": 3, "direction": "NORTH"
    }
    
    result = probe_service.move_probe("probe1", "M")
    
    probe_service.repository.update_probe.assert_called_once_with("probe1", 2, 3, "NORTH")
    assert result["x"] == 2
    assert result["y"] == 3
    assert result["direction"] == "NORTH"
  
  def test_move_probe_turn_left(self, probe_service):
    probe_service.repository.list_probes.return_value = {
        "probe1": {"x": 2, "y": 2, "direction": "NORTH", "limits": {"x": 5, "y": 5}}
    }
    probe_service.repository.update_probe.return_value = {
        "id": "probe1", "x": 2, "y": 2, "direction": "WEST"
    }
    
    result = probe_service.move_probe("probe1", "L")
    
    probe_service.repository.update_probe.assert_called_once_with("probe1", 2, 2, "WEST")
    assert result["direction"] == "WEST"
  
  def test_move_probe_turn_right(self, probe_service):
    probe_service.repository.list_probes.return_value = {
        "probe1": {"x": 2, "y": 2, "direction": "NORTH", "limits": {"x": 5, "y": 5}}
    }
    probe_service.repository.update_probe.return_value = {
        "id": "probe1", "x": 2, "y": 2, "direction": "EAST"
    }
    
    result = probe_service.move_probe("probe1", "R")
    
    probe_service.repository.update_probe.assert_called_once_with("probe1", 2, 2, "EAST")
    assert result["direction"] == "EAST"
  
  def test_move_probe_complex_sequence(self, probe_service):
    probe_service.repository.list_probes.return_value = {
        "probe1": {"x": 1, "y": 2, "direction": "NORTH", "limits": {"x": 5, "y": 5}}
    }
    probe_service.repository.update_probe.return_value = {
        "id": "probe1", "x": 1, "y": 3, "direction": "EAST"
    }
    
    result = probe_service.move_probe("probe1", "MR")
    
    probe_service.repository.update_probe.assert_called_once_with("probe1", 1, 3, "EAST")

  def test_move_probe_not_found(self, probe_service):
    probe_service.repository.list_probes.return_value = {}
    
    with pytest.raises(HTTPException) as exc_info:
        probe_service.move_probe("nonexistent", "M")
    
    assert exc_info.value.status_code == 404
    assert "Sonda não encontrado" in exc_info.value.detail

  def test_move_probe_invalid_instruction(self, probe_service):
    probe_service.repository.list_probes.return_value = {
        "probe1": {"x": 2, "y": 2, "direction": "NORTH", "limits": {"x": 5, "y": 5}}
    }
  
    with pytest.raises(HTTPException) as exc_info:
        probe_service.move_probe("probe1", "X")
    
    assert exc_info.value.status_code == 400
    assert "Instrução inválida" in exc_info.value.detail

  def test_move_probe_out_of_bounds_north(self, probe_service):
    probe_service.repository.list_probes.return_value = {
        "probe1": {"x": 2, "y": 5, "direction": "NORTH", "limits": {"x": 5, "y": 5}}
    }

    with pytest.raises(HTTPException) as exc_info:
        probe_service.move_probe("probe1", "M")
    
    assert exc_info.value.status_code == 400
    assert "fora dos limites" in exc_info.value.detail

  def test_move_probe_out_of_bounds_south(self, probe_service):
    probe_service.repository.list_probes.return_value = {
        "probe1": {"x": 2, "y": 0, "direction": "SOUTH", "limits": {"x": 5, "y": 5}}
    }
    
    with pytest.raises(HTTPException) as exc_info:
        probe_service.move_probe("probe1", "M")
    
    assert exc_info.value.status_code == 400
    assert "fora dos limites" in exc_info.value.detail

  def test_move_probe_out_of_bounds_east(self, probe_service): 
    probe_service.repository.list_probes.return_value = {
        "probe1": {"x": 5, "y": 2, "direction": "EAST", "limits": {"x": 5, "y": 5}}
    }
    
    with pytest.raises(HTTPException) as exc_info:
        probe_service.move_probe("probe1", "M")
    
    assert exc_info.value.status_code == 400
    assert "fora dos limites" in exc_info.value.detail

  def test_move_probe_out_of_bounds_west(self, probe_service):
    probe_service.repository.list_probes.return_value = {
        "probe1": {"x": 0, "y": 2, "direction": "WEST", "limits": {"x": 5, "y": 5}}
    }
    
    with pytest.raises(HTTPException) as exc_info:
        probe_service.move_probe("probe1", "M")
    
    assert exc_info.value.status_code == 400
    assert "fora dos limites" in exc_info.value.detail

  def test_move_probe_direction_rotation_full_cycle(self, probe_service):
    probe_service.repository.list_probes.return_value = {
        "probe1": {"x": 2, "y": 2, "direction": "NORTH", "limits": {"x": 5, "y": 5}}
    }
    
    probe_service.move_probe("probe1", "LLLL")
    
    probe_service.repository.update_probe.assert_called_once_with("probe1", 2, 2, "NORTH")