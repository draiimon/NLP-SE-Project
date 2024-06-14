import tkinter as tk
import random  # For generating random suggestions
from groq import Groq
import os
import threading

# Set GROQ API key
os.environ["GROQ_API_KEY"] = "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"

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Function to generate AI response in a separate thread
def generate_response_async(prompt):
    response = generate_response(prompt)
    update_chat_display(prompt, response)

# Function to generate AI response
def generate_response(prompt):
    # Define the user message
    user_message = [{"role": "user", "content": prompt}]
    
    # Request chat completion
    chat_completion = client.chat.completions.create(
        messages=user_message,
        model="llama3-8b-8192",
    )
    
    # Get the AI response
    ai_response = chat_completion.choices[0].message.content
    
    # Customize the response to mention MoodSync
    ai_response = ai_response.replace("AI", "MoodSync")
    return ai_response

# Function to update the chat display
def update_chat_display(user_message, ai_response):
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You: {user_message}\n", "user")
    chat_display.insert(tk.END, f"MoodSync: {ai_response}\n\n", "ai")
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)

# Function to handle button click event
def on_click(event=None):
    prompt = user_input.get()
    if prompt:
        user_input.delete(0, tk.END)
        threading.Thread(target=generate_response_async, args=(prompt,)).start()

# Function to generate a random suggestion
def generate_suggestion():
    suggestions = [
        "How was your day?",
        "What's on your mind?",
        "Tell me about something that made you happy today.",
        "How are you feeling right now?",
        "Share a recent experience with me.",
        "Is there something you'd like to talk about?"
    ]
    return random.choice(suggestions)

# Function to handle suggestion button click event
def on_suggestion_click():
    suggestion = generate_suggestion()
    user_input.insert(tk.END, suggestion)

# Create main application window
root = tk.Tk()
root.title("MoodSync - AI Mood Tracker")

# Create text widget for chat display
chat_display = tk.Text(root, height=20, width=50, wrap=tk.WORD)
chat_display.pack(padx=10, pady=10)
chat_display.tag_config("user", foreground="blue")
chat_display.tag_config("ai", foreground="green")
chat_display.config(state=tk.DISABLED)

# Create entry widget for user input
user_input = tk.Entry(root, width=50)
user_input.pack(padx=10, pady=(0, 10))
user_input.bind("<Return>", on_click)

# Create button to trigger AI response
send_button = tk.Button(root, text="Send", command=on_click)
send_button.pack(padx=10, pady=(0, 10), ipadx=10)

# Create suggestion button
suggestion_button = tk.Button(root, text="Suggestion", command=on_suggestion_click)
suggestion_button.pack(padx=10, pady=(0, 10), ipadx=10)

# Introduce MoodSync with a personalized touch
intro_text = "Welcome to MoodSync!\nI'm here to listen, understand, and sync with your mood. Share how you feel with me, and let's navigate through emotions together."
chat_display.insert(tk.END, intro_text, "intro")
chat_display.tag_config("intro", foreground="purple", font=("Helvetica", 12, "italic"))

# Run the application
root.mainloop()
