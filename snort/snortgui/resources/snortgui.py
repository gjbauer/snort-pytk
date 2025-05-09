#!/usr/bin/python3
import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
import passw

#sudo_password = tk.simpledialog.askstring("Password", "\nEnter your administrator password:\n", show='*')
# sudo_password

try:
	# create the main window
	root = tk.Tk()
	root.title('SNORT IDS GUI')
	root.geometry('1200x650+1+1')
	root.resizable(False, False)

	# create a canvas to display the background image
	canvas = tk.Canvas(root, width=1200, height=650)
	canvas.pack(fill=tk.BOTH, expand=True)

	# load and display the background image
	home_dir = os.path.expanduser("~")
	rel_path = ".snortgui/info/images/snort.jpg"
	abs_path = os.path.join(home_dir, rel_path)
	img = Image.open(abs_path)
	img = img.resize((1200, 650), Image.LANCZOS)
	img = ImageTk.PhotoImage(img)
	canvas.create_image(0, 0, image=img, anchor=tk.NW)

	# define the functions for the buttons
	def generate_rules():
		command='sudo -S python3 ~/.snortgui/rule_generator.py'
		process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, preexec_fn=os.setsid)
		process.stdin.write(passw.getPass().encode('utf-8') + b'\n')
		process.stdin.flush()

	def open_files():

		filename = filedialog.askopenfilename(initialdir='/etc/snort/rules/', title='Select File', filetypes=(('SNORT Rules', '*.rules'), ('config', '*.conf')))
		if filename:
			command='sudo -S gedit '+filename
			process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, preexec_fn=os.setsid)
			process.stdin.write(passw.getPass().encode('utf-8') + b'\n')
			process.stdin.flush()
		else:
			messagebox.showerror("Error", "ⓘ Incorrect password, try again.")

	def run_ids():
		command='sudo -S python3 ~/.snortgui/run_ids.py'
		process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, preexec_fn=os.setsid)
		process.stdin.write(passw.getPass().encode('utf-8') + b'\n')
		process.stdin.flush()

	def exit_app():
		if messagebox.askokcancel(title='Exit', message='Are you sure?'):
			root.destroy()

	def log_analyser():
		command="sudo -S python3 ~/.snortgui/loganalyzer.py"
		process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, preexec_fn=os.setsid)
		process.stdin.write(passw.getPass().encode('utf-8') + b'\n')
		process.stdin.flush()

	def about():
		command="python3 ~/.snortgui/about.py"
		os.system(command)

	def help():
		command="python3 ~/.snortgui/help.py"
		os.system(command)
 
  
	# create the buttons
	button_width, button_height = 20, 2
	button_font = ('TkDefaultFont', 15)
	button_bg, button_fg = '#000', '#fff'
	button_active_bg, button_active_fg = '#f00', '#fff'

	generate_button = tk.Button(root, width=button_width, height=button_height, text='GENERATE RULES', font=button_font,
	bg=button_bg, fg=button_fg, relief='groove', cursor='hand2', activebackground=button_active_bg,
	activeforeground=button_active_fg, command=generate_rules)
	generate_button.place(x=45, y=100)

	open_button = tk.Button(root, width=button_width, height=button_height, text='CONFIGURATION FILES', font=button_font,
	bg=button_bg, fg=button_fg, relief='groove', cursor='hand2', activebackground=button_active_bg,
	activeforeground=button_active_fg, command=open_files)
	open_button.place(x=45, y=225)

	run_button = tk.Button(root, width=button_width, height=button_height, text='LOG ANALYZER', font=button_font,
	bg=button_bg, fg=button_fg, relief='groove', cursor='hand2', activebackground=button_active_bg,
	activeforeground=button_active_fg, command=log_analyser)
	run_button.place(x=45, y=350)

	run_button = tk.Button(root, width=button_width, height=button_height, text='RUN SNORT', font=button_font,
	bg=button_bg, fg=button_fg, relief='groove', cursor='hand2', activebackground=button_active_bg,
	activeforeground=button_active_fg, command=run_ids)
	run_button.place(x=45, y=475)


	# create the menu bar
	menu_bar = tk.Menu(root)

	file_menu = tk.Menu(menu_bar, tearoff=0)
	file_menu.add_command(label='Help',command=help )
	file_menu.add_command(label='Exit', command=exit_app)
	menu_bar.add_cascade(label='Option', menu=file_menu)
	file_menu1 = tk.Menu(menu_bar, tearoff=0)
	file_menu1.add_command(label='SNORT-GUI', command=about)
	menu_bar.add_cascade(label='About', menu=file_menu1)
	root.config(menu=menu_bar)
	root.mainloop()

except tk.TclError:
    exit()
