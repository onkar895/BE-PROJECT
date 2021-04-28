import subprocess
import ctypes, sys
import re
import threading
import tkinter as tk
import time
import sys
import os
import ctypes
import random
from tkinter import *
from tkinter.ttk import *
import webbrowser
#netsh interface ipv4 show interfaces
global info_variable
info_variable = 0
class Utils(object):
    def __init__(arg):
        pass

    def close_info(arg):
        global info_variable
        info_window.destroy()
        info_variable = 0

    def close_everything(arg):
        try:
            window.destroy()
            info_window.destroy()
        except:
            pass
    def open_files(arg):
        #For vide extraction and enhancement
        from tkinter import filedialog
        global window_filename,enc_file_list,mylist,enc_file_scroll,file_to_encrypt_label
        enc_file_list = []
        window_filename =  filedialog.askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
        enc_file_list.append(window_filename)
        enc_video = enc_file_list[0][0].strip('\n')
        mylist.insert(END,enc_video + "------ selected for frame extraction"," Extraction started output_dir = 'frames'")
        def extraction_function_thread(enc_video):
            time.sleep(3)
            os.system('python video_extraction.py -v "'+enc_video+'" -ex')
            print("extraction Completed")

            progress1 = Progressbar(window,orient=HORIZONTAL,length=1200,mode='determinate')
            progress1.place(x='70',y='670',height=20)

            for i in range(0,5):
                progress1['value'] = 84 + i*15/5
                mylist.insert(END,"Extracting Frames.....%" + str(84 + i*15/5))
                time.sleep(0.5)
            progress1['value'] = 100
            mylist.insert(END,"###- Extraction Complete \n Starting GAN process")
            progress.place_forget()
            progress1.place_forget()
        extraction_thread = threading.Thread(target=extraction_function_thread,args=(enc_video,))
        extraction_thread.start()

        def check_file_status_function():
            global progress
            progress = Progressbar(window,orient=HORIZONTAL,length=1200,mode='determinate')
            progress.place(x='70',y='670',height=20)
            for i in range(0,20):
                time.sleep(1)
                r = i*15 / 5
                progress['value'] = i*15 / 5

                mylist.insert(END,"Extracting Frames.....%" + str(i*15 / 5))
            for i in range(0,10):
                time.sleep(1)
                progress['value'] = r + i*10 / 20
                mylist.insert(END,"Extracting Frames.....%"+ str(r + i*15 / 5))
        extraction_check_thread = threading.Thread(target=check_file_status_function)
        extraction_check_thread.start()
        return enc_file_list

    def open_single_file(arg):
        from tkinter import filedialog
        global window_filename,enc_single_file_list,enc_file_scroll,file_to_encrypt_label
        enc_single_file_list = []
        window_filename =  filedialog.askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
        enc_single_file_list.append(window_filename)
        print(enc_single_file_list[0])
        return enc_single_file_list

    def open_info(arg):
        global info_window,info_variable

        if info_variable == 0:

            info_window = tk.Tk() #creates window
            info_window.tk.call('tk', 'scaling', 2.0)
            info_window.geometry("750x750")
            info_window.resizable(width=False,height=False)
            info_window.title("Info")
            info_window.configure(bg='#333338')
            info_window.protocol('WM_DELETE_WINDOW',x.close_info)
            info_file_scroll = tk.Scrollbar(info_window,width=20,elementborderwidth=0,highlightcolor='green',bg='green',bd=0,activebackground='green')
            info_file_scroll.place(x='700',y='130',height=600)#anchor='w',fill='y',side='right',pady=50,padx=20)

            info_list = Listbox(info_window,width='80',height='7',yscrollcommand=info_file_scroll.set,bg='#d6d6c2',bd=0,fg='black')
            info_list.place(x='30',y='130',height=600)

            here = tk.Label(info_window,text = "Usage and Contributors Info" ,fg="white",bg="#333338")
            here.pack()
            info_variable = 1
            try:
                info_data = open('info_data.txt','r+')
                infolines = info_data.readlines()
                info_data.close()

                for i in infolines:
                    info_list.insert(END,'   ' + i)

                    #print(i)
            except:
                pass
            """
            code goes here
            """
            info_window.mainloop()



try:
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    if is_admin():
        x = Utils()
        global window
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        window = tk.Tk() #creates window
        window.tk.call('tk', 'scaling', 2.0)
        window.geometry("1350x700")
        window.resizable(width=False,height=False)
        window.title("Under Water Image Enhancement")
        try:
            window.iconbitmap('m.ico')
        except:
            oh = 'my god'
        window.configure(bg='#333338')
        button = tk.Button(text ="Change",height = 1,width=10,fg="#d6d6c2",bg="blue")
        entry  = tk.Entry(width=20)
        label = tk.Label(text = "Under Water Image Enhancement" ,fg="#d6d6c2",bg="#333338")
        label.place(relx=.5,rely=.5,anchor="c")
        window.protocol('WM_DELETE_WINDOW',x.close_everything)

        def clear_label():
            global mylist
            label.place_forget()
            label2 = tk.Label(text="Under Water Image Enhancement GUI",fg='white',bg='#333338')
            label2.pack()

            label3 = tk.Label(text="Current Process...",fg='white',bg='#333338')
            label3.place(x='65',y='200')

            open_files_button = tk.Button(text=' Enhance Video ',activebackground='black',highlightcolor='black',bd=1,relief='flat',height=0,width=15,fg='white',bg='#338237',command=x.open_files,master=window)
            open_files_button.pack(anchor='nw',pady=100,padx=50,side='left')

            info_button = tk.Button(text='Info',activebackground='black',highlightcolor='black',bd=1,relief='flat',height=0,width=7,fg='white',bg='#338237',command=x.open_info,master=window)
            info_button.place(x='1250',y='30')


            open_single_files_button = tk.Button(text=' Enhance Image ',activebackground='black',highlightcolor='black',bd=1,relief='flat',height=0,width=15,fg='white',bg='#338237',command=x.open_single_file,master=window)
            open_single_files_button.pack(anchor='nw',pady=100,padx=5,side='left')

            enc_file_scroll = tk.Scrollbar(window,width=20,elementborderwidth=0,highlightcolor='green',bg='green',bd=0,activebackground='green')
            enc_file_scroll.place(x='1290',y='250',height=400)#anchor='w',fill='y',side='right',pady=50,padx=20)

            mylist = Listbox(window,width='120',height='7',yscrollcommand=enc_file_scroll.set,bg='#d6d6c2',bd=0,fg='black')
            mylist.place(x='70',y='250',height='400')

            label4 = tk.Label(text="Source Code:",fg='white',bg='#333338')
            label4.place(x='800',y='200')

            link = tk.Label(window, text="https://github.com/lawlie8/BE_PROJECT", fg="blue",bg='#333338', cursor="hand2")
            link.pack(anchor='nw',pady=170,padx=75,side='right')
            link.bind("<Button-1>", lambda event: webbrowser.open(link.cget("text")))

            #open_files()
        label.after(3000,clear_label)

        #next here


    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    try:
        window.mainloop()  #main window opens here
    except:
        tomato = 'potato'
    is_admin()
except:
    egg = 'omelete'
