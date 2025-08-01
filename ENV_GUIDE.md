# Environment Variable Management Guide

This guide explains how to use `.env` variables across multiple app folders in this repository.

## Environment File Structure

```
transcript_to_powerpoint/
├── .env                    # SHARED variables (API keys, global settings)
├── openai/
│   ├── .env               # APP-SPECIFIC overrides (optional)
│   └── app.py             # Loads both .env files
└── claude/                # Future app example
    ├── .env               # APP-SPECIFIC overrides (optional)  
    └── app.py             # Loads both .env files
```

## How It Works

### 1. Loading Order (Priority)
1. **System Environment** (highest priority)
2. **App `.env`** (overrides root)
3. **Root `.env`** (default/shared values)

### 2. Using Shared Environment Utilities (Recommended)
The easiest way is to use the shared `env_utils.py` module:

```python
# At the top of any app
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from env_utils import setup_env

# One-liner setup with validation
setup_env(["OPENAI_API_KEY"])

# Then use environment variables normally
api_key = os.getenv("OPENAI_API_KEY")
```

### 3. Manual Loading Function (Alternative)
If you prefer to copy the function to each app:

```python
from pathlib import Path

def load_env_files():
    """Load environment variables from root and app-specific .env files"""
    try:
        from dotenv import load_dotenv
        
        # Load root .env first (shared settings)
        root_env = Path(__file__).parent.parent / '.env'
        if root_env.exists():
            load_dotenv(root_env)
        
        # Load app-specific .env (overrides root)
        app_env = Path(__file__).parent / '.env'
        if app_env.exists():
            load_dotenv(app_env, override=True)
            
    except ImportError:
        # dotenv not available, rely on system environment
        pass

# Call this at the start of your app
load_env_files()

# Then use environment variables normally
api_key = os.getenv("OPENAI_API_KEY")
```

## Best Practices

### Root `.env` (Shared Variables)
Put shared settings here:
```env
# Root .env - Shared across all apps
OPENAI_API_KEY=sk-your-shared-openai-key
DEBUG=false
LOG_LEVEL=INFO

# Database settings (if shared)
DATABASE_URL=postgresql://localhost/shared_db

# Common API endpoints
API_BASE_URL=https://api.company.com
```

### App-Specific `.env` (Overrides)
Only create app `.env` for app-specific settings:
```env
# openai/.env - OpenAI app specific
DEBUG=true
MODEL_OVERRIDE=gpt-4o
MAX_TOKENS=4000

# claude/.env - Claude app specific  
DEBUG=true
MODEL_OVERRIDE=claude-3-opus
ANTHROPIC_API_KEY=sk-ant-your-claude-key
```

## Practical Examples

### Example 1: Shared API Key
**Root `.env`:**
```env
OPENAI_API_KEY=sk-shared-key-for-all-apps
```

**All apps can use:**
```python
load_env_files()
api_key = os.getenv("OPENAI_API_KEY")  # Gets shared key
```

### Example 2: App-Specific Override
**Root `.env`:**
```env
OPENAI_API_KEY=sk-shared-key
MODEL=gpt-4o-mini
```

**openai/.env:**
```env
MODEL=gpt-4o  # Override to use stronger model
```

**App usage:**
```python
load_env_files()
api_key = os.getenv("OPENAI_API_KEY")  # Gets shared key
model = os.getenv("MODEL")             # Gets app-specific override (gpt-4o)
```

### Example 3: Multiple AI Providers
**Root `.env`:**
```env
# Shared keys
OPENAI_API_KEY=sk-openai-key
ANTHROPIC_API_KEY=sk-claude-key
```

**openai/app.py:**
```python
load_env_files()
openai_key = os.getenv("OPENAI_API_KEY")    # Uses shared key
# anthropic_key is available but not used
```

**claude/app.py:**
```python
load_env_files()  
anthropic_key = os.getenv("ANTHROPIC_API_KEY")  # Uses shared key
# openai_key is available but not used
```

## 🔒 Security Best Practices

### 1. Git Ignore
Ensure `.env` files are ignored:
```gitignore
# In root .gitignore
.env
*/.env
**/.env
```

### 2. Environment Templates
Create `.env.example` files:
```env
# .env.example (root)
OPENAI_API_KEY=your-openai-api-key-here
DEBUG=false

# openai/.env.example  
MODEL_OVERRIDE=gpt-4o-mini
MAX_TOKENS=2000
```

### 3. Environment Validation
Add validation in your apps:
```python
def validate_env():
    """Validate required environment variables"""
    required_vars = ["OPENAI_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        raise ValueError(f"Missing required environment variables: {missing}")

load_env_files()
validate_env()
```

## Three Ways to Use Environment Variables

### Option 1: Shared Utility (Recommended)
```python
# Clean and simple - just 3 lines!
import sys; sys.path.append(str(Path(__file__).parent.parent))
from env_utils import setup_env
setup_env(["OPENAI_API_KEY"])
```

### Option 2: Import Functions
```python
# More control over the process
from env_utils import load_env_files, validate_required_env
load_env_files()
validate_required_env(["OPENAI_API_KEY"])
```

### Option 3: Copy Function (Manual)
```python
# Copy the function to each app (more code duplication)
def load_env_files():
    # ... full function code
```

## Practical Examples (Updated)

### Example 1: Simple App Setup
```python
# new-app/app.py
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from env_utils import setup_env

# One line does everything!
setup_env(["OPENAI_API_KEY"])

# Use variables
api_key = os.getenv("OPENAI_API_KEY")
```

### Example 2: Multiple Variables with Debug
```python
# app.py  
from env_utils import setup_env

# Setup with multiple required vars and debug info
setup_env(["OPENAI_API_KEY", "DATABASE_URL"], debug=True)
```

### Example 3: Advanced Control
### Example 3: Advanced Control
```python
# More granular control
from env_utils import load_env_files, validate_required_env, debug_env

# Debug if needed
debug_env()

# Load environment files
load_env_files()

# Custom validation with better error handling
try:
    validate_required_env(["OPENAI_API_KEY"])
except ValueError as e:
    print(f"Environment setup failed: {e}")
    exit(1)

# Use variables
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL", "gpt-4o-mini")  # Default fallback
```

## Checklist for New Apps

When creating a new app:

- [ ] Import shared env utilities: `from env_utils import setup_env`
- [ ] Call `setup_env(["REQUIRED_VARS"])` at the top of your app
- [ ] Add `python-dotenv` to app's `requirements.txt`
- [ ] Document required environment variables in app README
- [ ] Create `.env.example` if app has specific variables
- [ ] Test that app works with only root `.env`

**Super Quick Setup:**
```python
# Top of any new app.py
import sys; sys.path.append(str(Path(__file__).parent.parent))
from env_utils import setup_env
setup_env(["OPENAI_API_KEY"])  # Add your required vars here
```

## 🐛 Troubleshooting

### Problem: Variables Not Loading
```python
# Debug environment loading
def debug_env():
    print("Current working directory:", os.getcwd())
    print("Script location:", Path(__file__).parent)
    print("Root .env path:", Path(__file__).parent.parent / '.env')
    print("App .env path:", Path(__file__).parent / '.env')
    
debug_env()
load_env_files()
```

### Problem: Wrong Values
Check loading order:
```python
# Check what's loaded
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY", "NOT_SET"))
print("DEBUG:", os.getenv("DEBUG", "NOT_SET"))
```

This system gives you maximum flexibility while keeping configuration manageable across multiple AI apps!
