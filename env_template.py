# Environment Setup Templates
# Choose one of these approaches for your new app

# =============================================================================
# OPTION 1: Shared Utility (Recommended)
# =============================================================================
"""
# Copy these 3 lines to any new app:

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from env_utils import setup_env

# One-liner setup with validation
setup_env(["OPENAI_API_KEY", "OTHER_REQUIRED_VARS"])

# Then use environment variables normally
api_key = os.getenv("OPENAI_API_KEY")
"""

# =============================================================================
# OPTION 2: Import Specific Functions
# =============================================================================
"""
# For more control over the process:

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from env_utils import load_env_files, validate_required_env, debug_env

# Optional: debug environment setup
debug_env()

# Load environment files
load_env_files()

# Validate required variables
validate_required_env(["OPENAI_API_KEY"])

# Use variables
api_key = os.getenv("OPENAI_API_KEY")
"""

# =============================================================================
# OPTION 3: Copy Function to App (Manual)
# =============================================================================

import os
from pathlib import Path

def load_env_files():
    """
    Load environment variables from both root and app-specific .env files
    
    Loading order (priority):
    1. System environment (highest)
    2. App-specific .env (overrides root)
    3. Root .env (shared defaults)
    """
    try:
        from dotenv import load_dotenv
        
        # Load root .env first (shared settings)
        root_env = Path(__file__).parent.parent / '.env'
        if root_env.exists():
            load_dotenv(root_env)
            print(f"Loaded root .env from: {root_env}")
        else:
            print(f"Root .env not found at: {root_env}")
        
        # Load app-specific .env (overrides root)
        app_env = Path(__file__).parent / '.env'
        if app_env.exists():
            load_dotenv(app_env, override=True)
            print(f"Loaded app .env from: {app_env}")
        else:
            print(f"No app-specific .env at: {app_env}")
            
    except ImportError:
        print("python-dotenv not installed, using system environment only")
        print("   Install with: pip install python-dotenv")

def validate_required_env(required_vars):
    """
    Validate that required environment variables are set
    
    Args:
        required_vars (list): List of required environment variable names
        
    Raises:
        ValueError: If any required variables are missing
    """
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print(f"Missing required environment variables: {missing}")
        print("\nPlease check:")
        print("1. Root .env file has the required variables")
        print("2. Variables are spelled correctly")
        print("3. No extra spaces around variable names")
        raise ValueError(f"Missing required environment variables: {missing}")
    
    print(f"All required environment variables found: {required_vars}")

# Example usage in your app:
if __name__ == "__main__":
    # Load environment files
    load_env_files()
    
    # Validate required variables for your app
    validate_required_env(["OPENAI_API_KEY"])
    
    # Use environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    debug_mode = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"API Key loaded: {'Yes' if api_key else 'No'}")
    print(f"Debug mode: {debug_mode}")
