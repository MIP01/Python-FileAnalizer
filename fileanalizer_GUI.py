from threading import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import tkinter, tkinter.scrolledtext
import threading
import os
import sys
import glob
import time
import hashlib
import webbrowser
#self-made
import quarantaene 

os_name = sys.platform
verzeichnisse = []
files = []
partitionen = []
terminations = []



if "win" in os_name:
    if not os.path.exists("FileAnalizer\\Quarantine\\"):
        os.makedirs("FileAnalizer\\Quarantine\\")
    if not os.path.exists("FileAnalizer\\Database\\"):
        os.makedirs("FileAnalizer\\Database")
    quarantine_folder = "FileAnalizer\\Quarantine\\*"
    file_to_quarantine = "FileAnalizer\\Quarantine\\"
else:
    if not os.path.exists("FileAnalizer//Quarantine//"):
        os.makedirs("FileAnalizer//Quarantine//")
    if not os.path.exists("FileAnalizer//Database//"):
        os.makedirs("FileAnalizer//Database//")
    quarantine_folder = "FileAnalizer//Quarantine//*"
    file_to_quarantine = "FileAnalizer//Quarantine//"

files_len = counter = 0
main = None
update_button = None
scan_button = None
quit_button = None
b_restore = None
b_restore_all = None
b_add_file = None
text_box = None
e = None
li = None
rb1 = None
rb2 = None
method = None
bgc = None
fgc = None
special = None
special_text = None

daytime = int(time.strftime("%H", time.localtime()))

#Adjusting the brightness for the current day_time
#It's totally unnecessary but I wanted to play around a little
if daytime >= 18 or daytime <= 4:
    bgc = "black"
    fgc = "white"
    special = "brown"
    special_text = "（°_°）☽ ☆ Good evening " + os.getlogin() + " ☆ ☾（°_°）\n"
elif daytime > 4 and daytime <= 8:
    special_text = "＼(o￣∇￣o)/ Good morning " + os.getlogin() + " ＼(o￣∇￣o)/\n"
    bgc = "white"
    fgc = "black"
    special = "orange"
else:
    bgc = "white"
    fgc = "black"
    special = "#1ccaed"
    special_text = "\(≧∇≦)/ Welcome " + os.getlogin() + " \(≧∇≦)/\n"

def quarantine():
    global text_box
    global terminations
    global li
    global b_restore
    global b_restore_all
    global b_add_file
        

    k = 0
    while True:
        tmp = len(li.get(k))
        if tmp == 0:
            break
        else:
            li.delete(0, tmp)
            k += 1
    li.update()
        
        
    terminations = glob.glob(quarantine_folder)
    if terminations == []:
        text_box.insert(END, "[ + ] No files in quarantine\n", "positive")
        text_box.tag_config('positive', foreground="green")
        text_box.see(END)
        text_box.update()
    else:
        text_box.insert(END, "[ + ] Files in quarantine:\n", "positive")
        text_box.tag_config('positive', foreground="green")
        text_box.see(END)
        text_box.update()
        for i in terminations:
            text_box.insert(END, "[ * ] " + i + "\n", "info")
            text_box.tag_config("info", background = "red")
            text_box.see(END)
            text_box.update()
            li.insert(END, i)
            li.update()
        
    b_restore["command"] = lambda:button_action_handler("restore")
    b_restore_all["command"] = lambda:button_action_handler("restore_all")
    b_add_file["command"] = lambda:button_action_handler("add_file")
    

        
def restore(file, ALL):
    global li
    global text_box
    global terminations

    if len(terminations) != 0:
        if ALL == 1:
            for i in range(len(terminations)):
                quarantaene.decode_base64(terminations[i])
                text_box.insert(END, "[ + ] Successfully restored\n" + terminations[i] + "\n", 'positive')
                text_box.tag_config('positive', foreground="green")
                text_box.see(END)
                text_box.update()
                li.delete(0, len(terminations[i]))
                li.update()
        elif ALL == 0:
            quarantaene.decode_base64(file)
            li.delete(ACTIVE, len(file))
            text_box.insert(END, "[ + ] Successfully restored\n" + file + "\n", "positive")
            text_box.tag_config("positive", foreground="green")
            text_box.see(END)
            text_box.update()
            
        terminations = glob.glob(quarantine_folder)
        for i in terminations:
            li.insert(END, i)
        li.update()
        
    else:
        text_box.insert(END, "[ - ] Unable to locate any files\n", "negative")
        text_box.tag_config("negative", foreground="red")
        text_box.see(END)
        text_box.update()
    

