import os
import uuid
from flask import Flask, request, render_template, send_file
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    text_result = ""
    mp3_path = ""
    text_input = ""
    if request.method == "POST":
        if "text_input" in request.form and request.form["text_input"].strip():
            text_input = request.form["text_input"]
            lang = request.form.get("language", "en")
            tts = gTTS(text=text_input, lang=lang)
            filename = f"{uuid.uuid4()}.mp3"
            mp3_path = os.path.join(UPLOAD_FOLDER, filename)
            tts.save(mp3_path)
        elif "audio_file" in request.files:
            file = request.files["audio_file"]
            if file.filename.endswith(".mp3"):
                mp3_file = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(mp3_file)
                wav_file = mp3_file.replace(".mp3", ".wav")
                AudioSegment.from_mp3(mp3_file).export(wav_file, format="wav")
                recognizer = sr.Recognizer()
                with sr.AudioFile(wav_file) as source:
                    audio_data = recognizer.record(source)
                    try:
                        text_result = recognizer.recognize_google(audio_data)
                    except:
                        text_result = "Sorry, could not recognize the speech."
                os.remove(wav_file)
                os.remove(mp3_file)
    return render_template("index.html", text_result=text_result, mp3_path=mp3_path, text_input=text_input)

@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
