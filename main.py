import random
from collections import Counter
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import threading
import random
import time
import pygame

# Import libaries

# declare library
pygame.init()

letterlist = []
scorelabel2 = 0
intscore = 0
usedsr = False
usedx = False
mp = 1  # multiplier
# new
f1 = None
f2 = None
f3 = None
f4 = None
reload = False
last_update = pygame.time.get_ticks()
current_update = 0

vowellist = (65, 69, 73, 85, 79)
# delcares list to hold the ASCII numbers for vowels

#Creates the Scrabble word list 
with open("Collins Scrabble Words (2019).txt", "r") as file:
    word_list = set(line.strip().lower() for line in file) 

scrabble_points = {
    'a': 1,
    'b': 3,
    'c': 3,
    'd': 2,
    'e': 1,
    'f': 4,
    'g': 2,
    'h': 4,
    'i': 1,
    'j': 8,
    'k': 5,
    'l': 1,
    'm': 3,
    'n': 1,
    'o': 1,
    'p': 3,
    'q': 10,
    'r': 1,
    's': 1,
    't': 1,
    'u': 1,
    'v': 4,
    'w': 4,
    'x': 8,
    'y': 4,
    'z': 10
}

def scoring(arr):
    score = 0
    for i in range(len(arr)):
        for key, value in scrabble_points.items():
            if key == str(arr[i].lower()):
                score += value
    return score


def splitword(word):
    List = []
    for item in word:
        List.append(item)
    return List


# function for splitting the letters in the verified word into a list

def validate_duplicates(letter_list):
    letter_counts = Counter(letter_list)

    # checks if any letter count is greater than 1
    for letter, count in letter_counts.items():
        if count > 1:
            return True  # duplicates found
    return False  # no duplicare found


def createalphalist():
    letterlist.clear()
    # declares list which hold the alphabet letters
    global vowellist
    randnumber = 0
    for i in range(6):
        randnumber = random.randint(65, 90)
        # generates 6 random number from 65 to 90 as these are the ascii numbers
        # which correspond to the uppercase alphabet
        letterlist.append(chr(randnumber))
    for i in range(3):
        randnumber = random.choice(vowellist)
        letterlist.append(chr(randnumber))
        # last character must always be a vowel
    if validate_duplicates(letterlist) is True:
        createalphalist()
        return letterlist
    else:
        return letterlist


def realword(word, letterlist):
    global twoplayer
    global timeron
    global finish
    global playerscore
    global intscore
    global roundnumber
    global mp
    global ticked
    global word_list
    if roundnumber >= 6:
        finish = True

    if word in word_list:
        intscore = intscore + (scoring(splitword(word)) * mp)
        playerscore.set(intscore)
        prompt.set("The word '" + word + "' is correct\n" + str(scoring(splitword(word)) * mp) + " points are awarded!")
        roundnumber += 1
        mp = 1
        if roundnumber >= 6: 
            # timeron = False
            endgame(intscore, db(score=intscore))
            return

        rack.set(rack_opto((createalphalist())))
        ticked = False
        player1()
        return True
    else:
        prompt.set("This word is incorrect...")
        return False


# function which uses api to determine whether the word is valid or not

def validword(word, letterlist):
    global prompt
    validcount = 0
    if word.isalpha() is False:
        prompt.set("Invalid word")
        return False
    elif len(word) > 9:
        prompt.set("Word is too long")
        return False
    elif len(word) < 2:
        prompt.set("Word is too short")
        return False
    else:
        for char in word:
            for i in range(len(letterlist)):
                if letterlist[i] == str(char.upper()):
                    validcount += 1
        if validcount >= len(word):
            realword(word, letterlist)
            return True
        else:
            prompt.set("You have used letters which are not in the rack")
            return False


################################
# gui section######################
################################


finish = False
twoplayer = False
timerlabel = None
ticked = True
ticked_no = 0


