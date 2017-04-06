try:
    import tkinter as tk 
except ImportError:
    import Tkinter as tk     # python 2


class Popup(tk.Toplevel):

    def __init__(self, title=None, *args, **kwargs):

        tk.Toplevel.__init__(self)
        tkbody = tk.Frame(self)
        self.initial_focus = self.body(tkbody, *args, **kwargs)
        if not self.initial_focus:
            self.initial_focus = self
        self.initial_focus.focus_set()
        if title:
            self.title(title)
        self.transient()
        self.result = None
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.wait_window(self)

    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        pass

    def buttonbox(self, color, pad=0):
        # add standard button box. 
        # override if you don't want the standard buttons
        bbox = tk.Frame(self)
        but1 = tk.Button(bbox, text="Cancel", width=7, command=self.cancel)
        but1.configure(highlightbackground=color)
        but1.pack(side=tk.RIGHT, padx=(5, pad), pady=5)
        but2 = tk.Button(bbox, text="OK", width=7, command=self.ok)
        but2.configure(highlightbackground=color)
        but2.pack(side=tk.RIGHT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        bbox.configure(bg=color, highlightbackground="#443322")
        bbox.pack(fill=tk.X)

    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return
        
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the window
        self.focus_set()
        self.destroy()

    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override
