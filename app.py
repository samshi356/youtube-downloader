import os
from flask import Flask, render_template, request
from pytube import YouTube
from pytube.exceptions import PytubeError

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        video_url = request.form.get("url")
        quality = request.form.get("quality")
        try:
            yt = YouTube(video_url)
            if quality == "low":
                stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").first()
            else:
                stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").last()

            stream.download(output_path=DOWNLOAD_FOLDER)
            message = f"Downloaded: {yt.title}"
        except PytubeError as e:
            message = f"Download error: {str(e)}"
        except Exception as e:
            message = f"Unexpected error: {str(e)}"
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
