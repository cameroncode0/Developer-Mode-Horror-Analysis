import tkinter as tk
from tkinter import messagebox
import random
import time
from PIL import Image, ImageTk
import os
import winsound  # Windows only

# Sound files
sound_effects = {
    "whisper": "whisper.wav",
    "scream": "scream.wav",
    "knock": "knock.wav",
    "heartbeat": "heartbeat.wav",
    "dirt_shoveling": "dirt_shoveling.wav",
    "distorted": "distorted_voice.wav"
}

# Scary quotes
ghost_responses = [
    "They buried me alive...", "I never left this room...", "Do you feel it watching too?",
    "Time loops. Over and over.", "You're already fading...", "Don't answer the door tonight.",
    "My nails scraped the coffin...", "You smell like fear...", "He watches through the mirror...",
    "You should not have summoned me...", "I was cold. Then I woke up. Underground.",
    "Not dead. Not alive. Just forgotten.", "The walls whisper your name...",
    "I can see your breath... but you're not breathing.", "Your shadow moves when you don't..."
]

bg_colors = ["#0a0a0a", "#110000", "#0d0000", "#1a0000", "#000000", "#1a0a0a"]
history = []

root = tk.Tk()
root.title("💀 Bloodbound Death Predictor 💀")
root.geometry("600x800")
root.configure(bg="#0a0a0a")

# State flags
developer_mode = False
last_prediction = ""
jump_scares_enabled = True
flicker_enabled = True
mara_active = False
persistent_haunting = False

# Jumpscare overlay
jumpscare_frame = tk.Frame(root, bg="black")
jumpscare_frame.place(relwidth=1, relheight=1, x=0, y=0)
jumpscare_label = tk.Label(jumpscare_frame, text="", font=("Courier", 40, "bold"), fg="red", bg="black")
jumpscare_label.pack()
jumpscare_img_label = tk.Label(jumpscare_frame, bg="black")
jumpscare_img_label.pack()
jumpscare_frame.lower()

def play_sound(effect):
    if os.path.exists(sound_effects.get(effect, "")):
        winsound.PlaySound(sound_effects[effect], winsound.SND_ASYNC)

def flicker_bg():
    if flicker_enabled:
        color = random.choice(bg_colors)
        root.config(bg=color)
        for widget in root.winfo_children():
            if isinstance(widget, (tk.Label, tk.Entry, tk.Button, tk.Frame)):
                try:
                    widget.config(bg=color)
                except:
                    pass
    root.after(random.randint(200, 500), flicker_bg)

def rotate_quote():
    quote_label.config(text=random.choice(ghost_responses))
    root.after(random.randint(3000, 5000), rotate_quote)

def ghostly_flicker():
    colors = ["#ff5555", "#ff0000", "#770000", "#ff3333", "#aa0000"]
    title_label.config(fg=random.choice(colors))
    root.after(random.randint(300, 700), ghostly_flicker)

def show_jumpscare(text):
    try:
        img = Image.open("jumpscare.png")
        img = img.resize((600, 800))
        photo = ImageTk.PhotoImage(img)
        jumpscare_img_label.config(image=photo)
        jumpscare_img_label.image = photo
    except:
        jumpscare_img_label.config(image="")
        jumpscare_label.config(text=text)

    jumpscare_frame.lift()
    root.update()
    root.after(1000, jumpscare_frame.lower)

def maybe_jump_scare():
    if jump_scares_enabled and random.random() < 0.3:
        play_sound("scream")
        show_jumpscare("BEHIND YOU")

def on_predict():
    year = entry.get()
    countdown_to_prediction(year)

def countdown_to_prediction(year):
    global last_prediction, mara_active
    result_label.config(text="🕯️ Preparing your fate...", fg="#ffffff")
    button.config(state=tk.DISABLED)
    play_sound("heartbeat")

    for i in range(3, 0, -1):
        result_label.config(text=f"🕯️ {i}...", fg="#ff1a1a")
        root.update()
        time.sleep(1)

    result = predict_death_year(year)
    last_prediction = result
    result_label.config(text=result, fg="#ff0000", font=("Courier", 13, "bold"))
    button.config(state=tk.NORMAL)
    history.append(result)
    update_history()

    if year == "666":
        mara_active = True
        play_sound("whisper")
        chatbot_label.config(text="🕯️ Mara: You called me.")
    elif jump_scares_enabled:
        maybe_jump_scare()

