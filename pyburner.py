from __future__ import print_function
from csv_parser import *
import os
import sys
import csv
import socket
import platform
import subprocess
import tkPopup

try:
    # python 3
    from tkinter import filedialog, messagebox
    import tkinter as tk
    import configparser
    from tkinter.font import Font, nametofont
except ImportError:
    # python 2
    import Tkinter as tk
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
bgcolor = '#222222'
fgcolor = '#f0f0f0'


def truncate_file(file):
    try:
        with open(file, 'r+') as f:
            f.truncate()
    except FileNotFoundError: 
        pass

           
def add_quotes(txt):
    return '"{}"'.format(txt)


def config_reader(section):
    cfg = configparser.RawConfigParser()
    cfg.read('config.ini')
    config_dict = {}
    options = cfg.options(section)
    for option in options:
        try:
            config_dict[option] = cfg.get(section, option)
            if config_dict[option] == -1:
                print("skip: %s" % option)
        except Exception:
            print("exception on %s!" % option)
            config_dict[option] = None
    return config_dict


def config_writer(section, option, value):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set(section, option, value)
    with open('config.ini', 'w') as cfgfile:
        config.write(cfgfile)


def test_network(r_manager):
    try:
        ip_ = socket.gethostbyname(r_manager)
        return ip_
    except socket.gaierror:
        err_message = 'Check your network connection.\n Is your render server available?'
        messagebox.showerror('Network Error', err_message)
        return 0   


class MyTextSettings(tk.Text):

    def set_text(self, text):
        self.insert(tk.END, text+'\n', 'txt_indent')
        self.see(tk.END)
        if os_name == 'Darwin':
            my_font = Font(family="Lucida Console", size=11)
        elif os_name == 'Windows':
            my_font = Font(family="Consolas", size=9)
        self.configure(font=my_font, bg='#333333', wrap=tk.WORD,
                       fg=fgcolor, highlightthickness=0)

    def clear_all(self):
        self.delete("1.0", tk.END)
        
    def clear_help(self):
        self.clear_all()
        self.set_text('Use "File --> Open" to choose .csv or .txt file')


class MyLabel(tk.Label):
    def __init__(self, *args, **kwargs):
        tk.Label.__init__(self, *args, **kwargs)
        self.configure(bg=bgcolor, fg=fgcolor, highlightthickness=0)


