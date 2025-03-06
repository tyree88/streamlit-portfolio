#!/usr/bin/env python3
"""
Script to update the Python environment using uv package manager
based on the pyproject.toml file.
"""

import subprocess
import sys
import os
import json
from pathlib import Path

# Define colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def run_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            text=True, 
            capture_output=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}Error executing command: {command}{Colors.ENDC}")
        print(f"{Colors.FAIL}Error message: {e.stderr}{Colors.ENDC}")
        return None

def check_uv_installed():
    """Check if uv is installed and install it if not."""
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        print(f"{Colors.GREEN}uv package manager is installed.{Colors.ENDC}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Colors.WARNING}uv package manager not found. Installing...{Colors.ENDC}")
        try:
            # Install uv using the official installation method
            install_cmd = "curl -LsSf https://astral.sh/uv/install.sh | sh"
            subprocess.run(install_cmd, shell=True, check=True)
            print(f"{Colors.GREEN}uv package manager installed successfully.{Colors.ENDC}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Colors.FAIL}Failed to install uv: {e}{Colors.ENDC}")
            print(f"{Colors.FAIL}Please install uv manually: https://github.com/astral-sh/uv{Colors.ENDC}")
            return False

def get_installed_packages():
    """Get a list of all installed packages using uv."""
    output = run_command("uv pip list --format json")
    if output is None:
        return {}
    
    try:
        packages_json = json.loads(output)
        packages = {pkg['name'].lower(): pkg['version'] for pkg in packages_json}
        return packages
    except json.JSONDecodeError:
        print(f"{Colors.FAIL}Failed to parse installed packages.{Colors.ENDC}")
        return {}

def main():
    print(f"{Colors.HEADER}Starting environment update with uv...{Colors.ENDC}")
    
    # Check if uv is installed
    if not check_uv_installed():
        return
    
    # Check if pyproject.toml exists
    if not Path("pyproject.toml").exists():
        print(f"{Colors.FAIL}pyproject.toml not found in the current directory.{Colors.ENDC}")
        return
    
    # Get installed packages
    print(f"{Colors.BLUE}Getting installed packages...{Colors.ENDC}")
    installed_packages = get_installed_packages()
    print(f"{Colors.GREEN}Found {len(installed_packages)} installed packages.{Colors.ENDC}")
    
    # Install dependencies from pyproject.toml
    print(f"{Colors.BLUE}Installing dependencies from pyproject.toml...{Colors.ENDC}")
    result = run_command("uv pip install -e .")
    
    if result is not None:
        print(f"{Colors.GREEN}Dependencies installed successfully!{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}Failed to install dependencies.{Colors.ENDC}")
        return
    
    # Identify unused packages
    print(f"{Colors.BLUE}Checking for unused packages...{Colors.ENDC}")
    
    # Get the list of required packages from pyproject.toml
    # This is a simplified approach - in a real scenario, you might want to parse the TOML file properly
    required_output = run_command("grep -A 100 'dependencies = \\[' pyproject.toml | grep -v '#' | grep '\"' | sed 's/[^\"]*\"\\([^\"]*\\).*/\\1/g' | sed 's/>.*//g'")
    if required_output is None:
        print(f"{Colors.WARNING}Could not determine required packages from pyproject.toml.{Colors.ENDC}")
        return
    
    required_packages = [pkg.strip().lower() for pkg in required_output.split('\n') if pkg.strip()]
    
    # Find packages to uninstall
    to_uninstall = []
    for package in installed_packages:
        # Skip packages that start with streamlit- as they might be dependencies
        if package.startswith('streamlit-') and package not in required_packages:
            print(f"{Colors.WARNING}Skipping potential Streamlit dependency: {package}{Colors.ENDC}")
            continue
            
        if package not in required_packages:
            # Skip some common development packages
            if package in ['pip', 'setuptools', 'wheel', 'uv']:
                continue
            to_uninstall.append(package)
    
    # Uninstall unused packages
    if to_uninstall:
        print(f"{Colors.BLUE}Found {len(to_uninstall)} unused packages:{Colors.ENDC}")
        for package in to_uninstall:
            print(f"  - {package}")
        
        confirm = input(f"{Colors.WARNING}Do you want to uninstall these packages? (y/n): {Colors.ENDC}")
        if confirm.lower() == 'y':
            for package in to_uninstall:
                print(f"{Colors.BLUE}Uninstalling {package}...{Colors.ENDC}")
                run_command(f"uv pip uninstall -y {package}")
            print(f"{Colors.GREEN}Unused packages uninstalled successfully!{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}Skipping uninstallation.{Colors.ENDC}")
    else:
        print(f"{Colors.GREEN}No unused packages found.{Colors.ENDC}")
    
    # Generate lock file for reproducibility
    print(f"{Colors.BLUE}Generating lock file for reproducibility...{Colors.ENDC}")
    run_command("uv pip compile pyproject.toml -o requirements.lock")
    print(f"{Colors.GREEN}Lock file generated: requirements.lock{Colors.ENDC}")
    
    print(f"{Colors.GREEN}Environment update completed successfully!{Colors.ENDC}")

if __name__ == "__main__":
    main() 