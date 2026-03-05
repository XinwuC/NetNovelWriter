#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("manage_writer")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AGENTS_DIR = os.path.join(BASE_DIR, "agents")
TEMPLATE_DIR = os.path.join(AGENTS_DIR, "nnw_writer_template")

def spawn_writer(theme, writer_name, personality):
    logger.info(f"Spawning Writer Agent '{writer_name}' with theme '{theme}'...")
    target_dir = os.path.join(AGENTS_DIR, f"nnw_writer_{writer_name}")
    
    if os.path.exists(target_dir):
        logger.error(f"Writer agent directory {target_dir} already exists.")
        return False
        
    try:
        shutil.copytree(TEMPLATE_DIR, target_dir)
        
        # Replace template variables
        agent_md_path = os.path.join(target_dir, "agent.md")
        with open(agent_md_path, "r") as f:
            content = f.read()
        content = content.replace("{{theme}}", theme).replace("{{writer_name}}", writer_name)
        with open(agent_md_path, "w") as f:
            f.write(content)
            
        soul_md_path = os.path.join(target_dir, "SOUL.md")
        with open(soul_md_path, "r") as f:
            soul_content = f.read()
        soul_content = soul_content.replace("{{personality}}", personality)
        with open(soul_md_path, "w") as f:
            f.write(soul_content)

        logger.info(f"Writer '{writer_name}' workspace created at {target_dir}")
        print(json.dumps({"status": "success", "writer_name": writer_name, "message": "Workspace created successfully", "path": target_dir}))
        
        # In a real environment, we'd launch the agent here:
        # subprocess.Popen(["openclaw", "start", target_dir])
        return True
    except Exception as e:
        logger.error(f"Failed to spawn writer: {e}")
        print(json.dumps({"status": "error", "message": str(e)}))
        return False

def kill_writer(writer_name):
    logger.info(f"Terminating and archiving Writer Agent '{writer_name}'...")
    target_dir = os.path.join(AGENTS_DIR, f"nnw_writer_{writer_name}")
    
    if not os.path.exists(target_dir):
        logger.error(f"Writer agent directory {target_dir} does not exist.")
        print(json.dumps({"status": "error", "message": "Agent not found"}))
        return False
        
    try:
        # In a real environment, we'd stop the process first:
        # subprocess.run(["openclaw", "stop", f"nnw_writer_{writer_name}"])
        archive_dir = os.path.join(AGENTS_DIR, f"archive_nnw_writer_{writer_name}")
        shutil.move(target_dir, archive_dir)
        logger.info(f"Writer '{writer_name}' archived to {archive_dir}")
        print(json.dumps({"status": "success", "writer_name": writer_name, "message": "Agent archived successfully"}))
        return True
    except Exception as e:
        logger.error(f"Failed to kill writer: {e}")
        print(json.dumps({"status": "error", "message": str(e)}))
        return False

def main():
    parser = argparse.ArgumentParser(description="Skill: Manage OpenClaw Writer Agents")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    spawn_parser = subparsers.add_parser("spawn", help="Spawn a new writer agent")
    spawn_parser.add_parser("theme", help="The novel theme")
    spawn_parser.add_argument("--theme", required=True, help="Theme for the novel")
    spawn_parser.add_argument("--name", required=True, help="Unique name for the writer agent")
    spawn_parser.add_argument("--personality", default="Analytical and serious", help="Personality description for SOUL.md")
    
    kill_parser = subparsers.add_parser("kill", help="Terminate an existing writer agent")
    kill_parser.add_argument("--name", required=True, help="Unique name of the writer agent to kill")
    
    args = parser.parse_args()
    
    if args.command == "spawn":
        spawn_writer(args.theme, args.name, args.personality)
    elif args.command == "kill":
        kill_writer(args.name)

if __name__ == "__main__":
    main()
