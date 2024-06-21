import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import speech_recognition as sr
import language_tool_python
from transformers import pipeline

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        text_output.insert(tk.END, "Speak now...\n")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        text_output.insert(tk.END, "You said: " + text + "\n")
        return text
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        messagebox.showerror("Error", f"Could not request results from Google Speech Recognition service; {e}")

def check_grammar():
    tool = language_tool_python.LanguageTool('en-US')
    text = input_text.get("1.0", tk.END)
    matches = tool.check(text)
    corrected_text = tool.correct(text)
    text_output.insert(tk.END, "Original Text: " + text + "\n")
    text_output.insert(tk.END, "Corrected Text: " + corrected_text + "\n")

def summarize_text():
    summarizer = pipeline("summarization")
    text = input_text.get("1.0", tk.END)
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    text_output.insert(tk.END, "Original Text: " + text + "\n")
    text_output.insert(tk.END, "Summary: " + summary[0]['summary_text'] + "\n")

# GUI setup
app = tk.Tk()
app.title("Speech-to-Text, Grammar Checker, and Text Summarizer")

# Input text box
input_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=50, height=10)
input_text.pack(padx=10, pady=10)

# Buttons
speech_button = tk.Button(app, text="Speech to Text", command=recognize_speech)
speech_button.pack(pady=5)

grammar_button = tk.Button(app, text="Check Grammar", command=check_grammar)
grammar_button.pack(pady=5)

summary_button = tk.Button(app, text="Summarize Text", command=summarize_text)
summary_button.pack(pady=5)

# Output text box
text_output = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=50, height=10)
text_output.pack(padx=10, pady=10)

app.mainloop()
