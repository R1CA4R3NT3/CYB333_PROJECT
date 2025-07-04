CYB333 PROJECT 

Server Firewall Configuration Automation 

This script is designed to automate the setup of firewall rules on one or more remote Linux servers using SSH key-based authentication. Its core objective is to streamline the process of securing SSH and web access ports by applying ufw (Uncomplicated Firewall) rules remotely.

Script Objectives
- Connect to each server listed in servers.txt via SSH
- Apply standardized firewall rules using sudo ufw
- Support multiple private key paths for SSH authentication fallback
- Provide detailed logging of all operations for audit and troubleshooting

Key Features
- SSH Key Authentication      - Uses one or more .pem or private key files to securely log in to remote machines without passwords. 
- Retry Mechanism             - Attempts multiple retries per host and private key, with exponential backoff if a connection fails.  
- Logging                     - Writes structured logs with timestamps to a firewall_setup_<timestamp>.log file.  
- Firewall Enforcement        - Applies the following commands on each host:<br>ufw allow 22, ufw allow 80, ufw allow 443, and ufw --force enable  
- Dry-Run Mode                - With --dry-run, it logs what would be done without executing any SSH commands. 
- Modular & Scalable          - Reads hostnames/IPs from a text file; easy to extend across dozens of servers.  

Setup Instructions
1. Install the following prerequisites and dependencies;
	-Make sure Python 3.6+ is installed. Then install the required Python libraries:
		paramiko, time, logging, argparse, pyufw, datetime, path          
2. Prepare SSH Keys
3. Ensure private key files exist and are accessible:
	They must match public keys added to the remote servers’ `~/.ssh/authorized_keys` files. 
4. Create servers.txt (This file should be in the same directory as your script and contain one IP address or hostname per line)
5. Make sure each host:
- Is online and reachable over SSH (port 22)
- Has your public key authorized
- Allows `sudo ufw` commands
6. **Configure Your Username**
	Edit the line in your script:
	python - username = "your_ssh_user"
	Change `"your_ssh_user"` to match the user allowed to log in via SSH, such as `azureuser`, `ubuntu`, or `ec2-user`.

How to Run the Script

From the terminal:  AUTO_MULTI_SERVER_FRWL_MGR.py

