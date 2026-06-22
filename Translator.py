from tkinter import *
from deep_translator import GoogleTranslator
import speech_recognition as sr
import sounddevice as sd
import threading
import time
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
    def record_and_recognize():
        try:
            status_label.config(text="🎤 Listening... Speak now!")
            app.update()
            
            fs = 16000
            duration = 5
            
            # Start recording
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
            
            # Countdown in status label
            for i in range(duration, 0, -1):
                status_label.config(text=f"🎤 Listening... ({i}s left)")
                app.update()
                time.sleep(1)
                
            sd.wait()
            status_label.config(text="⚙ Processing speech...")
            app.update()
            
            frame_data = recording.tobytes()
            audio_data = sr.AudioData(frame_data, fs, 2)
            
            recognizer = sr.Recognizer()
            recognized_text = recognizer.recognize_google(audio_data)
            
            def success():
                text_entry.delete(0, END)
                text_entry.insert(0, recognized_text)
                status_label.config(text="✅ Voice input successful.")
            app.after(0, success)
            
        except sr.UnknownValueError:
            app.after(0, lambda: status_label.config(text="❌ Could not understand audio."))
        except sr.RequestError as e:
            app.after(0, lambda: status_label.config(text=f"❌ Service error: {e}"))
        except Exception as e:
            app.after(0, lambda: status_label.config(text=f"❌ Voice input failed: {e}"))

    threading.Thread(target=record_and_recognize, daemon=True).start()

# Title
Label(app, text="🌐 Voice Translator", font=("Segoe UI", 22, "bold"), bg="#e6f2ff", fg="#003366").pack(pady=12)

# Frame for content
frame = Frame(app, bg="#ffffff", padx=25, pady=25, relief=FLAT, bd=0)
# Add a subtle border effect for frame using highlight thickness
frame.config(highlightbackground="#d9d9d9", highlightthickness=1)
frame.pack(pady=10)

# Text Entry
Label(frame, text="Enter Text:", font=('Segoe UI', 11, 'bold'), bg="#ffffff", fg="#333333").pack(anchor='w')
text_entry = Entry(frame, width=54, font=('Segoe UI', 12), relief=SOLID, bd=0, highlightbackground="#cccccc", highlightcolor="#3399ff", highlightthickness=1)
text_entry.pack(pady=8, ipady=4)  # ipady adds inner vertical padding

# Dropdown helper styling
def style_option_menu(om):
    om.config(
        font=('Segoe UI', 10),
        bg='#f5f5f5',
        fg='#333333',
        activebackground='#e0e0e0',
        activeforeground='#333333',
        relief=FLAT,
        bd=0,
        highlightthickness=1,
        highlightbackground='#cccccc',
        width=15,
        cursor='hand2'
    )
    om["menu"].config(font=('Segoe UI', 10), bg='#ffffff', fg='#333333', activebackground='#3399ff', activeforeground='#ffffff')

# Language dropdowns
lang_frame = Frame(frame, bg="#ffffff")
lang_frame.pack(fill=X, pady=5)

# From Language
from_container = Frame(lang_frame, bg="#ffffff")
from_container.pack(side=LEFT, padx=(0, 20))
Label(from_container, text="From Language:", font=('Segoe UI', 10, 'bold'), bg="#ffffff", fg="#555555").pack(anchor='w')
src_lang = StringVar(app)
src_lang.set("English")
src_menu = OptionMenu(from_container, src_lang, *all_langs)
style_option_menu(src_menu)
src_menu.pack(pady=4)

# To Language
to_container = Frame(lang_frame, bg="#ffffff")
to_container.pack(side=LEFT)
Label(to_container, text="To Language:", font=('Segoe UI', 10, 'bold'), bg="#ffffff", fg="#555555").pack(anchor='w')
dest_lang = StringVar(app)
dest_lang.set("Hindi")
dest_menu = OptionMenu(to_container, dest_lang, *all_langs)
style_option_menu(dest_menu)
dest_menu.pack(pady=4)

# Hover event helpers for buttons
def on_enter(e):
    e.widget.config(bg=e.widget.hover_bg)

def on_leave(e):
    e.widget.config(bg=e.widget.normal_bg)

# Buttons
btn_frame = Frame(frame, bg="#ffffff")
btn_frame.pack(pady=15)

btn_voice = Button(btn_frame, text="🎤 Voice Input", command=voice_input, font=('Segoe UI', 11, 'bold'), bg='#ffcc66', fg='#333333', activebackground='#e6b85c', relief=FLAT, width=15, cursor="hand2", bd=0)
btn_voice.normal_bg = '#ffcc66'
btn_voice.hover_bg = '#e6b85c'
btn_voice.bind("<Enter>", on_enter)
btn_voice.bind("<Leave>", on_leave)
btn_voice.grid(row=0, column=0, padx=6)

btn_translate = Button(btn_frame, text="🔁 Translate", command=translate_text, font=('Segoe UI', 11, 'bold'), bg='#3399ff', fg='white', activebackground='#1a80e6', relief=FLAT, width=15, cursor="hand2", bd=0)
btn_translate.normal_bg = '#3399ff'
btn_translate.hover_bg = '#1a80e6'
btn_translate.bind("<Enter>", on_enter)
btn_translate.bind("<Leave>", on_leave)
btn_translate.grid(row=0, column=1, padx=6)

btn_speak = Button(btn_frame, text="🔊 Speak Output", command=speak_text, font=('Segoe UI', 11, 'bold'), bg='#33cc99', fg='white', activebackground='#29b385', relief=FLAT, width=15, cursor="hand2", bd=0)
btn_speak.normal_bg = '#33cc99'
btn_speak.hover_bg = '#29b385'
btn_speak.bind("<Enter>", on_enter)
btn_speak.bind("<Leave>", on_leave)
btn_speak.grid(row=0, column=2, padx=6)

# Output
result_label = Label(frame, text="", wraplength=500, bg="#f9f9f9", height=4, font=('Segoe UI', 12), relief=SOLID, bd=0, highlightbackground="#dddddd", highlightthickness=1, anchor='nw', justify=LEFT, padx=12, pady=12)
result_label.pack(pady=10, fill=X)

status_label = Label(app, text="", fg="#003366", bg="#e6f2ff", font=('Segoe UI', 10, 'italic'))
status_label.pack()

app.mainloop()