def add_file_to_quarantine():
    global li
    global terminations
    
    file = askopenfilename()
    file = file.replace("/", "\\")
    quarantaene.encode_base64(file, file_to_quarantine)
    text_box.insert(END, "[ + ] Moved to quarantine:\n" + file + "\n", "positive")
    text_box.tag_config("positive", foreground="green")
    text_box.see(END)
    text_box.update()
    li.update()

    k = 0
    while True:
        tmp = len(li.get(k))
        if tmp == 0:
            break
        else:
            li.delete(0, tmp)
            k += 1
    li.update()

    terminations = glob.glob(quarantine_folder)
    for i in terminations:
        li.insert(END, i)
        li.update()

def update():
    webbrowser.open_new("https://virusshare.com/hashes")
    text_box.insert(END, "[ + ] opening browser\n", 'positive')
    text_box.tag_config('positive', foreground="green")
    text_box.see(END)
    text_box.update()
    text_box.insert(END, "[ ! ] rename file to VirusShare.txt\n", 'danger')
    text_box.tag_config('danger', foreground="red")
    text_box.see(END)
    text_box.update()
    
def scan():
    global text_box  

    match = False
    file = askopenfilename()
    file = file.replace("/", "\\")
    start = time.time() 
    text_box.insert(END, "[ * ] Scanning " + file + "\n")
    text_box.see(END)
    text_box.update()
    with open(file,"rb") as f:
            bytes = f.read()
            content = hashlib.md5(bytes).hexdigest();
            text_box.insert(END, "MD5-Hash: " + content + "\n")
            text_box.see(END)
            text_box.update()
            with open("FileAnalizer\\Database\\VirusShare.txt",'r') as f:
                lines = [line.rstrip() for line in f]
                for line in lines:
                      if str(content) == str(line.split(";")[0]):
                            match = True
    
                f.close()
                
    
    text_box.insert(END, "[ * ] Scan duration: {0}\n".format(round(time.time()-start, 2)))
    text_box.see(END)
    text_box.update()
    if match:
        quarantaene.encode_base64(file, file_to_quarantine)
        text_box.insert(END, "[ ! ] Threat found\n[ ! ] File Has been Quarantine\n", "important")
        text_box.tag_config("important", foreground="red")
        text_box.see(END)
        text_box.update()
    if not match:
        text_box.insert(END, "[ + ] No threat was found\n", "positive")
        text_box.tag_config("positive", foreground="green")
        text_box.see(END)
        text_box.update()
        
    
def clear():
    text_box.delete('1.0', END)
    text_box.insert(END, special_text, "VIP")
    e.delete(0, END)
    e.insert(0, "Quarantine List")


def button_action_handler(s):
    global files_len
    global text_box
    global b_restore
    global b_restore_all
    global b_add_file
    global li
    global rb1
    global rb2
    global method

    if s == "rb1":
        method = 1
        rb1.place_forget()
        rb2.place_forget()
    if s == "rb2":
        method = 2
        rb2.place_forget()
        rb1.place_forget()

    if s == "restore":
        tb = Thread(target=restore, args=(li.get(ACTIVE),0))
        tb.start()
    if s == "restore_all":
        tb = Thread(target=restore, args=(0,1))
        tb.start()
        
    if s == "add_file":
        tb = Thread(target=add_file_to_quarantine)
        tb.start()

    if s == "scan_button":
        tb = Thread(target=scan)
        tb.start()
    if s == "update_button":
        tb = Thread(target=update)
        tb.start()

    if s == "quarantine_button":
        if li.winfo_viewable() == 0 :
            e.place(x = 570, y = 0)
            b_restore.place(x = 570, y = 87)
            b_restore_all.place(x = 570, y = 113)
            b_add_file.place(x = 570, y = 139)
            li.place(x = 570, y = 18.5)
            tb = Thread(target=quarantine)
            tb.start()
        if li.winfo_viewable() == 1:
            e.place_forget()
            b_restore.place_forget()
            b_restore_all.place_forget()
            b_add_file.place_forget()
            li.place_forget()

    if s == "clear_button":
        tb = Thread(target=clear)
        tb.start()
        
