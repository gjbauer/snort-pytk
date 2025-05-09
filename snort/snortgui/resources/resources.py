import subprocess,os, socket
import tkinter as tk
from tkinter import ttk,messagebox, simpledialog
from tkinter import *
import passw

#sudo_password = tk.simpledialog.askstring("Password", "\nEnter your administrator password:\n", show='*')

if os.path.exists('setup.conf'):
    messagebox.showinfo("Your Application is ready","All resources are downloaded and ready to be launched")
    os.system('python3 ~/.snortgui/snortgui.py')

else:
    #tkinter window declaration : Progressbar
    try:
    	command = 'mkdir -p ~/.snortgui/'
    	process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, preexec_fn=os.setsid)
    	process.stdin.write(passw.getPass().encode('utf-8') + b'\n')
    	process.stdin.flush()
    except:
    	print("~/.snortgui already exists")
    
    command = 'cp -r resources/* ~/.snortgui/'
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, preexec_fn=os.setsid)
    process.stdin.write(passw.getPass().encode('utf-8') + b'\n')
    process.stdin.flush()
    
    try:
    	command = 'mkdir -p ~/.local/bin/'
    	process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, preexec_fn=os.setsid)
    	process.stdin.write(passw.getPass().encode('utf-8') + b'\n')
    	process.stdin.flush()
    except:
    	print("~/.local/bin exists")
    
    
    command = 'chmod +x ~/.local/bin/snortgui'
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, preexec_fn=os.setsid)
    process.stdin.write(passw.getPass().encode('utf-8') + b'\n')
    process.stdin.flush()
    
    snort = Tk()
    snort.geometry('300x120')
    snort.title('Setup Wizard')

    #########################
    #exit
    def mQuit():
        mexit=messagebox.askokcancel(title='Exit',message='Are you sure?')
        if mexit>0:
            snort.destroy()
            return
    #main
    def run_commands():
        with open('resources/info/requirements.txt','r') as f:
            commands = f.readlines()
        i=1
        button1.place_forget()
        button['text'] = f'Downloading Components ({i}/{len(commands)})'
        button.place(x=30,y=80)
        message_label['text']='Installation in progress...'
        message_label.place(x=45,y=10)
        

        progress_bar['maximum'] = len(commands)

        for i, command in enumerate(commands):
            command = command.strip()
            button['text'] = f'Downloading Components ({i+1}/{len(commands)})'
            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, preexec_fn=os.setsid)
            process.stdin.write(passw.getPass().encode('utf-8') + b'\n')
            process.stdin.flush()
            process.wait()  # wait for the subprocess to complete before moving on to the next command
            progress_bar['value'] = i+1
            snort.update()

        button['text']='Download Completed!'
        button.place(x=63,y=80)
        

        with open('setup.conf','w') as f:
            f.write("This is a configuration file to notify the wizard a first time installation")
           
        username = tk.simpledialog.askstring("Username", "\nEnter your username:\n", show='*')
        hostname = socket.gethostname()
        
        command='sudo -S chown -R '+username+":"+username+" ~/.snortgui"
        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, preexec_fn=os.setsid)
        process.stdin.write(passw.getPass().encode('utf-8') + b'\n')
        process.stdin.flush()
        
        result=messagebox.askyesno('Installation complete','Click Yes to start SNORT GUI')
        if result==True:
            snort.destroy()
            os.system("python3 ~/.snortgui/snortgui.py")
        else:
            snort.destroy()


    #progress bar css
    style=ttk.Style()
    style.theme_use('default')
    style.configure('Custom.Horizontal.TProgressbar', foreground='#51C9C2', background='#C7F7F5', thickness=25)
    progress_bar=ttk.Progressbar(snort, orient='horizontal', mode = 'determinate', style='Custom.Horizontal.TProgressbar',length=200)
    progress_bar.pack(pady=40)

    #button css
    button=tk.Button(snort,text='Proceed', command=run_commands)
    button1=tk.Button(snort,text='Cancel', command=mQuit)
    button.place(x=155,y=80)
    button1.place(x=65,y=80)
    
    #messagelabel
    message_label=tk.Label(snort,text='Click Proceed to download resources')
    message_label.place(x=30,y=10)
    snort.mainloop()
