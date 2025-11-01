# Vidsnap-AI 🎬

An AI-powered Instagram Reel generator that transforms your images into engaging video reels with AI-generated voiceovers.

## Features

- 📸 **Multi-Image Upload**: Upload multiple images to create dynamic reels
- 🎙️ **AI Voiceover**: Convert text descriptions to natural-sounding audio using ElevenLabs
- 🎬 **Auto Video Generation**: Automatically combines images and audio into Instagram-ready reels
- 🖼️ **Gallery View**: Browse all generated reels in a beautiful gallery
- 🎨 **Responsive Design**: Works perfectly on desktop and mobile devices

## Prerequisites

- Python 3.9+
- FFmpeg
- ElevenLabs API Key

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Vidsnap-AI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your ElevenLabs API key
   ```

4. **Run the application**
   ```bash
   # Start the web server
   python main.py
   
   # In another terminal, start the background processor
   python generate_process.py
   ```

5. **Visit the application**
   Open http://localhost:5000 in your browser

## Deployment Options

### Option 1: Heroku
1. Install Heroku CLI
2. Create a new Heroku app
3. Add the FFmpeg buildpack:
   ```bash
   heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
   ```
4. Set environment variables:
   ```bash
   heroku config:set ELEVENLABS_API_KEY=your_api_key_here
   heroku config:set FLASK_ENV=production
   ```
5. Deploy:
   ```bash
   git push heroku main
   ```

### Option 2: Railway
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push

### Option 3: Docker
```bash
# Build the image
docker build -t vidsnap-ai .

# Run the container
docker run -p 5000:5000 -e ELEVENLABS_API_KEY=your_key vidsnap-ai
```

### Option 4: VPS (Ubuntu/Debian)
```bash
# Install FFmpeg
sudo apt update && sudo apt install ffmpeg

# Install Python dependencies
pip install -r requirements.txt

# Use gunicorn for production
gunicorn --bind 0.0.0.0:5000 main:app
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ELEVENLABS_API_KEY` | Your ElevenLabs API key | Yes |
| `FLASK_ENV` | Set to `production` for production | No |
| `SECRET_KEY` | Flask secret key for sessions | No |
| `PORT` | Port number (default: 5000) | No |

## How It Works

1. **Upload**: Users upload images and provide a text description
2. **Audio Generation**: Text is converted to speech using ElevenLabs AI
3. **Video Processing**: FFmpeg combines images and audio into a reel
4. **Gallery**: Generated reels are displayed in the gallery

## File Structure

```
Vidsnap-AI/
├── main.py              # Flask web application
├── generate_process.py  # Background video processor
├── text_to_audio.py     # ElevenLabs integration
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── Procfile             # Process definitions for deployment
├── Dockerfile           # Docker configuration
├── templates/           # HTML templates
├── static/              # CSS, JS, and generated content
└── user_uploads/        # Uploaded files (temporary)
```

## API Endpoints

- `GET /` - Homepage
- `GET /create` - Upload form
- `POST /create` - Handle file uploads
- `GET /gallery` - View generated reels

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue on GitHub or contact [your-email].

---

Made with ❤️ using Flask and AI