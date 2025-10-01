from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
import random
from src.schemas.requests import (
  CreateEnvironmentRequest,
  MoveProbeRequest
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
    "limits": {"x": request.x, "y": request.y}
  }
  
  return {
    "id": probe_id,
    "x": 0,
    "y": 0,
    "direction": request.direction
  }

@router.put("/move-probe/{probe_id}")
def move_probe(probe_id: str, request: MoveProbeRequest):
  if probe_id not in probes:
    raise HTTPException(status_code=404, detail="Probe not found")
  
  direction_map = ["NORTH", "EAST", "SOUTH", "WEST"]
  
  move_by_direction = {
    "NORTH": (0, 1),
    "EAST": (1, 0),
    "SOUTH": (0, -1),
    "WEST": (-1, 0)
  }
  
  probe = probes[probe_id]
  x, y, direction, limits = probe["x"], probe["y"], probe["direction"], probe["limits"]
  
  for instruction in request.instruction:
    match instruction:
      case 'L':
        direction = direction_map[(direction_map.index(direction) - 1) % 4]
      case 'R':
        direction = direction_map[(direction_map.index(direction) + 1) % 4]
      case 'M':
        dx, dy = move_by_direction[direction]
        new_x, new_y = x + dx, y + dy
        
        if 0 <= new_x <= limits["x"] and 0 <= new_y <= limits["y"]:
          x, y = new_x, new_y
        else:
          raise HTTPException(status_code=400, detail="Movimento inválido: fora dos limites do planalto")
      case _:
        raise HTTPException(status_code=400, detail="Instrução inválida")
  
  probe.update({"x": x, "y": y, "direction": direction})
  
  return probe  
      