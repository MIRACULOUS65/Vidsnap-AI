#this file looks for new folders inside user uploads and converts them to reel if they are not already converted
import os
from text_to_audio import text_to_speech_file
import time
import subprocess

def ensure_directories():
    """Ensure all required directories exist"""
    os.makedirs("user_uploads", exist_ok=True)
    os.makedirs("static/reels", exist_ok=True)
    os.makedirs("static/songs", exist_ok=True)
    
    # Create done.txt if it doesn't exist
    if not os.path.exists("done.txt"):
        with open("done.txt", "w") as f:
            f.write("")

def text_to_audio(folder):
    print("text_to_audio",folder)
    try:
        with open(f"user_uploads/{folder}/desc.txt") as f:
            text = f.read()
        print(text, folder)
        text_to_speech_file(text, folder)
        return True
    except Exception as e:
        print(f"Error in text_to_audio for {folder}: {e}")
        return False

def create_reel(folder):
    try:
        command = f'''ffmpeg -f concat -safe 0 -i user_uploads/{folder}/input.txt -i user_uploads/{folder}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4'''
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("create_reel", folder, "SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error for {folder}: {e}")
        print(f"FFmpeg stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"Error in create_reel for {folder}: {e}")
        return False

if __name__=="__main__":
    ensure_directories()
    
    while True:
        print("Processing Queue......")
        try:
            with open("done.txt","r") as f:
                done_folders = f.readlines()
        except FileNotFoundError:
            done_folders = []

        done_folders = [f.strip() for f in done_folders] #need coz if the folders are already processed they will not be needed to be processed again
        
        try:
            folders = os.listdir("user_uploads")
        except FileNotFoundError:
            print("user_uploads directory not found, creating...")
            os.makedirs("user_uploads", exist_ok=True)
            folders = []
            
        for folder in folders:
            if folder not in done_folders and os.path.isdir(f"user_uploads/{folder}"):
                print(f"Processing folder: {folder}")
                
                # Check if required files exist
                desc_file = f"user_uploads/{folder}/desc.txt"
                input_file = f"user_uploads/{folder}/input.txt"
                
                if not os.path.exists(desc_file):
                    print(f"Missing desc.txt for {folder}")
                    continue
                    
                if not os.path.exists(input_file):
                    print(f"Missing input.txt for {folder}")
                    continue
                
                # Process the folder
                if text_to_audio(folder): #generate the audio from desc.txt
                    if create_reel(folder): #convert the images and audio.mp3 inside the folder to a reel
                        with open("done.txt","a") as f:
                            f.write(folder+"\n")
                        print(f"Successfully processed {folder}")
                    else:
                        print(f"Failed to create reel for {folder}")
                else:
                    print(f"Failed to create audio for {folder}")
        
        time.sleep(4)