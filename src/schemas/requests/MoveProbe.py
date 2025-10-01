from pydantic import BaseModel

class MoveProbeRequest(BaseModel):
  instruction: str