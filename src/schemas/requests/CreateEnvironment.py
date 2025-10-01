from pydantic import BaseModel

class CreateEnvironmentRequest(BaseModel):
  x: int
  y: int
  direction: str