def predict_death_year(birth_year_str):
    global developer_mode, mara_active
    if birth_year_str == "death":
        enable_developer_mode()
        return "🛠️ Developer Mode Enabled"
    try:
        birth_year = int(birth_year_str)
        if birth_year < 1900 or birth_year > 2025:
            return "💀 Enter a year between 1900 and 2025."
    except ValueError:
        return "🩸 That's not a number..."

    lifespan = random.randint(60, 100)
    death_year = birth_year + lifespan

    messages = [
        f"💉 Born: {birth_year} | Death: {death_year}",
        f"🩸 You fade in {death_year}", f"⚰️ Death forecast: {death_year}",
        f"🧠 {death_year} — The year it ends...",
        f"☠️ {death_year} - The year you join me...",
        f"🕯️ {death_year} - The candles go out...",
        f"🖤 {death_year} - Your heart stops..."
    ]

    if mara_active:
        response = random.choice([
            f"I will come for you in {death_year}...",
            f"We will meet in {death_year}...",
            f"Your suffering ends in {death_year}...",
            f"{death_year}... I'll be waiting..."
        ])
    else:
        response = random.choice(ghost_responses)

    return f"{random.choice(messages)}\n{response}"

def update_history():
    if history:
        history_text = "\n".join(history[-5:])
        history_label.config(text=f"📜 Previous Fates:\n{history_text}")

def chat_with_mara():
    global mara_active, persistent_haunting
    question = chat_entry.get().lower()
    if question.strip():
        if "hello" in question or "hi" in question:
            response = "Mara: Don't greet the dead..."
        elif "help" in question:
            response = "Mara: No one helped me..."
        elif "who are you" in question:
            response = "Mara: The one beneath your feet..."
        else:
            response = random.choice(ghost_responses)

        chatbot_label.config(text=f"👻 {response}")
        chat_entry.delete(0, tk.END)

        if random.random() < 0.2 and mara_active:
            play_sound("scream")
            show_jumpscare("DON'T TEST ME!")

    if question.count("mara") >= 3:
        play_sound("dirt_shoveling")
        show_jumpscare("SHE DRAGS YOU DOWN...")
        persistent_haunting = True
        
def enable_developer_mode():
    global developer_mode
    developer_mode = True
    dev_frame.pack(pady=10)
    update_dev_info()

    # Subtle creepy audio cue
    if jump_scares_enabled:
        play_sound("whisper")

    # Mara's presence is felt...
    chatbot_label.config(text="🕯️ Mara: You shouldn't be here...")

    # Add to history
    history.append("🛠️ Developer Mode Entered")
    update_history()

    # Quick flicker effect
    root.config(bg="red")
    root.update()
    time.sleep(0.1)
    root.config(bg=random.choice(bg_colors))



def update_dev_info():
    dev_output.config(text=f"Last Prediction: {last_prediction}\nFlicker: {'On' if flicker_enabled else 'Off'}\nJump Scares: {'On' if jump_scares_enabled else 'Off'}\nMara Active: {'Yes' if mara_active else 'No'}")

def toggle_jump_scares():
    global jump_scares_enabled
    jump_scares_enabled = not jump_scares_enabled
    update_dev_info()

def toggle_flicker():
    global flicker_enabled
    flicker_enabled = not flicker_enabled
    update_dev_info()

def show_story():
    story_label.config(text=""" 
Mara was a girl from 1876.
Buried too soon, she clawed at her casket,
but no one heard her.
Now, she listens... from below.
She waits for others who listen back.
""")
    if mara_active:
        play_sound("knock")

def show_about():
    messagebox.showinfo("About", """
💀 Death Year Predictor 💀
Created by: The Midnight Programmer

Features:
- Spooky death predictions
- Developer Mode
- Real ghost quotes (Mara)
- Jump scares
- Sound effects & background flicker
- Ask Mara your questions... if you dare.

This app is not for the faint of heart.
""")

