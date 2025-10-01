from typing import Dict

class ProbeRepository:
  def __init__(self):
    self.probes: Dict[str, Dict] = {}
  
  def list_probes(self):
    return self.probes
  
  def create_environment(self, probe_id: str, x: int, y: int, direction: str):
    self.probes[probe_id] = {
      "x": 0,
      "y": 0,
      "direction": direction,
      "limits": {"x": x, "y": y}
    }
    
    probe = self.probes[probe_id]
    
    return {
      "id": probe_id,
      "x": probe["x"],
      "y": probe["y"],
      "direction": probe["direction"]
    }
    
  def update_probe(self, probe_id, x, y, direction):
    self.probes[probe_id].update({
      "x": x,
      "y": y,
      "direction": direction
    })
    
    probe = self.probes[probe_id]
    
    return {
      "id": probe_id,
      "x": probe["x"],
      "y": probe["y"],
      "direction": probe["direction"]
    }
  