from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
import random
from src.schemas.requests import (
  CreateEnvironmentRequest
)

router = APIRouter()

probes: Dict[str, Dict] = {}

@router.get("/probes")
def get_probes():
  probes_list = []
  for probe_id, probe in probes.items():
    probe_info = {
      "id": probe_id,
      "x": probe["x"],
      "y": probe["y"],
      "direction": probe["direction"]
    }
    probes_list.append(probe_info)
  return {"probes": probes_list}

@router.post("/create-environment")
def create_environment(request: CreateEnvironmentRequest):
  probe_id = "probe" + str(random.randint(1, 1000))
  
  probes[probe_id] = {
    "x": 0, 
    "y": 0, 
    "direction": request.direction, 
    "limites": {"x": request.x, "y": request.y}
  }
  
  return {
    "id": probe_id,
    "x": 0,
    "y": 0,
    "direction": request.direction
  }