def on_close():
    if mara_active:
        show_jumpscare("YOU CAN'T LEAVE")
        play_sound("scream")  # More intense exit
        root.config(bg="black")
        chatbot_label.config(text="🕯️ Mara: You belong to me now...")
        result_label.config(text="The room grows colder...")
        root.update()
        time.sleep(2.5)
        root.destroy()
    else:
        play_sound("whisper")
        root.destroy()


# Layout
title_label = tk.Label(root, text="☠️ Death Year Revealer ☠️", font=("Courier", 18, "bold"), fg="#ff0000", bg="#0a0a0a")
title_label.pack(pady=15)

label = tk.Label(root, text="When were you born? (e.g. 1990)", fg="#eeeeee", bg="#0a0a0a", font=("Courier", 12))
label.pack()

entry = tk.Entry(root, font=("Courier", 12), width=10, bg="#1a1a1a", fg="#eeeeee", insertbackground="white")
entry.pack(pady=5)

button = tk.Button(root, text="See Your End", command=on_predict,
                   bg="#550000", fg="white", font=("Courier", 12), relief="ridge", activebackground="#770000")
button.pack(pady=15)

result_label = tk.Label(root, text="", fg="#ff3333", bg="#0a0a0a", font=("Courier", 13), wraplength=400, justify="center")
result_label.pack(pady=10)

# Chat section
chat_frame = tk.Frame(root, bg="#0a0a0a")
chat_frame.pack(pady=10)

chat_label = tk.Label(chat_frame, text="Ask the dead (Mara):", fg="#aaaaaa", bg="#0a0a0a", font=("Courier", 10))
chat_label.pack()

chat_entry = tk.Entry(chat_frame, font=("Courier", 10), width=40, bg="#1a1a1a", fg="#eeeeee", insertbackground="white")
chat_entry.pack(pady=5)

chat_button = tk.Button(chat_frame, text="Speak", command=chat_with_mara,
                        bg="#440000", fg="white", font=("Courier", 10), relief="ridge", activebackground="#770000")
chat_button.pack()

chatbot_label = tk.Label(chat_frame, text="", fg="#ff5555", bg="#0a0a0a", font=("Courier", 10, "italic"), wraplength=400)
chatbot_label.pack(pady=5)

# Story, history, and footer
story_button = tk.Button(root, text="Reveal Mara's Story", command=show_story,
                         bg="#330000", fg="white", font=("Courier", 10), relief="ridge")
story_button.pack(pady=5)

story_label = tk.Label(root, text="", fg="#ff6666", bg="#0a0a0a", font=("Courier", 10), wraplength=500, justify="center")
story_label.pack(pady=5)

history_label = tk.Label(root, text="", fg="#ff9999", bg="#0a0a0a", font=("Courier", 10), justify="left")
history_label.pack(pady=10)

quote_label = tk.Label(root, text="", font=("Courier", 10, "italic"), fg="#aa0000", bg="#0a0a0a")
quote_label.pack(side="bottom", pady=5)

about_button = tk.Button(root, text="About", command=show_about, bg="#220000", fg="white", font=("Courier", 10), relief="ridge")
about_button.pack(pady=2)

# Developer mode frame
dev_frame = tk.Frame(root, bg="#0a0a0a")
dev_output = tk.Label(dev_frame, text="", fg="#00ffcc", bg="#0a0a0a", font=("Courier", 10), justify="left")
dev_output.pack()

toggle_jump = tk.Button(dev_frame, text="Toggle Jump Scares", command=toggle_jump_scares,
                         bg="#003333", fg="white", font=("Courier", 10), relief="ridge")
toggle_jump.pack(pady=2)

toggle_flick = tk.Button(dev_frame, text="Toggle Flicker", command=toggle_flicker,
                          bg="#003333", fg="white", font=("Courier", 10), relief="ridge")
toggle_flick.pack(pady=2)

# Start animations
flicker_bg()
rotate_quote()
ghostly_flicker()
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()

