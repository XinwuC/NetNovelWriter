import os
import shutil
import pytest
import sys

# Add skills directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from skills.manage_writer.manage_writer import spawn_writer, kill_writer, AGENTS_DIR

def test_spawn_and_kill_writer():
    writer_name = "test_writer_x1"
    target_dir = os.path.join(AGENTS_DIR, f"nnw_writer_{writer_name}")
    archive_dir = os.path.join(AGENTS_DIR, f"archive_nnw_writer_{writer_name}")
    
    # Cleanup before test
    if os.path.exists(target_dir): shutil.rmtree(target_dir)
    if os.path.exists(archive_dir): shutil.rmtree(archive_dir)

    # Test Spawn
    result = spawn_writer("Cyberpunk", writer_name, "Analytical and bold")
    assert result is True
    assert os.path.exists(target_dir)
    assert os.path.exists(os.path.join(target_dir, "agent.md"))
    
    with open(os.path.join(target_dir, "agent.md"), "r") as f:
        content = f.read()
        assert "Cyberpunk" in content
        assert writer_name in content

    with open(os.path.join(target_dir, "SOUL.md"), "r") as f:
        soul_content = f.read()
        assert "Analytical and bold" in soul_content

    # Test Kill
    result_kill = kill_writer(writer_name)
    assert result_kill is True
    assert not os.path.exists(target_dir)
    assert os.path.exists(archive_dir)

    # Cleanup after test
    shutil.rmtree(archive_dir)