# needs fixing
def endgame(score=0, scoredict={}):
    # new
    global frame1
    global frame2
    global frame3
    global frame4
    global timeron
    global ticked_no
    global usedx
    global usedsr
    global f1
    global f2
    global f3
    global f4

    global hex_background
    global hex_buttons

    global message
    global number
    global scorelist

    # Declaring all the frame variables

    timeron = False
    ticked_no = 0

    # code from chat gpt which iterates through list and deletes previous frames
    frames = [frame1, frame2, frame3, frame4]
    for frame in frames:
        if frame is not None:
            frame.destroy()
    for i in range(len(frames)):
        frames[i] = None

    f = [f1, f2, f3, f4]
    for frame in f:
        if frame is not None:
            frame.destroy()
    for i in range(len(f)):
        f[i] = None

    frame4 = Frame(root, bg=hex_background, width=1750,
                   height=1700)
    frame4.pack(expand=True, fill=BOTH)
    # Creating the first frame

    f = Frame(frame4, bg="#808080")
    f.pack(expand=True, fill=BOTH)
    f.pack(side="bottom", padx=100)
    # creates child frame for ui

    # reset
    prompt.set("")
    entryword.set("")
    playerscore.set("0")
    usedx = False
    usedsr = False

    CongratsLabel = Label(frame4, text=(f"Your Final Score Is: {score}"), bg=hex_buttons, fg="white",
                          font=("impact", 40),
                          width=300, height=3)
    CongratsLabel.pack(side="top")

    btn_MM = Button(f, text="Main Menu", font='impact 27', bg=hex_buttons, fg='white', command=MM)
    btn_MM.pack(padx=50, pady=10, side="bottom")  # 40
    btn_MM.pack_configure(anchor="e")
    # Main Menu

    ScoreLabel = Label(f, text=("Well Done!"), bg="#808080", fg="white",
                       font=("impact", 32), width=60)
    ScoreLabel.pack(padx=20, pady=5, ipady=0)  # 40
    # chatgpt helped
    # Basically
    highscores = [
        ("AI8888888889", 0),
        ("Botmaaeel69", 0),
        ("Placeholder", 0),
        ("MHartley1234", 0),
        ("AdinRossKickDeal", 0)
    ]

    # add items from scoredict to highscore list
    for username, score in scoredict.items():
        highscores.append((username, score))

    #print(highscores)

    # Sort the highscores list based on the score (second element of each tuple) in descending order
    sorted_highscores = sorted(highscores, key=lambda x: x[1], reverse=True)

    # keeps first 5 elements
    sorted_highscores = sorted_highscores[:5]
    #print(sorted_highscores)

    max_username_length = max(
        len(username) for username, _ in sorted_highscores)  # iterate trhough first items in the tuple

    HighscoreLabel = Label(f, text=(
            f"HIGHSCORES:\n\n" +
            ''.join(
                f"{username}{' ' * (max_username_length - len(username))}\t\t{score}\n" for username, score in
                sorted_highscores)
    ), bg=hex_buttons, fg="white", font=("impact", 24), width=40)
    HighscoreLabel.pack(padx=20, pady=10, ipady=10)  # 40

    UsernameMessage = Label(f, textvariable=highscore_prompt, bg="#808080", fg="white",
                            font=("impact", 24), width=60)
    UsernameMessage.pack(padx=10, pady=10, ipady=10)  # 40

    btn_enter = Button(f, width="12", text="ENTER", font='Impact 27', bg=hex_buttons, fg='ghostwhite',
                       command=lambda: confirm_entry(User_high.get()))
    btn_enter.pack(pady=5, side="bottom")
    # enter

    UsernameEntry = Entry(f, textvariable=User_high, bg=hex_buttons, fg="ghostwhite", font=("segoe print", 24),
                          width=20)
    UsernameEntry.pack(padx=50, pady=10, side="bottom")  # 40

