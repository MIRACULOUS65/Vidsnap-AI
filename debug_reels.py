#!/usr/bin/env python3
"""
Debug script to test reel generation locally
"""
import os
import sys
from text_to_audio import text_to_speech_file
import subprocess

def test_reel_generation():
    print("Testing reel generation process...")
    
    # Check directories
    print("\n1. Checking directories:")
    dirs = ["user_uploads", "static/reels", "static/songs"]
    for directory in dirs:
        exists = os.path.exists(directory)
        print(f"   {directory}: {'✓' if exists else '✗'}")
        if not exists:
            os.makedirs(directory, exist_ok=True)
            print(f"   Created {directory}")
    
    # Check user uploads
    print("\n2. Checking user uploads:")
    try:
        folders = os.listdir("user_uploads")
        print(f"   Found folders: {folders}")
        
        for folder in folders:
            if os.path.isdir(f"user_uploads/{folder}"):
                print(f"\n   Checking folder: {folder}")
                files = os.listdir(f"user_uploads/{folder}")
                print(f"      Files: {files}")
                
                # Check required files
                desc_exists = os.path.exists(f"user_uploads/{folder}/desc.txt")
                input_exists = os.path.exists(f"user_uploads/{folder}/input.txt")
                print(f"      desc.txt: {'✓' if desc_exists else '✗'}")
                print(f"      input.txt: {'✓' if input_exists else '✗'}")
                
    except FileNotFoundError:
        print("   No user_uploads directory found")
    
    # Check static/reels
    print("\n3. Checking generated reels:")
    try:
        reels = os.listdir("static/reels")
        reels = [r for r in reels if r.endswith('.mp4')]
        print(f"   Found reels: {reels}")
    except FileNotFoundError:
        print("   No static/reels directory found")
    
    # Check done.txt
    print("\n4. Checking done.txt:")
    try:
        with open("done.txt", "r") as f:
            done = f.readlines()
        print(f"   Processed folders: {[d.strip() for d in done]}")
    except FileNotFoundError:
        print("   No done.txt file found")
        with open("done.txt", "w") as f:
            f.write("")
        print("   Created empty done.txt")

if __name__ == "__main__":
    test_reel_generation()