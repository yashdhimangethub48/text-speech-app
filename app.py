import os
import uuid
from flask import Flask, request, render_template, send_file, url_for
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    text_result = ""
    mp3_path = ""
    text_input = ""
    selected_lang = "en"  # Default language

    if request.method == "POST":
        # Get selected language
        selected_lang = request.form.get("lang", "en")

        # Text to Speech
        if "text_input" in request.form and request.form["text_input"].strip():
            text_input = request.form["text_input"]
            tts = gTTS(text=text_input, lang=selected_lang)
            filename = f"{uuid.uuid4()}.mp3"
            mp3_path = os.path.join(UPLOAD_FOLDER, filename)
            tts.save(mp3_path)

        # MP3 to Text
        elif "audio_file" in request.files:
            file = request.files["audio_file"]
            if file and file.filename.endswith(".mp3"):
                mp3_file = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(mp3_file)

                wav_file = mp3_file.replace(".mp3", ".wav")
                AudioSegment.from_mp3(mp3_file).export(wav_file, format="wav")

                recognizer = sr.Recognizer()
                with sr.AudioFile(wav_file) as source:
                    audio_data = recognizer.record(source)
                    try:
                        text_result = recognizer.recognize_google(audio_data, language=selected_lang)
                    except Exception as e:
                        text_result = "Sorry, could not recognize the speech."

                os.remove(wav_file)
                os.remove(mp3_file)

    return render_template("index.html",
                           text_input=text_input,
                           text_result=text_result,
                           mp3_path=mp3_path,
                           selected_lang=selected_lang)

@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
