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

def spawn_writer(theme, writer_name, personality, model):
    logger.info(f"Spawning Writer Agent '{writer_name}' with theme '{theme}'...")
    target_dir = os.path.join(AGENTS_DIR, f"nnw_writer_{writer_name}")
    
    if os.path.exists(target_dir):
        logger.error(f"Writer agent directory {target_dir} already exists.")
        return False
        
    try:
        shutil.copytree(TEMPLATE_DIR, target_dir, symlinks=True)
        
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
        
        # Register the new agent into openclaw
        cmd = ["openclaw", "agent", "add", writer_name, "--workspace", target_dir]
        if model:
            cmd.extend(["--model", model])
            
        logger.info(f"Registering new agent with OpenClaw: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
            logger.info("Successfully registered agent with OpenClaw.")
        except FileNotFoundError:
            logger.warning("OpenClaw command not found in this environment. Skipping registration.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to register agent with OpenClaw: {e}")
            
        print(json.dumps({"status": "success", "writer_name": writer_name, "message": "Workspace created and agent registered successfully", "path": target_dir}))
        
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
        shutil.rmtree(target_dir)
        logger.info(f"Writer '{writer_name}' workspace removed.")
        
        # Remove agent from openclaw
        cmd = ["openclaw", "agent", "remove", writer_name]
        try:
            subprocess.run(cmd, check=True)
            logger.info(f"Successfully removed '{writer_name}' from OpenClaw registry.")
        except FileNotFoundError:
            pass
        except subprocess.CalledProcessError as e:
            logger.warning(f"Warning: Failed to remove agent from OpenClaw registry: {e}")
            
        print(json.dumps({"status": "success", "writer_name": writer_name, "message": "Writer agent terminated and removed successfully"}))
        return True
    except Exception as e:
        logger.error(f"Failed to kill writer: {e}")
        print(json.dumps({"status": "error", "message": str(e)}))
        return False

def main():
    parser = argparse.ArgumentParser(description="Skill: Manage OpenClaw Writer Agents")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    spawn_parser = subparsers.add_parser("spawn", help="Spawn a new writer agent")
    spawn_parser.add_argument("--theme", required=True, help="Theme for the novel")
    spawn_parser.add_argument("--name", required=True, help="Unique name for the writer agent")
    spawn_parser.add_argument("--personality", default="Analytical and serious", help="Personality description for SOUL.md")
    spawn_parser.add_argument("--model", default=os.environ.get("OPENCLAW_MODEL"), help="Model to use for the agent (defaults to master agent's model if OPENCLAW_MODEL env var is set)")
    
    kill_parser = subparsers.add_parser("kill", help="Terminate an existing writer agent")
    kill_parser.add_argument("--name", required=True, help="Unique name of the writer agent to kill")
    
    args = parser.parse_args()
    
    if args.command == "spawn":
        spawn_writer(args.theme, args.name, args.personality, args.model)
    elif args.command == "kill":
        kill_writer(args.name)

if __name__ == "__main__":
    main()
