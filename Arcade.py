from cgitb import text
import imp
from re import M
from tkinter import *
from PIL import Image, ImageTk
#from Dragon import dragon as d
from CatchTheClown import clown as c
from HungryRabbit import rabbit as r
from MonsterHunter import MonsterHunter as m
from Snake import snake as snk
from Puzzle import puzzle as p
from Skier import Skier as s
from SpaceInvader import space as spce


root = Tk()
root.geometry('1536x864')
root.iconbitmap('Artboard_1_4x_qNO_icon.ico')
root.title('Arcadia')

#Header area
header = Frame(root, width=1536, height=127, bg="#7289da")
header.grid(columnspan=4, rowspan=1, row=0)

#Display Logo
def display_logo(url, row, column):
    img = Image.open(url)
    #resize image
    img = img.resize((int(img.size[0]/7),int(img.size[1]/7)))
    img = ImageTk. PhotoImage(img)
    img_label = Label(image=img, bg="#7289da")
    img_label.image = img
    img_label.grid(column=column, row=row, sticky=NW, rowspan=2, padx=40 ,pady=10 )
    
display_logo('gamepad.png', 0, 0)

titletext = Label(root, text='Arcadia', font=('Russo One', 40), bg="#7289da", fg='#ffffff', padx=0)
titletext.grid(row=0, column=0, sticky=E)

#Quit button
quit_img = PhotoImage(file = "Quit.png")
quit_btn = Button(root, text="quit", image=quit_img, bg="#7289da", command=root.destroy)
quit_btn.grid(row=0, column=3, sticky=E, padx=60)

#main content
main_content = Frame(root, width=1536, height=750, bg="#99aab5")
main_content.grid(columnspan=4, rowspan=3, row=4) 

#btn creation

snake_thumbnail = PhotoImage(file = "snakenail.png")
game1_btn = Button(root, text="Game1", image=snake_thumbnail, command=snk.snake)

ctc_thumbnail = PhotoImage(file = "ctcnail.png")
game2_btn = Button(root, text="Game2", image=ctc_thumbnail, command=c.catch_the_clown)

hr_thumbnail = PhotoImage(file = "hrnail.png")
game3_btn = Button(root, text="Game3", image=hr_thumbnail, command=r.hungry_rabbit)

mh_thumbnail = PhotoImage(file = "mhnail.png")
game4_btn = Button(root, text="Game4", image=mh_thumbnail, command=m.monster)

si_thumbnail = PhotoImage(file = "sinail.png")
game5_btn = Button(root, text="Game5", image=si_thumbnail, command=spce.spaceInvader)

skier_thumbnail = PhotoImage(file = "skiernail.png")
game6_btn = Button(root, text="Game6", image=skier_thumbnail, command=s.skier)

puzzle_thumbnail = PhotoImage(file = "puzzlenail.png")
game7_btn = Button(root, text="Game7", image=puzzle_thumbnail, command=p.puzzle)

#btn on screen
game1_btn.grid(row=4, column=0)
game2_btn.grid(row=4, column=1)
game3_btn.grid(row=4,column=2)
game4_btn.grid(row=4,column=3)
game5_btn.grid(row=5,column=0, columnspan=2)
game6_btn.grid(row=5, column=1, columnspan=2)
game7_btn.grid(row=5, column=2, columnspan=2)


#Open in Maximised Form
#root.state('zoomed')
#always the last
root.minsize(1536, 864)
root.maxsize(1536, 864)
root.mainloop()
  





#always the last
root.mainloop()
  