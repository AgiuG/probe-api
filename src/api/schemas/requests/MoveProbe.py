from pydantic import BaseModel, Field

class MoveProbeRequest(BaseModel):
  instruction: str = Field(examples=["MRMLM"])