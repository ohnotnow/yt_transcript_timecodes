# YouTube Video Transcription and Segmentation

This project provides a Python script that downloads a YouTube video, transcribes the audio using OpenAI's Whisper model, and segments the transcript into logical sections based on topics discussed, using OpenAI's GPT-4o model for use as timecodes.

## Features

- **Download YouTube Audio**: Extracts the audio from a YouTube video and converts it to MP3.
- **Transcription**: Transcribes the audio to text using the Whisper model.
- **Segmentation**: Groups the transcript into segments based on topics using GPT-4o.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <your-github-repo-url>
   cd <your-repo-directory>
   ```

2. **Install the required dependencies**:
   ```bash
   python -mvenv venv
   source venv/bin/activate
   pip install yt_dlp openai
   ```

3. **Set up OpenAI API Key**:
   Ensure you have your OpenAI API key set up in your environment:
   ```bash
   export OPENAI_API_KEY='sk-.....'
   ```

## Usage

To use the script, simply run it with the YouTube video URL as an argument:

```bash
python main.py <youtube-video-url>
```

### Example Output

The final segmented JSON file will have the following structure:

```json
{
    "segments": [
        {
            "start": "00:00:00",
            "end": "00:01:00",
            "title": "Introduction"
        },
        {
            "start": "00:01:00",
            "end": "00:02:00",
            "title": "Main Topic 1"
        },
        ...
    ]
}
```

## Notes

- Ensure that you have the necessary API keys and permissions to use OpenAI's Whisper and GPT-4o models.
- The script handles existing transcripts and segments, skipping steps if files are already present.

## Contributing

Feel free to submit issues or pull requests if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License.
