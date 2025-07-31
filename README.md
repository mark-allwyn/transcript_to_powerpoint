# Transcript → Slides

An AI-powered Streamlit application that automatically converts meeting transcripts into professional PowerPoint presentations with AI-generated images.

## Features

- **Smart Transcript Analysis**: Uses OpenAI's structured output to extract key points, decisions, and action items from meeting transcripts
- **Automated Slide Generation**: Creates professional slide decks with relevant titles and bullet points
- **AI-Generated Visuals**: Generates contextual business illustrations using DALL-E 3
- **Easy Web Interface**: Simple drag-and-drop file upload via Streamlit
- **Instant Download**: Get your PowerPoint presentation ready in seconds

## How It Works

1. **Upload** a meeting transcript (.txt file)
2. **AI Analysis** extracts key information using GPT-4o-mini
3. **Slide Creation** generates structured slides with titles and bullets
4. **Image Generation** creates relevant business illustrations with DALL-E 3
5. **Download** your complete PowerPoint presentation

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd transcribe_to_slide
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser to `http://localhost:8501`

3. Upload a meeting transcript text file

4. Wait for processing (typically 30-60 seconds)

5. Download your generated PowerPoint presentation

## Dependencies

```
streamlit
openai
python-pptx
pydantic
pillow
requests
```

## Technical Details

### AI Models Used

- **GPT-4o-mini**: For transcript analysis and slide content generation
- **GPT-4o**: For creating detailed image prompts
- **DALL-E 3**: For generating professional business illustrations

### Structured Output

The application uses OpenAI's structured output feature with Pydantic models to ensure reliable and consistent results:

- `MeetingSummary`: Extracts key points, decisions, and action items
- `SlideSpecs`: Defines slide titles and bullet points
- `ImagePrompts`: Generates contextual DALL-E prompts

### Slide Generation Process

1. **Analysis Phase**: Extract structured information from transcript
2. **Content Phase**: Create slide specifications with titles and bullets
3. **Visual Phase**: Generate relevant image prompts based on content
4. **Assembly Phase**: Combine text and images into PowerPoint format

## Example Output

The application generates:

- **Title slide** with meeting summary
- **Content slides** covering:
  - Key discussion points
  - Decisions made
  - Action items identified
- **Professional visuals** relevant to meeting topics

## Error Handling

The application includes robust fallback mechanisms:

- If AI analysis fails, creates basic slides from available content
- If image generation fails, uses clean placeholder images
- Graceful handling of API rate limits and timeouts

## Customization

### Slide Content
Modify the prompt templates in `generate_slide_package()` to adjust:
- Number of bullet points per slide
- Slide title formats
- Content structure

### Visual Style
Adjust image generation prompts to change:
- Color schemes (default: blue/gray/white)
- Illustration style (default: minimalist business)
- Visual complexity

### Output Format
The PowerPoint template can be customized by modifying the `build_pptx()` function.

## Troubleshooting

### Common Issues

1. **"No module named 'openai'"**
   - Run `pip install -r requirements.txt`

2. **API key errors**
   - Verify your OpenAI API key is set correctly
   - Check your OpenAI account has sufficient credits

3. **Image generation fails**
   - The app will use placeholder images if DALL-E fails
   - Check OpenAI API status if persistent

4. **Long processing times**
   - Large transcripts take longer to process
   - Image generation can take 30-60 seconds

### Debug Mode

The application includes debug print statements that show:
- Summary extraction results
- Number of slides generated
- Image prompt creation status

## API Costs

Approximate costs per transcript (varies by length):
- GPT-4o-mini analysis: ~$0.01-0.05
- DALL-E 3 images: ~$0.04 per image
- Total: ~$0.10-0.25 per presentation

## License

[Specify your license here]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues or questions:
- Create an issue in this repository
- Check the troubleshooting section above
- Verify your OpenAI API key and credits

## Changelog

### v1.0.0
- Initial release with OpenAI structured output
- DALL-E 3 image generation
- Streamlit web interface
- PowerPoint export functionality
