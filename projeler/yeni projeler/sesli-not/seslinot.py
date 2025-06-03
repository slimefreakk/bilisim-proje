#kodun çalışması için pyaudio ve speechrecognition gerekmetedir
#pip install speechrecognition
#pip install pyaudio (ikisinide komut istemcisine yazın)
#Mert Tangül ve Selim Haftacıoğullarının projesidir




import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import speech_recognition as sr
from datetime import datetime
import json
import os

NOTES_FILE = "notes.json"

# Notları kaydetme
def save_note(note, category):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"note": note, "category": category, "timestamp": timestamp}
    
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            notes = json.load(f)
    else:
        notes = []
    
    notes.append(entry)
    
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)
    
    messagebox.showinfo("Başarılı", "Not kaydedildi!")

# Sesli not alma
def record_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        messagebox.showinfo("Bilgi", "Lütfen konuşun...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="tr-TR")
        category = simpledialog.askstring("Kategori", "Not kategorisini girin:")
        if category:
            save_note(text, category)
            show_notes()
    except sr.UnknownValueError:
        messagebox.showerror("Hata", "Ses anlaşılamadı.")
    except sr.RequestError:
        messagebox.showerror("Hata", "Google API erişilemedi.")

# Notları göster
def show_notes():
    notes_box.delete("1.0", tk.END)
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            notes = json.load(f)
            for n in notes:
                notes_box.insert(tk.END, f"[{n['timestamp']}] ({n['category']}): {n['note']}\n")

# Arayüz
root = tk.Tk()
root.title("Sesli Not Uygulaması")
root.geometry("500x500")

btn_record = tk.Button(root, text="🎙️ Sesli Not Al", command=record_voice, bg="#5cb85c", fg="white", font=("Arial", 12))
btn_record.pack(pady=10)

notes_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 10))
notes_box.pack(expand=True, fill='both', padx=10, pady=10)

btn_refresh = tk.Button(root, text="🔄 Notları Yenile", command=show_notes, bg="#0275d8", fg="white")
btn_refresh.pack(pady=5)

show_notes()
root.mainloop()