class MainApplication(tk.Tk):
    """main application window
    
    Attributes:
        all_servers (list): returns list of all servers
        customFont (TYPE): defined two types of fonts for mac/win compatibility
        entry (entry field): enter number of the server that failed to render
        file_contents (list): the contents of the Backburner job file
        ip_address (txt): check if the render manager is available and fill it's ip address
        job_name (txt): Backburner job name
        L1 (UI label): label
        PRIORITY (txt): set priority for new Backburner job
        RENDER_MANAGER (txt): render manager name
        run_button (button): run program to create .bat-render file 
        SCENE_LOOKUP (txt): path to the folder with .max files 
        selected_server (txt): failed server name you have chosen 
        server_frames_list (list): list of frames assigned to failed server to be re-rendered
        servers (list): list of servers in Backburner job
        text (txt): text field
        the_csv_file (file): Backburner job exported file 
        var (int): 1 - to call 'open result' function; 0 - to pass
        VERSION (txt): 3DsMax version
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('+300+100')
        self.title('pyBurner')
        self.configure(bg=bgcolor)

        if os_name == 'Darwin':
            self.customFont = Font(family="Lucida Console", size=10)
            txt_area = [18, 53]
        elif os_name == 'Windows':
            txt_area = [18, 48]
            self.customFont = nametofont("TkDefaultFont")
            self.customFont.configure(size=9)       
        # text area
        frame1 = tk.Frame(self)
        frame1.configure(background=bgcolor)
        frame1.grid(row=0, column=0, columnspan=2, sticky='w')

        scrollbar = tk.Scrollbar(frame1)
        self.text = MyTextSettings(frame1,
                                   height=txt_area[0],
                                   width=txt_area[1],
                                   yscrollcommand=scrollbar.set)
        self.text.pack(padx=(4,0), side=tk.LEFT, expand=True)
        scrollbar.configure(command=self.text.yview)      
        scrollbar.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        
        # labels area
        l_frame = tk.Frame(self)
        l_frame.configure(background=bgcolor, highlightthickness=0)
        l_frame.grid(row=1, column=0, sticky='w', padx=(5,0), pady=10)
        self.L1 = MyLabel(l_frame, font=self.customFont)
        self.L1.grid(row=1, column=0, sticky='w', padx=(0, 20))
        self.var = tk.IntVar()
        checkbutton1 = tk.Checkbutton(l_frame,
                                      background=bgcolor,
                                      activebackground=bgcolor,
                                      activeforeground=fgcolor,
                                      selectcolor='#555555',
                                      foreground=fgcolor,
                                      text='open result',
                                      variable=self.var,
                                      font=self.customFont
                                      )
        checkbutton1.grid(row=2, column=0, sticky='w')

        # buttons area
        b_frame = tk.Frame(self)
        b_frame.config(bg=bgcolor)
        b_frame.grid(row=1, column=1,padx=(0, 20), sticky='e')
        submit_button = tk.Button(b_frame, text='submit', command=self.get_server_entry, font=self.customFont)
        submit_button.grid(row=1, column=3, padx=(0,3), sticky='w')
        submit_button.configure(highlightbackground=bgcolor)
        self.bind('<Return>', self.get_server_entry)
        self.run_button = tk.Button(b_frame, text='run', command=self.run_app, font=self.customFont)
        self.run_button.configure(highlightbackground=bgcolor)
        self.run_button.grid(row=1, column=4, padx=(0,3))
        self.bind('<Control-r>', self.run_app)
        reset_button = tk.Button(b_frame, text='reset', command=self.cleanup, font=self.customFont)
        reset_button.configure(highlightbackground=bgcolor)
        reset_button.grid(row=1, column=5, sticky='we')
        showall_button = tk.Button(b_frame, text='all jobs', 
                                   command=self.show_all)
        showall_button.configure(highlightbackground=bgcolor)
        showall_button.grid(row=2, column=3, sticky='w')
        showall_button.config(font=self.customFont)
        close_button = tk.Button(b_frame, text='close', command=self.quit_app, font=self.customFont)
        close_button.configure(highlightbackground=bgcolor)
        close_button.grid(row=2, column=4, columnspan=2, sticky='we')
        self.entry = tk.Entry(b_frame, width=6, font=self.customFont)
        self.entry.grid(row=1, column=2, sticky='w', padx=(0,6))
        self.entry.configure(background="#535353", foreground=fgcolor, highlightthickness=0)

        # file menu
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        self.config(menu=menubar)
        filemenu.add_command(label='Open',
                             command=self.csv_open,
                             accelerator="Ctrl+O")
        filemenu.add_command(label='Preferences',
                             command=self.open_preferences)
        filemenu.add_separator()
        filemenu.add_command(label='Exit',
                             command=self.quit_app,
                             accelerator='Ctrl+Q')
        self.bind("<Control-o>", self.csv_open)
        self.bind("<Control-q>", self.quit_app)
        menubar.add_cascade(label='File', menu=filemenu)
        self.text.clear_help()
        self.load_defaults()

    def cleanup(self):
        self.text.clear_help()
        self.load_defaults()

    def load_defaults(self):
        self.var.set(1)
        self.L1.config(text='press CTRL+O to open file')
        self.entry.delete("0", tk.END)
        self.job_name = None
        self.selected_server = None
        self.file_contents = []
        self.servers = []
        self.all_servers = []
        self.the_csv_file = None
        self.read_config()

    def read_config(self):
        try:
            self.SCENE_LOOKUP = config_reader('settings')['path']
            self.PRIORITY = config_reader('settings')['priority']
            self.RENDER_MANAGER = config_reader('settings')['manager']
            self.VERSION = config_reader('settings')['version']
        except (configparser.NoSectionError, KeyError):
            sample_config=r'''[settings]
priority = 100
path = ~\Documents
version = 2016
manager = localhost'''
            with open('config.ini', 'w') as cfgfile:
                cfgfile.write(sample_config)

    def show_all(self):
        if self.the_csv_file:
            ShowAllWindow('all frames', file=self.the_csv_file)
        else:
            self.text.set_text('open file first')

    @staticmethod
    def open_preferences():
        OpenPrefs('Preferences')

    def csv_open(self, *args):
        self.text.clear_all()
        self.the_csv_file = filedialog.askopenfilename(
                        initialdir='{}/Desktop'.format(os.path.expanduser('~')),
                        filetypes=(('Text File', '*.txt'),
                                   ('CSV file', '*.csv'),
                                   ('All Files', '*.*')),
                        title='Choose a file')
        if self.the_csv_file:
            try:
                self.job_name = get_job_name(self.the_csv_file)
                if self.job_name == None:
                    self.text.set_text('Job name is empty, check file')
                    return
            except csv.Error:
                self.text.set_text('The file is not valid')
                return
            self.all_servers = servers_sorted(self.the_csv_file)
            self.text.set_text('Job name: {}\n'.format(self.job_name))
            self.text.set_text("Found {} servers in file:".format(
                              len(self.all_servers)))
            for num, serv in enumerate(self.all_servers):
                self.text.set_text('{}) {}'.format(num+1, serv))
            self.text.set_text('\nenter server number and submit (hit ENTER)')
            self.L1.configure(text='Enter server number (1-{})'.format(len(self.all_servers)))
            self.entry.delete("0", tk.END)
            self.entry.focus()
        else:
            self.text.clear_help()

    def get_server_entry(self, *args):
        try:
            server_num = int(self.entry.get().strip())
            if server_num > 0:
                self.server_frames_list = list(return_frames(self.the_csv_file, self.all_servers[int(server_num)-1]))
                self.selected_server = self.all_servers[int(server_num)-1]
                self.text.set_text('\nyou\'ve selected server #{}'.format(server_num))
                self.text.set_text("'{}'".format(self.selected_server))
                self.text.set_text(r'Now press RUN button and choose .max file')
                self.run_button.focus()
            else:
                self.text.set_text('enter number greater than zero')
        except (ValueError, IndexError):
            self.text.set_text('enter correct number, please')

    def choose_max_file(self):
        open_maxfile = filedialog.askopenfilename(
                  initialdir=self.SCENE_LOOKUP,
                  filetypes=(('3dMax file', '*.max'),
                            ('All Files', '*.*')),
                  title='Choose MAX file')
        if open_maxfile:
            return open_maxfile
        else:
            self.text.set_text('\nClick "run" and choose .max file!')
            return 0

    def run_app(self, event=None):
        if self.job_name and self.selected_server:
            self.read_config()
            max_file = self.choose_max_file()
            if max_file:
                self.text.set_text('\nThese frames will be rendered again:')
                self.text.set_text(", ".join(self.server_frames_list))
                self.text.set_text('\r')
                self.ip_address = test_network(self.RENDER_MANAGER) #test network path again just in case
                if self.ip_address:
                    norm_path = os.path.normpath(max_file)
                    self.make_bat(norm_path)
                else:
                    self.text.set_text('\nCheck server settings\
                        in preferences and run again')
        elif not self.job_name:
            self.text.set_text("You should select jobs file first")
        elif not self.selected_server:
            self.text.set_text("Enter server number and submit!")

    @staticmethod
    def open_result(folder):
        # show the result folder in Windows Explorer or macOS Finder
        if os_name == 'Darwin':
            subprocess.Popen(['open', folder])
        elif os_name == 'Windows':
            subprocess.Popen('explorer /open, {}'.format(folder))
        else:
            pass

    def make_bat(self, max_path):
        max_version = '\"C:\\Program Files\\Autodesk\\3ds Max {}\\3dsmaxcmd.exe\"'.format(self.VERSION)
        quoted_max_file = add_quotes(max_path)
        max_folder, max_file = os.path.split(max_path)
        filename, _ = os.path.splitext(max_file)
        bat_file = os.path.join(max_folder, '{}_{}.bat'.format(filename, self.selected_server))
        truncate_file(bat_file)
        with open(bat_file, 'a') as bat:
            print(max_version, quoted_max_file, file=bat, end=' ')
            print('-frames:', file=bat, end='')
            print(",".join(self.server_frames_list), file=bat, end=' ')
            print('-submit:', self.ip_address,
                  file=bat, end=' ')
            print('-jobname: {}_{}'.format(self.job_name, self.selected_server), file=bat, end=' ')
            print('-priority:{}'.format(self.PRIORITY), file=bat)
        if self.var.get() == 1:
            self.text.set_text('Opening folder...\n')
            self.open_result(max_folder)
            self.var.set(0)  # uncheck button to prevent multiple windows when re-run
        else:
            pass
        self.text.set_text('Done!\nPlease, check "{}" at {}'.format(
                          os.path.split(bat_file)[1], max_folder))
        self.entry.focus()

    @staticmethod
    def quit_app(event=None):
        sys.exit(0)
        

class OpenPrefs(tkPopup.PopupWindow):

    def body(self, master):
        self.geometry('+680+100')
        self.config(bg=bgcolor, takefocus=True, padx=20, pady=5)
        window_frame = tk.Frame(self)
        enter_label = MyLabel(window_frame, text='render manager: ')
        enter_label.grid(row=0, column=0, sticky='w')
        self.ip_label = MyLabel(window_frame, text='')
        self.ip_label.grid(column=1, sticky='w')
        self.serv_entry = tk.Entry(window_frame)
        self.serv_entry.configure(bg='#535353', fg=fgcolor, width=15)
        self.serv_entry.grid(row=0, column=1,  sticky='we')
        self.manager = config_reader('settings')['manager']
        test_button = tk.Button(window_frame, text='test', command=self.validate)
        test_button.configure(highlightbackground=bgcolor)
        test_button.grid(row=0, column=2, sticky='we', padx=(5,0))
        reset_button = tk.Button(window_frame, text='reset', command=self.set_local)
        reset_button.grid(row=0, column=3, sticky='we')
        reset_button.configure(highlightbackground=bgcolor)
        self.serv_entry.insert(tk.END, self.manager)
        window_frame.config(bg=bgcolor)
        window_frame.pack()
        self.buttonbox(bgcolor)

    def set_local(self):
        self.serv_entry.delete(0, tk.END)
        self.serv_entry.insert(tk.END, 'localhost')

    def validate(self):
        self.new_manager = self.serv_entry.get()
        ipaddress = test_network(self.new_manager)
        if ipaddress:
            self.ip_label.config(text=ipaddress)
            return 1
        else:
            self.ip_label.config(text='connection error')
            return 0

    def apply(self):
        config_writer('settings', 'manager', self.new_manager)


class ShowAllWindow(tkPopup.PopupWindow):

    def body(self, master, file):
        self.geometry('+680+100')
        self.resizable(0,0)
        s_frame= tk.Frame(self, bg=bgcolor, highlightthickness=0)
        s_frame.pack()
        sb = tk.Scrollbar(s_frame)
        txt_all = MyTextSettings(s_frame, width=42,
                                 yscrollcommand=sb.set)
        txt_all.pack(side=tk.LEFT, padx=(5,0))
        sb.configure(highlightcolor=bgcolor, command=txt_all.yview)
        sb.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        for item in servers_sorted(file):
            txt_all.set_text(item)
            txt_all.set_text(', '.join(return_frames(file, item)))
            txt_all.set_text('\r')
        self.buttonbox(bgcolor, pad=20)

        
if __name__ == '__main__':
    app = MainApplication()
    app.resizable(width=tk.FALSE, height=tk.FALSE)
    app.mainloop()
    