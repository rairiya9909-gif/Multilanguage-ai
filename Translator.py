from tkinter import *
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
from PIL import ImageTk, Image

# Prepare language options
indian_langs = {
    "Hindi": "hi", "Marathi": "mr", "Bengali": "bn", "Gujarati": "gu",
    "Tamil": "ta", "Telugu": "te", "Kannada": "kn", "Malayalam": "ml",
    "Punjabi": "pa", "Urdu": "ur", "English": "en"
}
all_langs = list(indian_langs.keys())

# Main app window
app = Tk()
app.title("🎙 Voice Language Translator")
app.geometry("650x550")
app.resizable(False, False)

# Load background image (optional)
try:
    bg_image = Image.open("bg.jpg")  # Your image file
    bg_image = bg_image.resize((650, 550), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(app, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    app.configure(bg="#e6f2ff")

# Functions
def translate_text():
    try:
        src = indian_langs[src_lang.get()]
        dest = indian_langs[dest_lang.get()]
        translated_text = GoogleTranslator(source=src, target=dest).translate(text_entry.get())
        result_label.config(text=translated_text)
    except Exception as e:
        status_label.config(text=f"❌ Translation Error: {e}")

def speak_text():
    text = result_label.cget("text").strip()
    if text:
        try:
            lang_code = indian_langs[dest_lang.get()]
            tts = gTTS(text=text, lang=lang_code)
            filename = "temp_output.mp3"
            tts.save(filename)
            playsound(filename)
            os.remove(filename)
        except Exception as e:
            status_label.config(text=f"TTS Error: {e}")
    else:
        status_label.config(text="⚠ No text to speak.")

def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            status_label.config(text="🎤 Listening...")
            app.update()
            audio = recognizer.listen(source, timeout=5)
            recognized_text = recognizer.recognize_google(audio)
            text_entry.delete(0, END)
            text_entry.insert(0, recognized_text)
            status_label.config(text="✅ Voice input successful.")
        except Exception as e:
            status_label.config(text=f"❌ Voice input failed: {e}")

# Title
Label(app, text="🌐 Voice Translator", font=("Segoe UI", 20, "bold"), bg="#e6f2ff", fg="#003366").pack(pady=10)

# Frame for content
frame = Frame(app, bg="#ffffff", padx=20, pady=20, relief=RIDGE, bd=2)
frame.pack(pady=10)

# Text Entry
Label(frame, text="Enter Text:", font=('Segoe UI', 12, 'bold'), bg="#ffffff").pack(anchor='w')
text_entry = Entry(frame, width=60, font=('Segoe UI', 12))
text_entry.pack(pady=5)

# Language dropdowns
Label(frame, text="From Language:", font=('Segoe UI', 12), bg="#ffffff").pack(anchor='w', pady=(10, 0))
src_lang = StringVar(app)
src_lang.set("English")
OptionMenu(frame, src_lang, *all_langs).pack(pady=5)

Label(frame, text="To Language:", font=('Segoe UI', 12), bg="#ffffff").pack(anchor='w', pady=(10, 0))
dest_lang = StringVar(app)
dest_lang.set("Hindi")
OptionMenu(frame, dest_lang, *all_langs).pack(pady=5)

# Buttons
btn_frame = Frame(frame, bg="#ffffff")
btn_frame.pack(pady=10)

Button(btn_frame, text="🎤 Voice Input", command=voice_input, font=('Segoe UI', 11), bg='#ffcc66', width=15).grid(row=0, column=0, padx=5)
Button(btn_frame, text="🔁 Translate", command=translate_text, font=('Segoe UI', 11), bg='#3399ff', fg='white', width=15).grid(row=0, column=1, padx=5)
Button(btn_frame, text="🔊 Speak Output", command=speak_text, font=('Segoe UI', 11), bg='#33cc99', fg='white', width=15).grid(row=0, column=2, padx=5)

# Output
result_label = Label(frame, text="", wraplength=500, bg="#f5f5f5", height=4, font=('Segoe UI', 12), relief=GROOVE, bd=1, anchor='w', justify=LEFT)
result_label.pack(pady=10, fill=X)

status_label = Label(app, text="", fg="darkred", bg="#e6f2ff", font=('Segoe UI', 10))
status_label.pack()

app.mainloop()