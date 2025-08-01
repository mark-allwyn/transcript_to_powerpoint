# OpenAI Transcript to Slides App

AI-powered application that converts meeting transcripts into professional PowerPoint presentations using OpenAI's structured output and DALL-E 3.

## Quick Start

1. **Setup Environment**:
   ```bash
   cd openai
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   - Copy the `OPENAI_API_KEY` from the root `.env` file
   - Or set app-specific key in `openai/.env`

3. **Run Application**:
   ```bash
   streamlit run app.py
   ```

## Features

- **Smart Transcript Analysis**: Extracts key points, decisions, and action items
- **Automated Slide Generation**: Creates professional slide decks
- **AI-Generated Visuals**: Contextual business illustrations with DALL-E 3
- **Performance Tracking**: Detailed timing for each processing step

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed technical documentation.

## Usage

1. Upload a meeting transcript (.txt file)
2. Wait for AI processing (45-90 seconds typical)
3. Review timing metrics
4. Download your PowerPoint presentation

## API Costs

- Approximately $0.10-0.25 per presentation
- Breakdown: GPT analysis + DALL-E images

## Configuration

Environment variables (use root `.env` or app-specific `openai/.env`):
- `OPENAI_API_KEY`: Required for all AI operations
