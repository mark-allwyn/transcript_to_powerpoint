"""
Shared environment utilities for all apps
-----------------------------------------
This module provides environment loading functionality that can be imported
by any app in the repository.

Usage:
    from env_utils import load_env_files, validate_required_env
    
    load_env_files()
    validate_required_env(["OPENAI_API_KEY"])
"""

import os
from pathlib import Path


def load_env_files(app_path=None):
    """
    Load environment variables from both root and app-specific .env files
    
    Args:
        app_path (str, optional): Path to the app directory. If None, auto-detects
                                 based on caller's location.
    
    Loading order (priority):
    1. System environment (highest)
    2. App-specific .env (overrides root)
    3. Root .env (shared defaults)
    """
    try:
        from dotenv import load_dotenv
        
        # Auto-detect paths if not provided
        if app_path is None:
            # Get the caller's directory (the app calling this function)
            import inspect
            caller_frame = inspect.currentframe().f_back
            caller_file = caller_frame.f_code.co_filename
            app_dir = Path(caller_file).parent
        else:
            app_dir = Path(app_path)
        
        # Load root .env first (shared settings)
        root_env = app_dir.parent / '.env'
        if root_env.exists():
            load_dotenv(root_env)
            print(f"Loaded root .env from: {root_env}")
        else:
            print(f"Root .env not found at: {root_env}")
        
        # Load app-specific .env (overrides root)
        app_env = app_dir / '.env'
        if app_env.exists():
            load_dotenv(app_env, override=True)
            print(f"Loaded app .env from: {app_env}")
        else:
            print(f"No app-specific .env at: {app_env}")
            
    except ImportError:
        print("python-dotenv not installed, using system environment only")
        print("   Install with: pip install python-dotenv")


def validate_required_env(required_vars, show_success=True):
    """
    Validate that required environment variables are set
    
    Args:
        required_vars (list): List of required environment variable names
        show_success (bool): Whether to print success message
        
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
    
    if show_success:
        print(f"All required environment variables found: {required_vars}")


def get_env_info():
    """
    Get information about current environment setup
    
    Returns:
        dict: Environment information
    """
    import inspect
    caller_frame = inspect.currentframe().f_back
    caller_file = caller_frame.f_code.co_filename
    app_dir = Path(caller_file).parent
    
    root_env = app_dir.parent / '.env'
    app_env = app_dir / '.env'
    
    return {
        "app_directory": str(app_dir),
        "root_env_path": str(root_env),
        "root_env_exists": root_env.exists(),
        "app_env_path": str(app_env),
        "app_env_exists": app_env.exists(),
        "working_directory": os.getcwd()
    }


def debug_env():
    """Print debug information about environment setup"""
    info = get_env_info()
    
    print("🔍 Environment Debug Information:")
    print(f"   Working directory: {info['working_directory']}")
    print(f"   App directory: {info['app_directory']}")
    print(f"   Root .env: {info['root_env_path']} ({'Yes' if info['root_env_exists'] else 'No'})")
    print(f"   App .env: {info['app_env_path']} ({'Yes' if info['app_env_exists'] else 'No'})")


# Convenience function for common setup
def setup_env(required_vars=None, debug=False):
    """
    One-liner to set up environment for an app
    
    Args:
        required_vars (list, optional): Required environment variables to validate
        debug (bool): Whether to show debug information
        
    Usage:
        from env_utils import setup_env
        setup_env(["OPENAI_API_KEY"])
    """
    if debug:
        debug_env()
    
    load_env_files()
    
    if required_vars:
        validate_required_env(required_vars)


# Example usage
if __name__ == "__main__":
    print("Testing environment utilities...")
    debug_env()
    load_env_files()
    
    # Test with common variables
    test_vars = ["OPENAI_API_KEY"]
    try:
        validate_required_env(test_vars)
    except ValueError as e:
        print(f"Validation failed: {e}")
