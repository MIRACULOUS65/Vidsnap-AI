from flask import Flask, render_template,request, redirect, url_for
from werkzeug.utils import secure_filename
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static/reels', exist_ok=True)
os.makedirs('static/songs', exist_ok=True)



@app.route("/")
def home():
    return render_template("index.html")




@app.route("/create",methods=["GET", "POST"])
def create():
        myid=uuid.uuid1()
        input_files=[]  # Initialize outside the if block
        if request.method == "POST":
            print(request.files.keys())
            rec_id=request.form.get("uuid")
            desc = request.form.get("text")
            
            for key,value in request.files.items():
                print(key,value)    
                #Upload the file
                file=request.files[key]
                if file:
                    filename = secure_filename(file.filename)
                    if(not(os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],rec_id)))):
                        os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'],rec_id))
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],rec_id, filename))
                    input_files.append(file.filename)

            #capture the description
            with open(os.path.join(app.config['UPLOAD_FOLDER'],rec_id, "desc.txt"),"w") as f:
                f.write(desc)

            # Move the file processing inside the POST block
            for fl in input_files:
                with open(os.path.join(app.config['UPLOAD_FOLDER'],rec_id, "input.txt"),"a") as f:
                    f.write(f"file '{fl}'\nduration 1\n")
                

        return render_template("create.html",myid=myid)
        



@app.route("/gallery")
def gallery():
    try:
        reels = os.listdir("static/reels")
        # Filter only .mp4 files
        reels = [reel for reel in reels if reel.endswith('.mp4')]
        print(f"Found reels: {reels}")
    except FileNotFoundError:
        print("static/reels directory not found, creating...")
        os.makedirs("static/reels", exist_ok=True)
        reels = []
    return render_template("gallery.html", reels=reels)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') != 'production')