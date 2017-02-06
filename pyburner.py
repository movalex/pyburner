from __future__ import print_function
from csv_parser import *
import os
import sys
import csv
import socket
import platform
import subprocess
import tkSimpleDialog


try:
    # python 3
    from tkinter import filedialog, messagebox
    import tkinter as tk
    from tkinter.ttk import Style
    import configparser
    from tkinter.font import Font, nametofont
except ImportError:
    # python 2
    import Tkinter as tk
    from ttk import Style
    from tkFont import Font, nametofont
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog
    import ConfigParser as configparser

try:
    FileNotFoundError
except NameError: 
    # for Python2
    FileNotFoundError = IOError

os_name = platform.system()
bgcolor = '#333333'
fgcolor = '#f0f0f0'

def truncate_file(file):
    try:
        f = open(file, 'r+')
        f.truncate()
    except FileNotFoundError: 
        pass


def add_quotes(txt):
    return '"{}"'.format(txt)


def config_reader(section):
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    config_dict = {}
    options = cfg.options(section)
    for option in options:
        try:
            config_dict[option] = cfg.get(section, option)
            if config_dict[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            config_dict[option] = None
    return config_dict


def config_writer(a, m, v):
    Config = configparser.ConfigParser()
    Config.read('config.ini')
    Config.set(a, m, v)
    with open('config.ini', 'w') as cfgfile:
        Config.write(cfgfile)


class MyTextSettings(tk.Text):

    def set_frames(self, frame):
        self.insert(tk.END, frame)
        self.see(tk.END)

    def set_text(self, text):
        self.insert(tk.END, text+'\n', 'txt_indent')
        self.see(tk.END)
        if os_name == 'Darwin':
            myfont = Font(family="Lucida Console", size=11)
        elif os_name == 'Windows':
            myfont = Font(family="Consolas", size=9)

        self.configure(font=myfont)

    def clear_all(self):
        self.delete("1.0", tk.END)
        
    def clear_help(self):
        self.clear_all()
        self.set_text('Use "File --> Open" to choose .csv or .txt file')
        

class MainApplication(tk.Tk):
    """main GUI"""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.style = Style()
        self.style.theme_use('alt')
        self.geometry('+300+100')
        self.title('pyBurner')
        self.configure(bg=bgcolor)
        
        if os_name == 'Darwin':
            self.customFont = Font(family="Lucida Console", size=10)
            txt_area = [18,50]
        elif os_name == 'Windows':
            txt_area = [18,48]
            self.customFont = nametofont("TkDefaultFont")
            self.customFont.configure(size=9)       
        # text area
        frame1 = tk.Frame(self)
        frame1.configure(background=bgcolor)
        frame1.grid(row=0, column=0, sticky='w')

        scrollbar = tk.Scrollbar(frame1)
        self.text = MyTextSettings(frame1,
                                   height=txt_area[0], 
                                   width=txt_area[1],
                                   wrap=tk.WORD,
                                   yscrollcommand=scrollbar.set)
        self.text.tag_configure('txt_indent', lmargin1=5)
        self.text.pack(side=tk.LEFT, expand=True)
        scrollbar.configure(highlightcolor=bgcolor, command=self.text.yview)      
        scrollbar.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        
        # labels area
        frame2 = tk.Frame(self)
        frame2.configure(background=bgcolor, highlightthickness=0)
        frame2.grid(sticky='we', padx=(5,0), pady=10)



        self.L1 = tk.Label(frame2, font=self.customFont)
        self.L1.grid_propagate(False)
        self.L1.grid(row=1, column=0, sticky='w')
        #self.L2 = tk.Label(frame2, width=5, text='', font=self.customFont)
        #self.L2.grid(row=1, column=1)
        self.entry = tk.Entry(frame2, width=5, font=self.customFont)
        self.entry.grid(row=1, column=2, sticky='w', padx=(28,6))


        # buttons area
        submit_button = tk.Button(frame2, text='submit', command=self.get_server_entry, font=self.customFont)
        submit_button.configure(highlightbackground=bgcolor)
        submit_button.grid(row=1, column=3, padx=(0,3), sticky='w')
        self.bind('<Return>', self.get_server_entry)
        self.run_button = tk.Button(frame2, text='run', command=self.run_app, font=self.customFont)
        self.run_button.configure(highlightbackground=bgcolor)
        self.run_button.grid(row=1, column=4, padx=(0,3))
        self.bind('<Control-r>', self.run_app)
        reset_button = tk.Button(frame2, text='reset', command=self.cleanup, font=self.customFont)
        reset_button.configure(highlightbackground=bgcolor)
        reset_button.grid(row=1, column=5, sticky='we')
        self.var = tk.IntVar()
        checkbutton1 = tk.Checkbutton(frame2,
                                      background="#535353",
                                      text='open result',
                                      variable=self.var,
                                      font=self.customFont)
        checkbutton1.configure(height=1,  fg="#a7a7a7")
        checkbutton1.grid(row=2, column=0, sticky='w')
        showall_button = tk.Button(frame2, text='all jobs', highlightbackground=bgcolor, command=self.show_all)
        showall_button.grid(row=2, column=3, sticky='w')
        showall_button.config(font=self.customFont)

        close_button = tk.Button(frame2, text='close', command=self.quit_app, font=self.customFont)
        close_button.configure(highlightbackground=bgcolor)
        close_button.grid(row=2, column=4, columnspan=2, sticky='we')

        self.L1.configure(background=bgcolor, foreground=fgcolor, highlightthickness=0)
        #self.L2.configure(background=bgcolor, foreground=fgcolor, highlightthickness=0)
        self.entry.configure(background="#535353", foreground=fgcolor, highlightthickness=0)
        self.text.configure(foreground=fgcolor, background=bgcolor, highlightthickness=1)

        # file menu
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        self.config(menu=menubar)
        filemenu.add_command(label='Open',
                             command=self.csv_open,
                             accelerator="Ctrl+L")
        filemenu.add_command(label='Preferences', 
                             command=OpenPrefs)
        filemenu.add_separator()
        filemenu.add_command(label='Exit',
                             command=self.quit_app,
                             accelerator='Ctrl+Q')
        self.bind("<Control-l>", self.csv_open)
        self.bind("<Control-q>", self.quit_app)
        menubar.add_cascade(label='File', menu=filemenu)

        self.text.clear_help()
        self.load_defaults()


    def cleanup(self):
        self.text.clear_help()
        self.load_defaults()

    def load_defaults(self):
        self.var.set(1)
        self.L1.config(text='press CRTL+L to load file',)
        self.entry.delete("0", tk.END)
        self.job_name = None
        self.selected_server = None
        self.file_contents = []
        self.servers = []
        self.all_servers = []
        self.SCENE_LOOKUP = config_reader('settings')['path']
        self.PRIORITY = config_reader('settings')['priority']
        self.RENDER_MANAGER = config_reader('settings')['manager']
        self.VERSION = config_reader('settings')['version']
        self.the_csv_file = None

    def show_all(self):
        window1=tk.Toplevel()
        window1.geometry('500x300+680+380')
        txt_all = MyTextSettings(window1)
        txt_all.pack()
        txt_all.set_text('Hello!')

    def csv_open(self, *args):
        self.text.clear_all()
        self.the_csv_file = filedialog.askopenfilename(
                        initialdir='{}/Desktop'.format(os.path.expanduser('~')),
                        filetypes=(('Text File', '*.txt'),
                                   ('CSV file', '*.csv'),
                                   ('All Files', '*.*')),
                        title='Choose a file')
        if self.the_csv_file:
            self.job_name = get_job_name(self.the_csv_file)
            self.all_servers = servers_sorted(self.the_csv_file)
            self.text.set_text("Found {} servers in file:".format(
                              len(self.all_servers)))
            for num, serv in enumerate(self.all_servers):
                self.text.set_text('{}) {}'.format(num, serv))
            #self.L2.config(text='0-{}'.format(len(self.all_servers)-1))
            self.L1.configure(text='Enter server number (0-{})'.format(len(self.all_servers)-1))
            self.entry.delete("0", tk.END)
            self.entry.focus()
        else:
            self.text.clear_help()

    def get_server_entry(self, *args):
        server_num = self.entry.get()
        try:
            if int(server_num) >= 0:
                self.frames_list = list(return_frames(self.the_csv_file, self.all_servers[int(server_num)]))
                self.selected_server = self.all_servers[int(server_num)]
                self.text.set_text('you\'ve selected server #{}'.format(server_num))
                self.text.set_text('\'{}\''.format(self.selected_server))
                self.text.set_text(r'Now press "run" button (CTRL+r) to choose .max file you wish to re-render')
                self.run_button.focus()
            else:
                self.text.set_text('enter positive number, dammit!')
        except (ValueError, IndexError) :
            self.text.set_text('enter correct number, please')

    def choose_max_file(self):

        open_maxfile = filedialog.askopenfilename(
                  initialdir=self.SCENE_LOOKUP,
                  title='Choose MAX file')
        if open_maxfile:
            norm_path = os.path.normpath(open_maxfile)
            self.make_bat(norm_path)
        else:
            self.text.set_text('\nClick "run" and choose .max file!')
            return

    def open_result(self, folder):
        # show the bat-file folder in Windows Explorer or macOS Finder
        if os_name == 'Darwin':
            subprocess.Popen(['open', folder])
        elif os_name == 'Windows':
            subprocess.Popen('explorer /open, {}'.format(folder))
        else:
            pass

    def run_app(self, *args):
        if self.job_name and self.selected_server:
            self.text.set_text('\nThese frames will be re-rendered:')
            for frame in self.frames_list:
                self.text.set_frames('{}, '.format(frame))
            self.text.set_frames('\n')
            self.choose_max_file()
        elif not self.job_name:
            self.text.set_text("You should select jobs file first")
        elif not self.selected_server:
            self.text.set_text("Enter server number and submit!")

    def make_bat(self, maxpath):

        max_version = '\"C:\\Program Files\\Autodesk\\3ds Max {}\\3dsmaxcmd.exe\"'.format(self.VERSION)
        quoted_max_file = add_quotes(maxpath)
        max_folder, max_file = os.path.split(maxpath)
        filename, _ = os.path.splitext(max_file)
        bat_file = os.path.join(max_folder, '{}_rerender.bat'.format(filename))
        truncate_file(bat_file)
        try:
            ip_address = socket.gethostbyname(self.RENDER_MANAGER)
        except socket.gaierror:
            err_message = 'Check your network connection.\n Is your render server available?'
            self.text.set_text('\n{}'.format(err_message))
            messagebox.showerror('Network Error', err_message)   
            return
        with open(bat_file, 'a') as bat:
            print(max_version, quoted_max_file, file=bat, end=' ')
            print('-frames:', file=bat, end='')
            for frame in self.frames_list:
                print(frame, file=bat, end=',')
            print(' -submit:', ip_address,
                  file=bat, end='')
            print(' -jobname: {}_{}_rerender'.format(self.job_name,
                                                     self.selected_server),
                                                     file=bat, end='')
            print(' -priority:{}'.format(self.PRIORITY), file=bat)
        if self.var.get() == 1:
            self.text.set_text('\nOpening folder...\n')
            self.open_result(max_folder)
            self.var.set(0)  # uncheck button to prevent multiple windows
        else:
            pass
        self.text.set_text('Done!\nPlease, check "{}"\nat {}'.format(
                          os.path.split(bat_file)[1], max_folder))
        self.entry.focus()

    def quit_app(self, *args):
        sys.exit(0)


class OpenPrefs(tk.Toplevel):

    def __init__(self):
        tk.Toplevel.__init__(self)
        manager = config_reader('settings')['manager']

        self.config(bg=bgcolor, takefocus=True)
        self.title('Preferences')
        self.geometry('300x150+680+100')
        enter_label = tk.Label(self, text='render manager: ')
        enter_label.configure(bg=bgcolor, fg=fgcolor)
        enter_label.grid(row=0, column=0)

        serv_entry = tk.Entry(self)
        serv_entry.insert(tk.END, manager)
        serv_entry.configure(bg='#535353', fg=fgcolor)
        serv_entry.grid(row=0, column=1)
        
        self.bind('<Tab>', serv_entry.select_range(0, tk.END))
        #serv_entry.focus()
        self.sumbit_manager = tk.Button(self, text='ok', command=lambda:get_entry('manager'))
        self.sumbit_manager.grid(row=0, column=2)

        def get_entry(option):
            config_writer('settings', option, serv_entry.get())


class MyDialog(tkSimpleDialog.Dialog):

    def body(self, master):

        tk.Label(master, text="First:").grid(row=0)
        tk.Label(master, text="Second:").grid(row=1)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def validate(self):
        try:
            first = int(self.e1.get())
            second = int(self.e2.get())
            self.result = first, second
            return 1
        except ValueError:
            print('Enter numbers')
            return 0

    def apply(self):
        n,m = self.result
        print(n,m)
        
if __name__ == '__main__':
    app = MainApplication()
    app.resizable(width=tk.FALSE, height=tk.FALSE)
    app.mainloop()