def db(name=None, score=None, db_path="Highscore.db"):
    """
    Adds a user and score to the database (if valid) and returns a dict of all user scores.
    
    Parameters:
        name (str): The player's name (alphanumeric). Ignored if None or invalid.
        score (int): The player's score. Ignored if None or 0.
        db_path (str): Path to SQLite database file.
        
    Returns:
        dict: {name: score} for all entries in the database.
    """
    import sqlite3
    # Connect to database and create table if it doesn't exist
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        """)
        
        # Insert valid user
        if name and score:
            if isinstance(name, str) and name.isalnum() and isinstance(score, int) and score > 0:
                cursor.execute("INSERT INTO users (name, score) VALUES (?, ?)", (name, score))
        
        # Fetch all users
        cursor.execute("SELECT name, score FROM users")
        rows = cursor.fetchall()
        
    # Build the dictionary, using alphanumeric prefix of names
    scoredict = {}
    for user_name, user_score in rows:
        clean_name = "".join([c for c in user_name if c.isalnum()])
        if clean_name:
            scoredict[clean_name] = user_score
            
    return scoredict


def j():
    global letterlist
    word = entryword.get()
    validword(word, letterlist)


# receives entry box inout and puts into validation funcion

def x2():
    global usedx
    global mp
    global btn_x2_colour
    global used_button_colour

    if usedx is False:
        mp = 2
        prompt.set("X2 SCORE ENABLED")
        usedx = True
        btn_x2_colour = used_button_colour

    else:
        mp = 1
        prompt.set("Already used this ability")



def shufflerack():
    global usedsr
    global btn_shuffle_colour
    global used_button_colour

    if usedsr is False:
        rack.set(rack_opto((createalphalist())))
        prompt.set("SHUFFLE RACK ENABLED")
        usedsr = True
        global timer
        timer = 30
        btn_shuffle_colour = used_button_colour

    else:
        prompt.set("Already used this ability")


hex_background = "#F3EFE0"
hex_buttons = "#BD2626"
used_button_colour = "#7F1919"
frame1 = None
frame2 = None
frame3 = None
frame4 = None
timedout = True
timeron = None
ticker = 0
# declare variables


root = Tk()

root.title("Scrabble")

# configure the window attributes to make it fullscreen
root.attributes("-fullscreen", True)


root_width = root.winfo_screenwidth()
root_height = root.winfo_screenheight()
# set the window geometry to match the screen resolution
root.geometry("{0}x{1}+0+0".format(root_width, root_height))


root.config(bg=hex_background)


def timefunc():
    global timer
    global timeron
    global roundnumber
    global ticker
    global twoplayer
    global ticked
    global rack

    # print(timeron,ticker)
    if timeron and ticker == 1:
        if int(timer) > 0:
            timerno.set(str(timer))
            timer -= 1
            root.after(1000, timefunc)
            # Call timefunc again after 1000 milliseconds (1 second)
        else:
            timeron = False
            timerno.set("0")
            roundnumber += 1
            rack.set(rack_opto(createalphalist()))
            prompt.set("Make sure you look at the timer!")
            mp = 1
            ticker = 0
            ticked = True
            rack.set(rack_opto((createalphalist())))
            player1()
            if roundnumber >= 6:
                # timeron = False
                endgame(intscore, db(score=intscore))
    ticker = 1
    # validates whether the user has run out of time

    # Buttons for main menu


def MM():
    global frame1
    global frame2
    global frame3
    global frame4
    global rack
    global intscore
    global roundnumber
    global ticked
    global ticked_no
    global usedsr
    global prompt

    global btn_font_shuffle_colour
    global btn_font_x2_colour
    global btn_x2_colour
    global btn_shuffle_colour

    btn_shuffle_colour = hex_buttons
    btn_x2_colour = hex_buttons
    btn_font_shuffle_colour = '#F8F8FF'
    btn_font_x2_colour ='#F8F8FF'



    #reset prompt    
    prompt.set("Type a word using as many letters as possible")
    usedsr = False

    if ticked_no == 1: # determines whether timer should play
        ticked = False
    else:
        ticked = True
    # Declaring all the frame variables

    roundnumber = 1
    intscore = 0

    rack.set(rack_opto((createalphalist())))
    highscore_prompt.set("Enter your username below (8-16 Characters Only)")

    frames = [frame1, frame2, frame3, frame4]
    for frame in frames:
        if frame is not None:
            frame.destroy()
    for i in range(len(frames)):
        frames[i] = None

    frame1 = Frame(root, bg=hex_background, width=1750,
                   height=1700)
    frame1.pack(expand=True, fill=BOTH)
    # Creating the first frame

    TopHeading = Label(frame1, width=300, height=2, text="Red Scrabble", bg=hex_buttons, fg="ghostwhite",
                       font=("Impact", 32)).pack()
    # Creates the main heading for the Main menu page

    btn_play = Button(frame1, text="Play", font='Impact 60', bg=hex_buttons, fg='ghostwhite', command=player1,
                      width=15)
    btn_play.pack(padx=.032552*root_width, pady=0.0925925*root_height)
    # Creates the play button

    btn_exit = Button(frame1, text="Exit", font='Impact 60', bg=hex_buttons, fg='ghostwhite', command=close, width=15)
    btn_exit.pack(padx=.032552*root_width, pady=0.0925925*root_height)
    # Creates the exit button


# addition#####

# makes the rack sring # rack_opto( # actually works
def rack_opto(rack):
    rack_string = ""
    for i in range(len(rack) - 1):
        rack_string = " " + rack_string + str(rack[i]) + "     "
    return str(rack_string)


entryword = StringVar()
User_high = StringVar()
rack = StringVar()
rack.set(rack_opto((createalphalist())))
prompt = StringVar()
prompt.set("Type a word using as many letters as possible")
highscore_prompt = StringVar()
highscore_prompt.set("Enter your username below (8-16 Characters Only)")
playerscore = StringVar()
playerscore.set("0")
timerno = StringVar()
roundnumber = 1

def use_shufflerack():
    shufflerack()

    # darken the button after use
    global btn_shuffle_colour
    global btn_font_shuffle_colour
    btn_shuffle_colour = used_button_colour  # darker red
    btn_font_shuffle_colour = '#A9A9A9' 
    btn_shuffle.configure(bg=btn_shuffle_colour, fg = btn_font_shuffle_colour)

def use_x2():
    x2()

    # darken the button after use
    global btn_x2_colour
    global btn_font_x2_colour
    btn_x2_colour = used_button_colour  # darker red
    btn_font_x2_colour = '#A9A9A9'  
    btn_x2.configure(bg=btn_x2_colour, fg = btn_font_x2_colour)



def player1():
    global roundnumber
    global frame1
    global frame2
    global frame3
    global frame4
    # new
    global f1
    global f2
    global f3
    global f4
    global reload

    global rack
    global prompt
    global entryword
    global playerscore
    global timerlabel
    global timer
    global timeron
    global ticker
    global ticked  # only need to call once for the timer
    global ticked_no
    ticked_no = 1
    global btn_shuffle_colour
    global btn_x2_colour
    global hex_buttons
    global btn_x2
    global btn_shuffle
    global btn_font_shuffle_colour
    global btn_font_x2_colour

    timer = 30
    timerno.set("30")
    entryword.set("")
    twoplayer = False
    ticker = 1


    # Declaring all the frame variables

    frames = [frame1, frame2, frame3, frame4]
    for frame in frames:
        if frame is not None:
            frame.destroy()
    for i in range(len(frames)):
        frames[i] = None

    f1 = None
    f2 = None
    f3 = None
    f4 = None

    frame3 = Frame(root, bg=hex_background, width=1750,
                   height=1700)
    frame3.pack(expand=True, fill=BOTH)
    # Creating the first frame

    f1 = Frame(frame3, bg="#AEB6BF", width=250,
               height=500)
    f1.grid(row=0, column=0, pady=60, padx=20, ipady=10)
    f2 = Frame(frame3, bg="#808080", width=1200,
               height=750)
    f2.grid(row=0, column=1, pady=60, ipadx=100, padx=200)
    # delcaring sub frames within this function

    NumberLabel = Label(f2, text="Your Rack ", bg=hex_buttons, fg="ghostwhite", font=("impact", 48), width=20)
    NumberLabel.pack(padx=2, pady=20)

    RoundLabel = Label(f1, text=(f"Round {roundnumber}"), bg=hex_buttons, fg="ghostwhite", font=("Impact", 42), width=8)
    RoundLabel.grid(row=0, column=0, pady=20)
    # round
    wordlistlabel = Label(f2, textvariable=rack, bg=hex_buttons, fg="ghostwhite", font=("Impact", 32), width=25)
    wordlistlabel.pack(pady=20)
    # rack list
    WordEntry = Entry(f2, textvariable=entryword, bg=hex_buttons, fg="ghostwhite", font=("segoe print", 30), width=12)
    WordEntry.pack(pady=20)
    # entry
    responselabel = Label(f2, textvariable=prompt, fg="ghostwhite", font=("Impact", 20), width=50, bg="#808080")
    responselabel.pack(pady=10)
    # response
    btn_enter = Button(f2, width="12", text="ENTER", font='Impact 27', bg=hex_buttons, fg='ghostwhite', command=j)
    btn_enter.pack(pady=20)
    # enter
    scorelabel = Label(f1, text="Score:", bg=hex_buttons, fg="ghostwhite", font=("Impact", 27), width=7)
    scorelabel.grid(row=6, column=0, padx=2, pady=10)
    # scorelabel
    scorelabel2 = Label(f1, textvariable=playerscore, bg=hex_buttons, fg="ghostwhite", font=("Impact", 27), width=5)
    scorelabel2.grid(row=7, column=0, padx=2, pady=10)
    # scorevalue
    timerlabel = Label(f1, textvariable=timerno, bg=hex_buttons, fg="ghostwhite", font=("Impact", 27), width=5)
    timerlabel.grid(row=1, column=0, padx=2, pady=2)
    # timer
    btn_back = Button(frame3, text="Main Menu", font='impact 30', bg=hex_buttons, fg='ghostwhite', command=MM)
    btn_back.grid(row=2, column=1, padx=10, pady=0)
    # back
    btn_x2 = Button(f1, width="12", text="x2 round\nscore", font='Impact 27', bg=btn_x2_colour, fg=btn_font_x2_colour,
                    command=use_x2)
    btn_x2.grid(row=4, column=0, padx=20, pady=20)
    # x2 points power up
    btn_shuffle = Button(f1, width="12", text="Shuffle rack", font='Impact 27', bg=btn_shuffle_colour, fg=btn_font_shuffle_colour,
                         command=use_shufflerack)
    btn_shuffle.grid(row=5, column=0, padx=20, pady=20)
    # shuffle rack again

    timeron = True
    #print("ticked", ticked)
    if ticked:
        timefunc()  # prevents doubling up


def confirm_entry(username):
    #print("Username passed into confirm entry", username)
    if (len(str(username)) < 7 or len(str(username)) > 17) and username.isalnum():
        highscore_prompt.set("Invalid username. Try again!")
        return
    global intscore
    highscore_prompt.set("Highscore will be updated shortly")
    db(username, intscore)
    return


# Function to close the app
def close():
    root.destroy()


# define a function for exiting program when esc is pressed
def on_esc_press(event):
    root.destroy()


# Create a new thread for the keyboard listener
listener_thread = threading.Thread(target=keyboard.on_press_key, args=('esc', on_esc_press))
listener_thread.daemon = True  # Set the thread to be a daemon thread

# Start the keyboard listener thread
listener_thread.start()

# end of gui section###########


MM()
root.mainloop()


