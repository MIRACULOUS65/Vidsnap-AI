#!/bin/bash

# Deployment script for Vidsnap-AI

echo "Setting up Vidsnap-AI deployment..."

# Create necessary directories
mkdir -p user_uploads
mkdir -p static/reels
mkdir -p static/songs

# Install dependencies
pip install -r requirements.txt

echo "Setup complete!"
echo "Don't forget to:"
echo "1. Set your ELEVENLABS_API_KEY environment variable"
echo "2. Install FFmpeg on your system"
echo "3. Set FLASK_ENV=production for production deployment"