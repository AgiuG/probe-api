import pytest

class TestProbeRepository:
  def test_create_environment_sucess(self, probe_repository):
    probe_id = "test_probe"
    x, y, direction = 5, 5, "NORTH"
    
    result = probe_repository.create_environment(probe_id, x, y, direction)
    
    assert result["id"] == probe_id
    assert result["x"] == 0
    assert result["y"] == 0
    assert result["direction"] == "NORTH"
    assert probe_id in probe_repository.probes
    assert probe_repository.probes[probe_id]["limits"]["x"] == 5
    assert probe_repository.probes[probe_id]["limits"]["y"] == 5
  
  def test_create_environment_different_directions(self, probe_repository):
    directions = ["NORTH", "EAST", "SOUTH", "WEST"]
    
    for i, direction in enumerate(directions):
      probe_id = f"probe_{i}"
      
      result = probe_repository.create_environment(probe_id, 3, 3, direction)
      
      assert result["direction"] == direction
      assert probe_repository.probes[probe_id]["direction"] == direction
      
  def test_update_probe_sucess(self, probe_repository):
    probe_id = "test_probe"
    probe_repository.create_environment(probe_id, 5, 5, "NORTH")
    
    result = probe_repository.update_probe(probe_id, 2, 3, "EAST")

    assert result["id"] == probe_id
    assert result["x"] == 2
    assert result["y"] == 3
    assert result["direction"] == "EAST"
    assert probe_repository.probes[probe_id]["x"] == 2
    assert probe_repository.probes[probe_id]["y"] == 3
    assert probe_repository.probes[probe_id]["direction"] == "EAST"

  def test_update_probe_multiple_updates(self, probe_repository):
    probe_id = "test_probe"
    probe_repository.create_environment(probe_id, 5, 5, "NORTH")
    
    result1 = probe_repository.update_probe(probe_id, 1, 1, "SOUTH")
    assert result1["x"] == 1
    assert result1["y"] == 1
    assert result1["direction"] == "SOUTH"
    
    result2 = probe_repository.update_probe(probe_id, 4, 2, "WEST")
    assert result2["x"] == 4
    assert result2["y"] == 2
    assert result2["direction"] == "WEST"
  
  def test_list_probes_empty(self, probe_repository):
    result = probe_repository.list_probes()
    
    assert result == {}
    assert len(result) == 0
  
  def test_list_probes_with_single_probe(self, probe_repository):
    probe_repository.create_environment("probe1", 5, 5, "NORTH")
    
    result = probe_repository.list_probes()
    
    assert len(result) == 1
    assert "probe1" in result
    assert result["probe1"]["direction"] == "NORTH"
  
  def test_list_probes_with_multiple_probes(self, probe_repository):
    probe_repository.create_environment("probe1", 5, 5, "NORTH")
    probe_repository.create_environment("probe2", 3, 3, "SOUTH")
    probe_repository.create_environment("probe3", 10, 10, "EAST")
    
    result = probe_repository.list_probes()
    
    assert len(result) == 3
    assert "probe1" in result
    assert "probe2" in result
    assert "probe3" in result
    assert result["probe1"]["limits"]["x"] == 5
    assert result["probe2"]["limits"]["x"] == 3
    assert result["probe3"]["limits"]["x"] == 10
  
    