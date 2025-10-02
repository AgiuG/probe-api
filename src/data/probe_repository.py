import json
import os
from typing import Dict

class ProbeRepository:
  def __init__(self, json_file: str = "db/probes.json"):
    self.json_file = json_file
    self.probes: Dict[str, Dict] = {}
    self._load_json()
    
  def _load_json(self):
    try:
      if os.path.exists(self.json_file):
        with open(self.json_file, "r", encoding='utf-8') as f:
          self.probes = json.load(f)
      else:
        os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
        self.probes = {}
    except (json.JSONDecodeError, FileNotFoundError):
      self.probes = {}
  
  def _save_json(self):
    try:
      os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
      
      with open(self.json_file, "w", encoding='utf-8') as f:
        json.dump(self.probes, f, indent=2, ensure_ascii=False)
        
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Erro ao salvar dados: {str(e)}")
  
  def list_probes(self):
    return self.probes
  
  def create_environment(self, probe_id: str, x: int, y: int, direction: str):
    self.probes[probe_id] = {
      "x": 0,
      "y": 0,
      "direction": direction,
      "limits": {"x": x, "y": y}
    }
    
    self._save_json()
    
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
    
    self._save_json()
    
    probe = self.probes[probe_id]
    
    return {
      "id": probe_id,
      "x": probe["x"],
      "y": probe["y"],
      "direction": probe["direction"]
    }
  