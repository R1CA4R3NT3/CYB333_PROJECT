import paramiko
import time
import logging
import argparse
from datetime import datetime
from pathlib import Path

# Setup logging
log_filename = f"firewall_setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# CLI Argument: --dry-run
parser = argparse.ArgumentParser(description="Automate firewall setup on remote servers via SSH.")
parser.add_argument('--dry-run', action='store_true', help="Simulate actions without executing commands")
args = parser.parse_args()

# Load server list
def load_servers(file_path="servers.txt"):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logging.error(f"Server list file '{file_path}' not found.")
        return []

# SSH credentials
username = "PROJECTADMIN"
private_key_paths = [
    Path(r"C:\Users\jonat\OneDrive\Desktop\National University\CYB 333 Security Automation\Project\PROJECTKEY.pem"),
]

# Firewall commands
firewall_cmds = [
    "ufw allow 22",
    "ufw allow 80",
    "ufw allow 443",
    "ufw --force enable"
]

# Attempt connection with key fallback
def connect_with_retry(host, retries=3, delay=5):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for attempt in range(1, retries + 1):
        for key_path in private_key_paths:
            if not key_path.exists():
                continue
            try:
                pkey = paramiko.RSAKey.from_private_key_file(str(key_path))
                ssh.connect(
                    hostname=host,
                    username=username,
                    pkey=pkey,
                    timeout=10,
                    allow_agent=False,
                    look_for_keys=False
                )
                logging.info(f"Connected to {host} using key: {key_path.name}")
                return ssh
            except Exception as e:
                logging.warning(f"Attempt {attempt}: Failed with key {key_path.name}: {e}")
        time.sleep(delay * attempt)
    return None

# Apply or simulate firewall rules
def apply_firewall_rules(host):
    logging.info(f"Preparing firewall setup on {host}")
    if args.dry_run:
        logging.info(f"[Dry Run] Would attempt SSH to {host} and apply: {', '.join(firewall_cmds)}")
        return

    ssh = connect_with_retry(host)
    if ssh:
        try:
            for cmd in firewall_cmds:
                stdin, stdout, stderr = ssh.exec_command(f"sudo {cmd}")
                out = stdout.read().decode().strip()
                err = stderr.read().decode().strip()
                if out:
                    logging.info(f"{host}: {cmd} => {out}")
                if err:
                    logging.error(f"{host}: {cmd} => ERROR: {err}")
            logging.info(f"Completed firewall setup on {host}")
        finally:
            ssh.close()
    else:
        logging.error(f"Failed to connect to {host} after multiple attempts with all keys.")

# Main entry point
if __name__ == "__main__":
    servers = load_servers()
    if not servers:
        print("No servers found. Ensure 'servers.txt' contains valid hostnames or IPs.")
    for server in servers:
        apply_firewall_rules(server)

    print(f"Firewall setup {'simulated' if args.dry_run else 'completed'}. See log: {log_filename}")

# End of file
