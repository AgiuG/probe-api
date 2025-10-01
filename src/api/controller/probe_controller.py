from fastapi import APIRouter, HTTPException
from src.api.schemas.requests import (
  CreateEnvironmentRequest,
  MoveProbeRequest
)
from src.service import ProbeService

router = APIRouter()
service = ProbeService()

@router.get("/probes")
def get_probes():
  probes = service.list_probes()
  
  return {"probes": probes}

@router.post("/create-environment")
def create_environment(request: CreateEnvironmentRequest):
  try:
    probe = service.create_environment(request.x, request.y, request.direction)
    
    return probe
  except HTTPException:
    raise
  except Exception as e:
    raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.put("/move-probe/{probe_id}")
def move_probe(probe_id: str, request: MoveProbeRequest):
  try:
    probe = service.move_probe(probe_id, request.instruction)
    
    return probe
  except HTTPException:
    raise
  except Exception as e:
    raise HTTPException(status_code=500, detail="Erro interno do servidor")  
      