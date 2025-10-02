from pydantic import BaseModel, Field, field_validator

class CreateEnvironmentRequest(BaseModel):
  x: int = Field(examples=[5])
  y: int = Field(examples=[5])
  direction: str = Field(examples=["NORTH"])
  
  @field_validator("x", "y")
  @classmethod
  def validate_coordinates(cls, value):
    if value < 0:
      raise ValueError("Coordenadas devem ser maiores ou iguais a zero")
    return value
  
  @field_validator("direction")
  @classmethod
  def validate_direction(cls, value):
    valid_directions = ["NORTH", "EAST", "SOUTH", "WEST"]
    if value.upper() not in valid_directions:
      raise ValueError(f"Direção inválida. Direções válidas são: {', '.join(valid_directions)}")
    return value.upper()