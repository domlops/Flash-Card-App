from tkinter import *
from tkinter import messagebox
import pandas as pd
import random


def load_cards(language): #load the data base based on the language select and set the card list for the session
    global card_list, learn_language, known_language

    if language == 'Italiano':
        try:
            df = pd.read_csv('data/it_words_to_learn.csv')
        except FileNotFoundError:
            original_data = pd.read_csv('data/500_words_it.csv')
            df = original_data.copy()
        finally:
            card_list = df.to_dict(orient='records')
            learn_language = 'Italiano'
            known_language = 'Português'
            
            right_button.config(image=right_img, command=check_word)
            left_button.config(image=wrong_img, command=change_card)
            change_card()

    elif language == 'Deutsch':
        try:
            df = pd.read_csv('data/de_words_to_learn.csv')
        except FileNotFoundError:
            original_data = pd.read_csv('data/500_words_de.csv')
            df = original_data.copy()
        finally:
            card_list = df.to_dict(orient='records')
            learn_language = 'Deutsch'
            known_language = 'English'
            
            right_button.config(image=right_img, command=check_word)
            left_button.config(image=wrong_img, command=change_card)
            change_card()

def check_word(): #excludes the word marked as "known" so the database only keeps the words the user still needs to learn, before changing to the next card
    global count

    count += 1
    
    if count == 20:
        response = messagebox.askyesno(
            title='Daily Goal (Meta Diária)',
            message='You reached your daily goal of 20 words checked, would you like to keep going?\n(Você alcançou sua meta diária de 20 palavras acertadas, gostaria de continuar?')
        #will return True if yes is clicked and after that the program will continue until the user close it

        if response == False:
            window.quit()
    
    card_list.remove(current_card)
    data = pd.DataFrame(card_list)

    if learn_language == 'Italiano':
        data.to_csv('data/it_words_to_learn.csv', index=False)
    elif learn_language == 'Deutsch':
        data.to_csv('data/de_words_to_learn.csv', index=False)

    change_card()

def change_card(): #select a new word to show on the card and set the timer to 3 seconds before activating the show_translation function
    global timer, current_card
        
    current_card = random.choice(card_list) 
    
    canvas.itemconfig(card, image=front_card_img)
    canvas.itemconfig(
        title_text,
        text=learn_language,
        fill='black',
        )
    canvas.itemconfig(
        word_text,
        text=current_card[learn_language],
        font=('Arial', 60, 'bold'),
        fill='black',
        )
    try:
        window.after_cancel(timer)
    except ValueError: #a simple fix so an error doesn't show on the terminal on the first card
        timer = window.after(3000, show_translation)

def show_translation(): #"flips" the card showing the translation of the word
    canvas.itemconfig(card, image=back_card_img)
    canvas.itemconfig(title_text, text=known_language, fill='white')
    canvas.itemconfig(word_text, text=current_card[known_language], fill='white')

def select_language(): #initialize the buttons with language options
    right_button.config(
        text='Italiano/Português',
        command=lambda:load_cards('Italiano'),
        bg=BACKGROUND_COLOR,
        font=('Arial', 20, 'bold'),    
    )

    left_button.config(
        text='Deutsch/English',
        command=lambda:load_cards('Deutsch'),
        bg=BACKGROUND_COLOR,
        font=('Arial', 20, 'bold'),
    )

BACKGROUND_COLOR = "#B1DDC6"

card_list = []
learn_language = ''
known_language = ''
current_card = {}

window = Tk()
window.title('Flash Card App')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = 0
count = 0 #counter of how many cards were marked as "known"

#IMAGES
front_card_img = PhotoImage(file="images/card_front.png")
back_card_img = PhotoImage(file="images/card_back.png")
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")

#CANVAS SETUP
canvas = Canvas(
    width=800,
    height=526,
    bg=BACKGROUND_COLOR,
    highlightthickness=0,
    )
card = canvas.create_image(400, 263, image=front_card_img)
title_text = canvas.create_text(
    400, 150,
    text='Flash Card App',
    font=('Arial', 40, 'italic'),
    )
word_text = canvas.create_text(
    400, 263,
    text='Select a language (Selecione uma lingua)',
    font=('Arial', 20, 'bold'),
    )

canvas.grid(row=0, column=0, columnspan=2)

#BUTTONS
right_button = Button()
left_button = Button()

right_button.grid(row=1, column=1)
left_button.grid(row=1, column=0)

select_language()

window.mainloop()