def gui_thread():
    global main
    global update_button
    global scan_button
    global clear_button
    global text_box
    global e
    global files_len
    global files
    global li
    global b_restore
    global b_restore_all
    global b_add_file
    global rb1
    global rb2
    global method
    global bgc
    global fgc
    global special_text
                        
    main = tkinter.Tk()
    main.title("FileAnalizer")
    main.wm_iconbitmap("")
    main.configure(bg=bgc)
    main.geometry("750x164")#width x height
    main.resizable(False, False)
    #main.overrideredirect(1)
    hoehe = 2
    breite = 20

    
    #Buttons
    update_button = tkinter.Button(main, bg=bgc, fg=fgc, text = "Update", command=lambda:button_action_handler("update_button"), height = hoehe, width = breite)
    update_button.grid(row = 0, column = 0)
    scan_button = tkinter.Button(main, bg=bgc, fg=fgc, text = "Scan", command=lambda:button_action_handler("scan_button"), height = hoehe, width = breite)
    scan_button.grid(row = 1, column = 0)
    quarantine_button = tkinter.Button(main, bg=bgc, fg=fgc, text = "Quarantine", command=lambda:button_action_handler("quarantine_button"), height = hoehe, width = breite)
    quarantine_button.grid(row = 3, column = 0)
    quit_button = tkinter.Button(main, bg=bgc, fg=fgc, text = "Clear Log", command=lambda:button_action_handler("clear_button"), height = hoehe, width = breite)
    quit_button.grid(row = 4, column = 0, sticky="w")
    b_restore = tkinter.Button(main, bg=bgc, fg=fgc, text = "Restore current", height=0, width = 25, justify=CENTER)
    b_restore_all = tkinter.Button(main, bg=bgc, fg=fgc, text = "Restore all", height = 0, width = 25, justify=CENTER)
    b_add_file = tkinter.Button(main, bg=bgc, fg=fgc, text = "Add file manually", height = 0, width = 25, justify=CENTER)
    b_restore.place(x = 570, y = 120)
    b_restore_all.place(x = 570, y = 145)
    b_add_file.place(x = 570, y = 170)
    b_restore.place_forget()
    b_restore_all.place_forget()
    b_add_file.place_forget()
    
    #Text
    text_box = tkinter.scrolledtext.ScrolledText(main)
    text_box.configure(bg=bgc)
    text_box.configure(fg=fgc)
    text_box.place(height = 164, width = 419,x = 150, y = 0)

    #Entries
    e = tkinter.Entry(main,width = 30)
    e["justify"] = CENTER
    e.insert(0, "Quarantine List")

    #Listbox
    li = tkinter.Listbox(main, height=4, width = 29)
    li.place(x = 570, y = 18.5)
    li.place_forget()
    
    #Intro
    text_box.insert(END, special_text, "VIP")
    text_box.tag_config("VIP", background=special)
    text_box.insert(END, "[ + ] Preparing the program\n", 'positive')
    text_box.tag_config('positive', foreground='green')
    text_box.see(END)
    text_box.update()
    text_box.insert(END, "[ ! ] Add MD5 Sample to 'FileAnalizer\Database'\n", 'suggest')
    text_box.tag_config('suggest', foreground="blue")
    text_box.see(END)
    text_box.update()
    #row_counter += 3
    main.mainloop()

#Executing Threads
t_main = Thread(target=gui_thread)# Main Thread
t_main.start()
time.sleep(1)
time.sleep(5)

