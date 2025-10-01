import random
from src.data import ProbeRepository
from fastapi import HTTPException

class ProbeService:
  def __init__(self):
    self.repository = ProbeRepository()
    
  def list_probes(self):
    probes = self.repository.list_probes()
    probes_list = []
    
    for probe_id, probe in probes.items():
      probe_info = {
        "id": probe_id,
        "x": probe["x"],
        "y": probe["y"],
        "direction": probe["direction"]
      }
      
      probes_list.append(probe_info)
      
    return probes_list
  
  def create_environment(self, x: int, y: int, direction: str):
    try:  
      probe_id = "probe" + str(random.randint(1, 1000))
      
      probe = self.repository.create_environment(probe_id, x, y, direction)
      
      return probe
    
    except HTTPException:
      raise
    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))
  
  def move_probe(self, probe_id: str, instructions: str):
    try:
      probes = self.repository.list_probes()
      
      if probe_id not in probes:
        raise HTTPException(status_code=404, detail="Sonda não encontrado")
      
      direction_map = ["NORTH", "EAST", "SOUTH", "WEST"]
    
      move_by_direction = {
        "NORTH": (0, 1),
        "EAST": (1, 0),
        "SOUTH": (0, -1),
        "WEST": (-1, 0)
      }
      
      probe = probes[probe_id]
      x, y, direction, limits = probe["x"], probe["y"], probe["direction"], probe["limits"]
    
      for instruction in instructions:
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
      
      return self.repository.update_probe(probe_id, x, y, direction)
    
    except HTTPException:
      raise
    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))
  
  
    
  
  
    