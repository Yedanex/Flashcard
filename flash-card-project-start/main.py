from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

current_card = {}
to_learn = {}


try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/jap_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Japanese", fill="black")
    canvas.itemconfig(card_word, text=current_card["Japanese"], fill="black")
    canvas.itemconfig(card_background, image=front)
    flip_timer = window.after(5000, func=change_card)


def change_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=back)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn", index=False)
    next_card()


window = Tk()
window.title("Flashcard")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=change_card)

canvas = Canvas(width=800, height=526)
front = PhotoImage(file="images/card_front.png")
card_background = canvas.create_image(400, 263, image=front)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"), fill="black")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

back = PhotoImage(file="images/card_back.png")

right = PhotoImage(file="images/right.png")
right_button = Button(image=right, highlightbackground=BACKGROUND_COLOR, command=is_known)
right_button.grid(row=1, column=0)

wrong = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong, highlightbackground=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(row=1, column=1)

next_card()


window.mainloop()

