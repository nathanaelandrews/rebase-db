#!/usr/bin/env python3
"""
Update REBASE Database - Check for new versions and update enzyme database
"""
import re
import urllib.request
import os
from datetime import datetime

REBASE_URL = "http://rebase.neb.com/rebase/link_allenz"
DATA_DIR = "data"
ALLENZ_FILE = os.path.join(DATA_DIR, "allenz.txt")
VERSION_FILE = os.path.join(DATA_DIR, "current_version.txt")
OUTPUT_FILE = "enzymes.tsv"

def get_rebase_version_from_header():
    """Get REBASE version by downloading just the first few lines"""
    try:
        # Download just first 1024 bytes to get header
        req = urllib.request.Request(REBASE_URL)
        with urllib.request.urlopen(req) as response:
            header = response.read(1024).decode('utf-8')
            
        # Look for "REBASE version XXX"
        match = re.search(r'REBASE version (\d+)', header)
        if match:
            return int(match.group(1))
        else:
            print("Debug: Header content:")
            print(header[:200])
            return None
    except Exception as e:
        print(f"Error checking remote version: {e}")
        return None

def get_rebase_version_from_file(filepath):
    """Extract REBASE version number from downloaded file"""
    try:
        with open(filepath, 'r') as f:
            # Read first few lines to find version
            for i in range(10):  # Check first 10 lines
                line = f.readline().strip()
                if not line:
                    break
                match = re.search(r'REBASE version (\d+)', line)
                if match:
                    return int(match.group(1))
        return None
    except FileNotFoundError:
        return None

def get_current_local_version():
    """Get currently stored version number"""
    try:
        with open(VERSION_FILE, 'r') as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return None

def save_current_version(version):
    """Save current version number to file"""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(VERSION_FILE, 'w') as f:
        f.write(str(version))

def download_rebase_file():
    """Download complete REBASE file"""
    print("Downloading complete REBASE data...")
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        urllib.request.urlretrieve(REBASE_URL, ALLENZ_FILE)
        print(f"Downloaded to {ALLENZ_FILE}")
        return True
    except Exception as e:
        print(f"Error downloading REBASE file: {e}")
        return False

def check_for_updates():
    """Check if REBASE has been updated"""
    
    # Get current local version
    local_version = get_current_local_version()
    print(f"Local version: {local_version if local_version else 'None'}")
    
    # Check remote version (just header)
    remote_version = get_rebase_version_from_header()
    print(f"Remote version: {remote_version if remote_version else 'Unknown'}")
    
    if remote_version is None:
        print("Warning: Could not determine remote version, forcing update")
        return True
    
    # Check if update is needed
    if local_version is None or remote_version > local_version:
        print(f"Update needed: {local_version} -> {remote_version}")
        return True, remote_version
    else:
        print("Database is up to date")
        return False, remote_version

def run_parser():
    """Run the main parser script"""
    print("Running parser to update enzyme database...")
    
    # Import and run the parser (assuming parse_rebase.py is in same directory)
    try:
        import parse_rebase
        
        # Parse enzymes
        enzymes = parse_rebase.parse_rebase_file(ALLENZ_FILE)
        print(f"Parsed {len(enzymes)} valid commercial restriction enzymes")
        
        # Create database
        enzyme_db = parse_rebase.create_enzyme_database(enzymes)
        
        # Write output
        parse_rebase.write_tsv_output(enzyme_db, OUTPUT_FILE)
        print(f"Updated database written to {OUTPUT_FILE}")
        
        return True
        
    except Exception as e:
        print(f"Error running parser: {e}")
        return False

def main():
    """Main update workflow"""
    
    print("REBASE Database Updater")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check for updates (just header check)
    needs_update, remote_version = check_for_updates()
    
    if needs_update:
        # Download complete file
        if download_rebase_file():
            # Verify version from downloaded file
            downloaded_version = get_rebase_version_from_file(ALLENZ_FILE)
            print(f"Downloaded file version: {downloaded_version}")
            
            # Run parser to update database
            if run_parser():
                # Save new version number
                version_to_save = downloaded_version or remote_version
                if version_to_save:
                    save_current_version(version_to_save)
                    print(f"Successfully updated to version {version_to_save}")
                else:
                    print("Warning: Could not determine version to save")
            else:
                print("Failed to update database")
                return 1
        else:
            print("Failed to download REBASE file")
            return 1
    else:
        print("No update needed")
    
    print("Update check complete")
    return 0

if __name__ == "__main__":
    exit(main())
