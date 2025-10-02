import pytest
from pydantic import ValidationError
from src.api.schemas.requests import (
  CreateEnvironmentRequest,
  MoveProbeRequest
  )

class TestCreateEnvironmentValidation:
  def test_valid_direction_uppercase(self):
    request = CreateEnvironmentRequest(x=5, y=5, direction="NORTH")
    
    assert request.direction == "NORTH"
  
  def test_valid_direction_lowercase_converted(self):
    request = CreateEnvironmentRequest(x=5, y=5, direction="north")
    
    assert request.direction == "NORTH"
  
  def test_valid_direction_mixed_case_converted(self):
    request = CreateEnvironmentRequest(x=5, y=5, direction="NoRtH")
    
    assert request.direction == "NORTH"
  
  def test_invalid_direction_raises_validation_error(self):
    with pytest.raises(ValidationError) as exc_info:
        CreateEnvironmentRequest(x=5, y=5, direction="INVALID")
    
    assert "Direção inválida" in str(exc_info.value)
  
  def test_all_valid_directions(self):
    valid_directions = ["NORTH", "EAST", "SOUTH", "WEST"]
    
    for direction in valid_directions:
        request = CreateEnvironmentRequest(x=5, y=5, direction=direction.lower())
        
        assert request.direction == direction
  
  def test_negative_coordinates_validation(self):
    with pytest.raises(ValidationError):
        CreateEnvironmentRequest(x=-1, y=5, direction="NORTH")
    
    with pytest.raises(ValidationError):
        CreateEnvironmentRequest(x=5, y=-1, direction="NORTH")
  
  def test_zero_coordinates_allowed(self):
    request = CreateEnvironmentRequest(x=0, y=0, direction="NORTH")
    
    assert request.x == 0
    assert request.y == 0
  
  def test_invalid_instruction_raises_validation_error(self):
    with pytest.raises(ValidationError) as exc_info:
        MoveProbeRequest(instruction="MRXLM")
    
    assert "Instrução deve conter apenas L, R ou M" in str(exc_info.value)
  
  def test_valid_instruction_uppercase(self):
    request = MoveProbeRequest(instruction="MRMLM")
    
    assert request.instruction == "MRMLM"