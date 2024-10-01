from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
# Functions


def read_word():
    try:
        french = pandas.read_csv("./data/words_to_learn")
    except FileNotFoundError:
        french = pandas.read_csv("./data/french_words.csv")
        french.to_csv("./data/words_to_learn", index=False)
    word_dict = french.to_dict(orient="records")
    word = random.choice(word_dict)
    return word


def right_button():
    global flip_timer
    window.after_cancel(flip_timer)
    new_word = read_word()
    removed_word = pandas.read_csv("./data/words_to_learn")
    r_word_dict = removed_word.to_dict(orient="records")
    current_word = canvas.itemcget(french_word, "text")
    for d in r_word_dict:
        if d["English"] == current_word or d["French"] == current_word:
            r_word_dict.remove(d)
    data = pandas.DataFrame(r_word_dict)
    data.to_csv("./data/words_to_learn", index=False)
    reset_card()
    canvas.itemconfig(french_word, text=new_word["French"])
    flip_timer = window.after(3000, flip_card)


def wrong_button():
    global flip_timer
    window.after_cancel(flip_timer)
    new_word = read_word()
    reset_card()
    canvas.itemconfig(french_word, text=new_word["French"])
    flip_timer = window.after(3000, flip_card)


def flip_card():
    global card_back
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(language, text="English", fill="white")
    words = pandas.read_csv("./data/french_words.csv")
    english = words[words["French"] == canvas.itemcget(french_word, 'text')]
    canvas.itemconfig(french_word, text=english.English.values[0], fill="white")


def reset_card():
    global card_front
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(french_word, fill="black")


# GUI
window = Tk()
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)
window.title("Flashcards!")
flip_timer = window.after(3000, flip_card)

# Canvas
card_back = PhotoImage(file="./images/card_back.png")
canvas = Canvas(height=526, width=800, background=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_image = canvas.create_image(400, 263, image=card_front)
language = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
french_word = canvas.create_text(400, 263, text="partie", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
cross = PhotoImage(file="./images/wrong.png")
wrong = Button(image=cross, highlightthickness=0, command=wrong_button)
wrong.grid(row=1, column=0, pady=10)
tick = PhotoImage(file="./images/right.png")
right = Button(image=tick, highlightthickness=0, command=right_button)
right.grid(row=1, column=1)


window.mainloop()
