# AI-Powered Document Processing Suite

A collection of AI applications for document processing, transcript analysis, and presentation generation.

## Applications

### [OpenAI Transcript to Slides](./openai/)
Convert meeting transcripts into professional PowerPoint presentations with AI-generated visuals.

**Features:**
- Smart transcript analysis with GPT-4o-mini
- Automated slide generation
- DALL-E 3 image creation
- Performance timing metrics

**Quick Start:**
```bash
cd openai
pip install -r requirements.txt
streamlit run app.py
```

## Global Setup

### Prerequisites
- Python 3.8+
- OpenAI API key

### Environment Configuration
1. Copy `.env.example` to `.env` (if available)
2. Add your API keys:
```env
OPENAI_API_KEY=your-api-key-here
```

**See [ENV_GUIDE.md](./ENV_GUIDE.md) for detailed environment variable management across folders**

### Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Repository Structure

```
transcript_to_powerpoint/
├── .env                    # Shared environment variables
├── .gitignore             # Global ignore patterns
├── README.md              # This file
├── openai/                # OpenAI-based transcript processor
│   ├── .env              # App-specific environment (optional)
│   ├── app.py            # Main Streamlit application
│   ├── requirements.txt  # Dependencies
│   ├── ARCHITECTURE.md   # Technical documentation
│   └── README.md         # App-specific guide
└── [future apps]/        # Additional AI applications
```

## Adding New Applications

1. **Create App Directory:**
   ```bash
   mkdir new-app-name
   cd new-app-name
   ```

2. **App Structure:**
   ```
   new-app-name/
   ├── .env              # App-specific config (optional)
   ├── app.py            # Main application
   ├── requirements.txt  # Dependencies
   └── README.md         # Documentation
   ```

3. **Environment Variables:**
   - Use root `.env` for shared variables (API keys)
   - Create app `.env` only for app-specific settings

## Development Guidelines

### Environment Variables
- **Root `.env`**: Shared across all apps (API keys, global settings)
- **App `.env`**: App-specific overrides or additional variables
- Load order: App `.env` overrides root `.env`

### Dependencies
- Each app has its own `requirements.txt`
- Keep dependencies minimal and app-specific
- Document any special installation requirements

### Documentation
- Each app must have its own README.md
- Include quick start, features, and usage examples
- Technical details go in ARCHITECTURE.md (if complex)

## Contributing

1. Create new apps in separate directories
2. Follow the established structure
3. Include proper documentation
4. Test with sample data before committing

## License

[Specify your license here]
