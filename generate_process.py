#this file looks for new folders inside user uploads and converts them to reel if they are not already converted
import os
def text_to_audio(folder):
    print("text_to_audio",folder)

def create_reel(folder):
    print("create_reel",folder)

if __name__=="__main__":
    with open("done.txt","r") as f:
        done_folders=f.readlines()

    done_folders=[f.strip() for f in done_folders] #need coz if the folders are already processed they will not be needed to be processed again
    folders= os.listdir("user_uploads")
    for folder in folders:
        if (folder not in done_folders):
            text_to_audio(folder) #generate the audio from desc.txt
            create_reel(folder) #convert the images and audio.mp3 inside the folder to a reel
            with open("done.txt","a") as f:
                f.write(folder+"\n")
