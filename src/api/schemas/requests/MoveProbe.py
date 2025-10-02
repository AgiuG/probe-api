from pydantic import BaseModel, Field, field_validator

class MoveProbeRequest(BaseModel):
  instruction: str = Field(examples=["MRMLM"])
  
  @field_validator("instruction")
  @classmethod
  def validate_instruction(cls, value): 
    valid_chars = set("LRM")
    if not all(char in valid_chars for char in value.upper()):
      raise ValueError("Instrução deve conter apenas L, R ou M")
    return value.upper()