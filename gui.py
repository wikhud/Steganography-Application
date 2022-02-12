from tkinter import *
from PIL import Image, ImageTk
import math
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import scrolledtext
from tkinterdnd2 import *
import time
import en

class gui_class:
    # init function
        def __init__ (self):
            self.img_file_to_en = ''
            self.img_file_to_de = ''
            self.secret_en = ''
            self.kind_en = ''
            self.output_path = ''

            self.gui_window = TkinterDnD.Tk ()
            self.gui_window.focus_set ()
            self.gui_window.resizable (False, False)
            self.gui_window.title ('Coder')
            self.gui_window.geometry ('650x550')
            # self.gui_window.geometry ('650x500+700-500')
            
            tab_control = ttk.Notebook ()
            self.tab1 = Frame (tab_control)
            self.tab2 = Frame (tab_control)

            tab_control.add (self.tab1, text = 'Encoder')
            tab_control.add (self.tab2, text = 'Decoder')
            tab_control.pack (expand = True, fill = 'both')

        # encoder gui
            self.lf1e = LabelFrame (self.tab1, bd = 0)
            self.lf2e = LabelFrame (self.tab1, text = 'Select image')
            self.lf3e = LabelFrame (self.tab1, text = 'Enter secret')
            self.lf4e = LabelFrame (self.tab1, text = 'Save encoded image')
            self.lf5e = LabelFrame (self.tab1, bd = 0)
            self.lf1e.place (x = 2, y = 0, height = 40, width = 645)
            self.lf2e.place (x = 10, y = 40, height = 65, width = 625)
            self.lf3e.place (x = 10, y = 115, height = 240, width = 625)
            self.lf4e.place (x = 10, y = 360, height = 90, width = 625)
            self.lf5e.place (x = 2, y = 455, height = 60, width = 645)

            # labels to use while transparent window theme choosen
            self.transparent_l1e = Label (self.lf2e, text = 'Select image')
            self.transparent_l2e = Label (self.lf3e, text = 'Enter secret')
            self.transparent_l3e = Label (self.lf4e, text = 'Save encoded image')
        
            self.l1e = Label (self.lf2e, text = 'or')
            self.l2e = Label (self.lf3e, text = 'or')
            self.l3e = Label (self.lf3e)      # secret as img (show)
            self.l5e = Label (self.lf5e)      # encoding success
            self.l1e.place (x = 102, y = 10)

            self.t1e = Text (self.lf2e, width = 40, height = 1, wrap = NONE, state = DISABLED)    # input img path
            self.t2e = scrolledtext.ScrolledText (self.lf3e, height = 10, width = 40, wrap = 'word', undo = TRUE)       # secret as text input
            self.t3e = Text (self.lf3e, width = 40, height = 1, wrap = NONE, state = DISABLED)    # secret as img path
            self.t4e = Text (self.lf4e, width = 40, height = 1, wrap = NONE, state = DISABLED)    # custom output path
            self.t2e.drop_target_register (DND_FILES)
            self.t2e.dnd_bind ('<<Drop>>', self.drop_txt)
            self.t2e.bind ('<FocusIn>', self.focus_in_secret_as_text)
            self.t2e.bind ('<FocusOut>', self.focus_out_secret_as_text)

            self.b1e = Button (self.lf2e, bd = 1, text = 'Browse', command = lambda: self.browse_img ('encode'))    # browse input img
            self.b2e = Button (self.lf3e, bd = 1, text = 'Browse', command = lambda: self.browse_img ('secret'))    # browse secret as img
            self.b3e = Button (self.lf4e, bd = 1, text = 'Browse', command = lambda: self.save_as ('encode'))       # browse custom output
            self.b4e = Button (self.lf5e, width = 15, height = 2, bd = 1, text = 'Encode', command = self.main_f_en)                # encode
            self.b5e = Button (self.lf5e, bd = 1, text = 'Check result', command = lambda: self.check_result (self.img_file_to_en, self.output_path))       # check reuslts
            b6e = Button (self.lf5e, width = 8, bd = 1, text = 'Clear', command = lambda: self.clear ('encode'))         # clear
            b7e = Button (self.tab1, bd = 1, text = 'How to use?', command = lambda: self.help ('encode'))    # help
            self.b1e.place (x = 45, y = 10)
            self.b4e.place (x = 45, y = 10)
            b6e.place (x = 550, y = 20)
            b7e.place (x = 380, y = 10) 
            
            self.e1e = Entry (self.lf2e)    # drop input img
            self.e2e = Entry (self.lf3e)    # drop secret as img
            self.e1e.insert (0, 'Drop here')
            self.e1e.config (justify = 'center', state = 'readonly')
            self.e2e.insert (0, 'Drop here')
            self.e2e.config (justify = 'center', state = 'readonly')
            self.e1e.drop_target_register (DND_FILES)
            self.e1e.dnd_bind ('<<Drop>>', lambda event, function = 'encode': self.drop_img (event, function))
            self.e2e.drop_target_register (DND_FILES)
            self.e2e.dnd_bind ('<<Drop>>', lambda event, function = 'secret': self.drop_img (event, function))
            self.e1e.place (x = 130, y = 10, height = 25, width = 130)

            self.buttons_group_1 = IntVar ()
            self.rb1 = Radiobutton (self.lf3e, text = 'text', variable = self.buttons_group_1, value = 1, command =  lambda: self.what_secret ('text'))     # select txt as secret
            self.rb2 = Radiobutton (self.lf3e, text = 'image', variable = self.buttons_group_1, value = 2, command =  lambda: self.what_secret ('img'))       # select img as secret
            self.rb1.place (x = 45, y = 5)
            self.rb2.place (x = 125, y = 5)
            self.rb1.invoke ()
            self.buttons_group_2 = IntVar ()
            self.rb3 = Radiobutton (self.lf4e, text = 'default', variable = self.buttons_group_2, value = 3, command =   lambda: self.what_output_path ('default'))     # select default output
            self.rb4 = Radiobutton (self.lf4e, text = 'custom', variable = self.buttons_group_2, value = 4, command = lambda: self.what_output_path ('custom'))    # select custom output
            self.rb3.place (x = 45, y = 5)
            self.rb4.place (x = 125, y = 5)
            self.rb3.invoke ()

            self.progressbar_e = ttk.Progressbar (self.lf5e, length = 250, orient = 'horizontal', mode = 'determinate')

            self.scrollbar_e = Scrollbar (self.tab1, orient = 'horizontal') 
            def scroll_all (*args):
                self.t1e.xview (*args)
                self.t3e.xview (*args)
                self.t4e.xview (*args)
            self.scrollbar_e.config (command = scroll_all)

        # decoder gui
            self.lf1d = LabelFrame (self.tab2, bd = 0)
            self.lf2d = LabelFrame (self.tab2, text = 'Select image')
            self.lf3d = LabelFrame (self.tab2, bd = 0)
            self.lf1d.place (x = 2, y = 0, height = 40, width = 645)
            self.lf2d.place (x = 10, y = 40, height = 65, width = 625)
            self.lf3d.place (x = 2, y = 110, height = 500, width = 645)

            self.transparent_l1d = Label (self.lf2d, text = 'Select image')     # label to use while transparent window theme choosen

            self.l1_1d = Label (self.lf2d, text = 'or')
            self.l2d = Label (self.lf3d)    # decoding success/failed
            self.l3d = Label (self.lf3d)    # show secret as img
            self.l1_1d.place (x = 102, y = 10)

            self.t1d = Text (self.lf2d, width = 40, height = 1, wrap = NONE, state = DISABLED)        # input img path
            self.t2d = scrolledtext.ScrolledText (self.lf3d, height = 10, width = 50, wrap = 'word')          # show secret as text
            self.t2d.yview (END)     # it makes no delays while reading secret as text

            self.b1d = Button (self.lf2d, bd = 1, text = 'Browse', command = lambda: self.browse_img ('decode'))        # browse input img
            self.b2d = Button (self.lf3d, width = 15, height = 2, bd = 1, text = 'Decode', command = self.main_f_de)    # decode
            self.b3d = Button (self.lf3d, bd = 1, text = 'Save secret', command = lambda: self.save_as ('decode'))      # save secret
            b4d = Button (self.lf3d, width = 8, bd = 1, text = 'Clear', command = lambda: self.clear ('decode'))        # clear
            b5d = Button (self.lf1d, bd = 1, text = 'How to use?', command = lambda: self.help ('decode'))      # help
            self.b1d.place (x = 45, y = 10)
            self.b2d.place (x = 45, y = 10)
            b4d.place (x = 500, y = 330)
            b5d.place (x = 378, y = 10)

            self.e1d = Entry (self.lf2d)      # drop input img
            self.e1d.drop_target_register (DND_FILES)
            self.e1d.dnd_bind ('<<Drop>>', lambda event, function = 'decode': self.drop_img (event, function))
            self.e1d.insert (0, 'Drop here')
            self.e1d.config (justify = 'center', state = 'readonly')
            self.e1d.place (x = 130, y = 10, width = 130, height = 25)

            self.progressbar_d = ttk.Progressbar (self.lf3d, length = 250, orient = 'horizontal', mode = 'determinate')

            self.scrollbar_d = Scrollbar (self.tab2, orient = 'horizontal', command = self.t1d.xview)

        # common
            self.combo = Combobox (state = 'readonly')
            self.combo ['values'] = ('Change window theme', 'Standard (default)', 'Transparent')
            self.combo.current (0)
            self.combo.place (x = 490, y = 35) 
            self.combo.bind ('<<ComboboxSelected>>', self.theme)

    # input functions
        def browse_img (self, function):
            filename = filedialog.askopenfilename (filetypes = ( ('PNG', '*.png'), ('BMP', '*.bmp'), ('All files', '*.*')))

            if filename == '':
                return
            else:
                ext_short = ('.bmp', '.png')
                ext = ('.bmp', '.png', '.jpg', '.jpeg')

                if function == 'encode':
                    if filename.endswith (tuple (ext_short)):
                        self.img_file_to_en = filename

                        self.path_update (self.t1e, self.img_file_to_en)
                        if self.combo.get () == 'Transparent':
                            self.t1e.place (x = 400, y = 13)
                        else:
                            self.t1e.place (x = 280, y = 13)  

                        self.rb3.invoke ()
                    else:
                        self.warning ('format_not_recognized_short')     
                
                elif function == 'secret':
                    if filename.endswith (tuple (ext)):
                        self.secret_en = filename

                        self.path_update (self.t3e, self.secret_en)
                        self.t3e.place (x = 280, y = 38)

                        self.display_img (self.secret_en)
                    else:
                        self.warning ('format_not_recognized') 
                    
                elif function == 'decode':
                    if filename.endswith (tuple (ext_short)):
                        self.img_file_to_de = filename

                        self.path_update (self.t1d, self.img_file_to_de)
                        if self.combo.get () == 'Transparent':
                            self.t1d.place (x = 400, y = 13) 
                        else:
                            self.t1d.place (x = 280, y = 13)  
                    else:
                        self.warning ('format_not_recognized_short')

        def drop_img (self, event, function):
            ext_short = ('.bmp', '.png')
            ext = ('.bmp', '.png', '.jpg', '.jpeg')

            # it allows images with whitespaces in the path be recognized
            event.data = event.data.replace("{", "")
            event.data = event.data.replace("}", "")

            filename = StringVar ()
            filename.set (event.data)
            filename = filename.get ()

            if function == 'encode':
                if event.data.endswith (tuple (ext_short)):
                    self.img_file_to_en = filename

                    self.path_update (self.t1e, self.img_file_to_en)
                    if self.combo.get () == 'Transparent':
                        self.t1e.place (x = 400, y = 13)
                    else:
                        self.t1e.place (x = 280, y = 13)  

                    self.rb3.invoke ()

                else:
                    self.warning ('format_not_recognized_short') 

            elif function == 'secret':
                if event.data.endswith (tuple (ext)):
                    self.secret_en = filename
                    
                    self.path_update (self.t3e, self.secret_en)
                    self.t3e.place (x = 280, y = 38)
                    
                    self.display_img (self.secret_en)

                else:
                    self.warning ('format_not_recognized')
                    
            elif function == 'decode':
                if event.data.endswith (tuple (ext_short)):
                    self.img_file_to_de = filename
                    
                    self.path_update (self.t1d, self.img_file_to_de)
                    if self.combo.get () == 'Transparent':
                        self.t1d.place (x = 400, y = 13) 
                    else:
                        self.t1d.place (x = 280, y = 13)  
                
                else:
                    self.warning ('format_not_recognized_short')            

        def what_secret (self, type):
            if type == 'text':
                self.secret_en = ''
                self.t3e.config (state = NORMAL)
                self.t3e.delete (1.0, END)
                self.t3e.config (state = DISABLED)
                self.t3e.place_forget ()
                self.l2e.place_forget ()
                self.l3e.place_forget ()
                self.b2e.place_forget ()
                self.e2e.place_forget ()

                self.kind_en = 'T'
                if self.t2e.compare ('end-1c', '==', 1.0):
                    self.t2e.config (fg = 'grey')
                    self.t2e.insert (END, 'Start typing or drop a .txt file here...')
                self.t2e.place (x = 45, y = 40)
                self.gui_window.focus_set ()

            elif type == 'img':
                self.t2e.place_forget ()

                self.kind_en = 'I'
                self.l2e.place (x = 102, y = 37)
                self.b2e.place (x = 45, y = 35)
                self.e2e.place (x = 130, y = 35, height = 25, width = 130)

    # secret as text functions
        def drop_txt (self, event):
            # it allows images with whitespaces in the path be recognized
            event.data = event.data.replace("{", "")
            event.data = event.data.replace("}", "")
            if event.data.endswith ('.txt'):
                self.t2e.delete (1.0, END)
                with open (event.data, 'r', encoding = 'utf-8') as file:
                    for line in file:
                        self.t2e.config (fg = 'black')
                        self.t2e.insert (END, line)

        def focus_out_secret_as_text (self, event):
            if self.t2e.compare ('end-1c', '==', 1.0):
                self.t2e.insert (END, 'Start typing or drop a .txt file here...')
                self.t2e.config (fg = 'grey')
            self.gui_window.focus_set ()

        def focus_in_secret_as_text (self, event):       
            if self.t2e['fg'] == 'grey':
                self.t2e.delete (1.0, END)
                self.t2e.config (fg = 'black')
        
        def get_secret (self):
            if self.kind_en == 'T':
                secret_data = self.t2e.get (1.0, 'end-1c')    # 'end-1c' deletes one automatically added line to tk.Text (and so blank line is gone and there's not secret recognized)

                if self.t2e['fg'] == 'grey':
                    return
                else:
                    self.secret_en = secret_data

    # output functions
        def what_output_path (self, type):
            if type == 'default':
                self.t4e.place_forget ()
                self.b3e.place_forget ()
            
                self.output_path = self.img_file_to_en

                if self.output_path != '':
                    self.path_update (self.t4e, self.output_path)
                    self.t4e.place (x = 45, y = 40)

                self.gui_window.focus_set ()

            elif type == 'custom':
                self.output_path = ''
                self.t4e.config (state = NORMAL)
                self.t4e.delete (1.0, END)
                self.t4e.config (state = DISABLED)
                self.t4e.place_forget ()

                self.b3e.place (x = 45, y = 35)

                self.gui_window.focus_set ()

        def save_as (self, function):
            if function == 'encode':
                file = filedialog.asksaveasfilename (defaultextension = '.png', initialfile = 'encoded_img', filetypes = ( ('PNG', '*.png'), ('BMP', '*.bmp'), ('All files', '*.*')))
                if file == '':
                    return
                else:
                    self.output_path = file
                    self.path_update (self.t4e, self.output_path)
                    self.t4e.place (x = 115, y = 38)

            elif function == 'decode':
                if self.secret_kind_de == 'T':
                    file = filedialog.asksaveasfilename (defaultextension = '.txt', initialfile = 'secret_file', filetypes = ( ('Text files', '*.txt'), ('All files', '*.*')))
                    try:
                        if file != '':
                            with open (file, 'w') as f:
                                f.write (self.secret_de)
                            message = 'Secret saved at: ' + file
                            messagebox.showinfo ('Success!', message)
                        else:
                            return
                    except:
                        self.warning ('failure')
                    

                elif self.secret_kind_de == 'I':
                    file = filedialog.asksaveasfilename (defaultextension = '.png', initialfile = 'secret_file', filetypes = ( ('PNG', '*.png'), ('BMP', '*.bmp'), ('All files', '*.*')))
                    try:
                        if file != '':
                            self.secret_de.save (file)
                            message = 'Secret saved at: ' + file
                            messagebox.showinfo ('Success!', message)
                        else:
                            return
                    except:
                        self.warning ('failure')     

    # tools functions
        def clear (self, function):
            if function == 'encode':
                self.img_file_to_en = ''
                self.secret_en = ''
                self.kind_en = ''
                self.output_path = ''

                self.l5e.config (text = '')
                self.l5e.place_forget ()
                
                self.t1e.config (state = NORMAL)
                self.t1e.delete (1.0, END)
                self.t1e.config (state = DISABLED)
                self.t1e.place_forget ()
                self.t2e.config (state = NORMAL)
                self.t2e.delete (1.0, END)
                self.t2e.dnd_bind ('<<Drop>>', self.drop_txt)
                self.t2e.bind ('<FocusIn>', self.focus_in_secret_as_text)
                self.t2e.bind ('<FocusOut>', self.focus_out_secret_as_text)
                self.gui_window.focus_set ()
                self.t3e.config (state = NORMAL)
                self.t3e.delete (1.0, END)
                self.t3e.config (state = DISABLED)
                self.t3e.place_forget ()
                self.t4e.config (state = NORMAL)
                self.t4e.delete (1.0, END)
                self.t4e.config (state = DISABLED)
                self.t4e.place_forget ()
                
                self.b1e.config (command = lambda: self.browse_img ('encode')) 
                self.b2e.config (command = lambda: self.browse_img ('secret'))              
                self.b3e.config (command = lambda: self.save_as ('encode'))
                self.b4e.config (command = self.main_f_en)
                self.b5e.place_forget ()
                
                self.e1e.dnd_bind ('<<Drop>>', lambda event, function = 'encode': self.drop_img (event, function))
                self.e2e.dnd_bind ('<<Drop>>', lambda event, function = 'secret': self.drop_img (event, function))

                self.rb1.config (state = NORMAL)
                self.rb2.config (state = NORMAL)
                self.rb3.config (state = NORMAL)
                self.rb4.config (state = NORMAL)
                self.rb1.invoke ()

                self.scrollbar_e.pack_forget () 

            elif function == 'decode':
                self.img_file_to_de = ''
                self.secret_de = ''
                self.secret_kind_de = ''
                self.message = ''
                
                self.l2d.config (text = '')
                self.l2d.place_forget ()
                self.l3d.place_forget ()
                
                self.t1d.config (state = NORMAL)
                self.t1d.delete (1.0, END)
                self.t1d.config (state = DISABLED)
                self.t1d.place_forget ()
                self.t2d.config (state = NORMAL)
                self.t2d.delete (1.0, END)
                self.t2d.place_forget ()

                self.b1d.config (command = lambda: self.browse_img ('decode'))             
                self.b2d.config (command = self.main_f_de)
                self.b3d.place_forget ()

                self.e1d.dnd_bind ('<<Drop>>', lambda event, function = 'decode': self.drop_img (event, function))

                self.scrollbar_d.pack_forget () 
        
        def path_update (self, text_widget, filename):
            text_widget.config (state = NORMAL)
            text_widget.delete (1.0, END)
            text_widget.insert (1.0, filename)
            text_widget.config (state = DISABLED)
            self.to_scroll (text_widget)    

        def to_scroll (self, text_widget):
            if text_widget == self.t1e or text_widget == self.t3e or text_widget == self.t4e:
                if self.combo.get () == 'Transparent':
                    if len (text_widget.get (1.0, END)) > 28:
                        self.scrollbar_e.pack (side = BOTTOM, fill = X)
                        text_widget.config (xscrollcommand = self.scrollbar_e.set)
                    else:
                        self.scrollbar_e.pack_forget ()
                else:
                    if len (text_widget.get (1.0, END)) > 40:
                        self.scrollbar_e.pack (side = BOTTOM, fill = X)
                        text_widget.config (xscrollcommand = self.scrollbar_e.set)
                    else:
                        self.scrollbar_e.pack_forget ()
            elif text_widget == self.t1d:
                if self.combo.get () == 'Transparent':
                    if len (text_widget.get (1.0, END)) > 28:
                        self.scrollbar_d.pack (side = BOTTOM, fill = X)
                        text_widget.config (xscrollcommand = self.scrollbar_d.set)
                    else:
                        self.scrollbar_d.pack_forget ()
                else:
                    if len (text_widget.get (1.0, END)) > 40:
                        self.scrollbar_d.pack (side = BOTTOM, fill = X)
                        text_widget.config (xscrollcommand = self.scrollbar_d.set)
                    else:
                        self.scrollbar_d.pack_forget ()

        def display_img (self, inupt_image):
            if inupt_image == self.secret_en:
                image = Image.open (inupt_image)
                
                max_width = 225     # 'max' values define size of image so it could be the largest and still fit nicely into its intended place
                max_height = 135
                img_width, img_height = image.size
                if img_width > max_width or img_height > max_height:
                    a = img_width/max_width
                    b = img_height/max_height
                    if a>b:
                        scalebase = max_width/img_width
                    else:
                        scalebase = max_height/img_height
                    image = image.resize (int (scalebase * size_component) for size_component in image.size)

                self.image_to_display =  ImageTk.PhotoImage (image)
                self.l3e.config (image = self.image_to_display)
                self.l3e.place (x = 45, y = 65)
                        

            elif inupt_image == self.secret_de:
                self.photo_img = ImageTk.PhotoImage (inupt_image)

                max_width = 400
                max_height = 230
                img_width = self.photo_img.width ()
                img_height = self.photo_img.height ()
                if img_width > max_width or img_height > max_height:
                    a = img_width/max_width
                    b = img_height/max_height
                    if a>b:
                        scalebase = math.ceil (img_width/max_width)
                    else:
                        scalebase = math.ceil (img_height/max_height)
                    self.photo_img = self.photo_img._PhotoImage__photo.subsample (scalebase)

                self.l3d.config (image = self.photo_img)
                self.l3d.place (x = 45, y = 110)

    # additional functions
        def warning (self, type):
            if type == 'no_input_file':
                messagebox.showwarning ('No input file selected.', 'Select input file!')
            elif type == 'no_output_file':
                messagebox.showwarning ('No output file selected.', 'Select name and destination directory of the output file!')
            elif type == 'no_secret':
                messagebox.showwarning ('No secret.', 'Input secret!')
            elif type == 'format_not_recognized_short':
                messagebox.showwarning ('File format not recognized.', 'Enter image file format that supports lossless data compression (".png", ".bmp")!')
            elif type == 'format_not_recognized':
                messagebox.showwarning ('File format not recognized.', 'Enter supported image file format (".png", ".bmp", ".jpg", ".jpeg")!')
            elif type == 'ascii':
                messagebox.showwarning ('No secret.', 'Secret contains unicode characters.\nChange it before moving on!')
            elif type == 'secret_too_long':
                messagebox.showwarning ('Secret too long.', 'Shorten secret text!')
            elif type == 'secret_too_large':
                messagebox.showwarning ('Secret too large.', 'Select secret image in smaller size!')
            elif type == 'secret_image_width':
                messagebox.showwarning ('Secret image`s width too wide.', 'Select secret image with shorter width!')
            elif type == 'larger_input_size':
                messagebox.showwarning ('Input image too small.', 'Need larger input image`s size for such a secret!')
            elif type == 'clear_first':
                messagebox.showwarning ('Old values.', 'Press Clear first!')
            elif type == 'failure':
                messagebox.showinfo ('Failure!', 'Something went wrong. Try again.')
                
        def progress_bar_step (self, function):
            if function == 'encode':
                self.progressbar_e.place (x = 180, y = 20)
                for i in range (5):
                    self.gui_window.update_idletasks ()
                    self.progressbar_e ['value'] += 20
                    time.sleep (1)  
                self.progressbar_e.stop ()
                self.progressbar_e.place_forget ()

            if function == 'decode':
                self.progressbar_d.place (x = 180, y = 20)
                for i in range (5):
                    self.gui_window.update_idletasks ()
                    self.progressbar_d ['value'] += 20
                    time.sleep (1)  
                self.progressbar_d.stop ()
                self.progressbar_d.place_forget ()   

        def check_result (self, input_img_file, output_img_file):
            result_window = Toplevel (self.gui_window)

            input_img = Image.open (input_img_file)
            output_img = Image.open (output_img_file)

            max_width = 500         # 'max' values define size of image so it could be the largest and still fit nicely into its intended place
            max_height = 500
            img_width, img_height = input_img.size
            if img_width > max_width or img_height > max_height:
                a = img_width/max_width
                b = img_height/max_height
                if a>b:
                    scalebase = max_width/img_width
                else:
                    scalebase = max_height/img_height
                input_img = input_img.resize (int (scalebase * size_component) for size_component in input_img.size)
                output_img = output_img.resize (int (scalebase * size_component) for size_component in output_img.size)
                img_width, img_height = input_img.size

            # setting window's size dynamically
            if img_width*2+20 > 300 and img_height+50 > 300:
                geo = str (img_width*2+20) + 'x' + str (img_height+50)      
            elif img_width*2+20 < 300:
                geo = str (300) + 'x' + str (img_height+50)
            elif img_height+50 < 300:
                geo = str (img_width*2+20) + 'x' + str (300)

            result_window.geometry (geo)
            result_window.resizable (False, False)

            input_img = ImageTk.PhotoImage (input_img)
            output_img  = ImageTk.PhotoImage (output_img)

            before_img = Label (result_window, image = input_img)
            after_img = Label (result_window, image = output_img)
            before_txt = Label (result_window, text = 'BEFORE')
            after_txt = Label (result_window, text = 'AFTER')

            result_window.columnconfigure (0, weight = 1)
            result_window.columnconfigure (1, weight = 1)

            before_img.grid (column = 0, row = 1, sticky = N, padx = 5)
            after_img.grid (column = 1, row = 1, sticky = N, padx = 5)
            before_txt.grid (column = 0, row = 0, sticky = N, padx = 5, pady = 5)
            after_txt.grid (column = 1, row = 0, sticky = N, padx = 5, pady = 5)
    
            result_window.title ('Result of encoding')
            result_window.mainloop ()

        def help (self, function):
            help_window = Toplevel (self.gui_window)
            
            lframe = LabelFrame (help_window, text = 'Instructions')
            lframe.pack (fill = BOTH, expand = True, padx = 10, pady = 10)

            if function == 'encode':
                instructions = Label (lframe, justify = 'left', text = '1. Select image to be a data storage.\n    Browse it or drop it.*\n    Warning! Only lossless data compression image file format can be selected (".png", ".bmp")!\n\n 2. Enter secret to encode it in previously selected image.\n     Your secret might be an image file or a text file.\n     Browse it or drop it.*\n\n 3. Select name and destination of an image to be created.*\n     Leaving it as default means the base (data storage) image will be overwritten.\n\n 4. Press "Encode" button to encode.\n\n 5. Press "Check result" button to check differences between input and output images.\n\n 6. Press "Clear" button to start again.\n\n\n *Path to the file will appear right after being selected.\n   If needed, it is scrollable (down the window).\n\n Change window theme by selecting one in bottom left corner.')        
            elif function == 'decode':
                instructions = Label (lframe, justify = 'left', text = '1. Select image to be decoded.\n    Browse it or drop it.*\n    Warning! Only lossless data compression image file format can be selected (".png", ".bmp")!\n\n 2. Press "Decode" button to decode.\n\n 3. Press "Save secret" button to save decrypted text or image as a file.\n     Select name and destination of the file to be created.*\n\n 4. Press "Clear" button to start again.\n\n\n *Path to the file will appear right after being selected.\n   If needed, it is scrollable (down the window).\n\n Change window theme by selecting one in bottom left corner.')        
            instructions.pack ()
            
            help_window.title ('Help')
            # help_window.geometry ('550x300+700-500')
            help_window.geometry ('550x380')
            help_window.resizable (False, False)
            
            help_window.mainloop ()    

        def theme (self, event):
            if self.combo.get () == 'Choose theme' or self.combo.get () == 'Standard (default)':
                # encoder
                self.transparent_l1e.place_forget ()
                self.b1e.place (x = 45, y = 10)
                self.e1e.place (x = 130, y = 10)
                self.l1e.place (x = 102, y = 10)
                self.t1e.config (width = 40, height = 1)
                if self.img_file_to_en != '':
                    self.t1e.place (x = 280, y = 13)
                    self.to_scroll (self.t1e)
                self.transparent_l2e.place_forget ()
                self.rb1.place (x = 45, y = 5)
                self.rb2.place (x = 125, y = 5)
                self.transparent_l3e.place_forget ()
                self.rb3.place (x = 45, y = 5)
                self.rb4.place (x = 125, y = 5)
                self.tab1.config (bg = '#ECF0F1')
                self.lf1e.config (bg = '#ECF0F1')
                self.lf2e.config (bg = '#ECF0F1', bd = 1, text = 'Select image')
                self.lf3e.config (bg = '#ECF0F1', bd = 1, text = 'Enter secret')
                self.lf4e.config (bg = '#ECF0F1', bd = 1, text = 'Save encoded image')
                self.lf5e.config (bg = '#ECF0F1')
                # decoder
                self.transparent_l1d.place_forget ()
                self.b1d.place (x = 45, y = 10)
                self.e1d.place (x = 130, y = 10)
                self.l1_1d.place (x = 102, y = 10)
                self.t1d.config (width = 40, height = 1)
                if self.img_file_to_de != '':
                    self.t1d.place (x = 280, y = 13)
                    self.to_scroll (self.t1d)
                self.tab2.config (bg = '#ECF0F1')
                self.lf1d.config (bg = '#ECF0F1')
                self.lf2d.config (bg = '#ECF0F1', bd = 1, text = 'Select image')
                self.lf3d.config (bg = '#ECF0F1')
            elif self.combo.get () == 'Transparent':
                # encoder
                self.transparent_l1e.place (x = 5, y = 10)
                self.b1e.place (x = 125, y = 10)
                self.e1e.place (x = 220, y = 10)
                self.l1e.place (x = 187, y = 10)
                self.t1e.config (width = 27, height = 1)
                if self.img_file_to_en != '':
                    self.t1e.place (x = 400, y = 13)
                    self.to_scroll (self.t1e)
                self.transparent_l2e.place (x = 5, y = 6)
                self.rb1.place (x = 125, y = 5)
                self.rb2.place (x = 190, y = 5)
                self.transparent_l3e.place (x = 5, y = 6)
                self.rb3.place (x = 175, y = 5)
                self.rb4.place (x = 255, y = 5)
                self.tab1.config (bg = '#F0F3F4')
                self.lf1e.config (bg = '#F0F3F4')
                self.lf2e.config (bg = '#F0F3F4', bd = 0, text = '')
                self.lf3e.config (bg = '#F0F3F4', bd = 0, text = '')
                self.lf4e.config (bg = '#F0F3F4', bd = 0, text = '')
                self.lf5e.config (bg = '#F0F3F4')
                # decoder
                self.tab2.config (bg = '#F0F3F4')
                self.lf1d.config (bg = '#F0F3F4')
                self.lf2d.config (bg = '#F0F3F4', bd = 0, text = '')
                self.lf3d.config (bg = '#F0F3F4')
                self.transparent_l1d.place (x = 5, y = 10)
                self.b1d.place (x = 125, y = 10)
                self.e1d.place (x = 220, y = 10)
                self.l1_1d.place (x = 187, y = 10)
                self.t1d.config (width = 27, height = 1)
                if self.img_file_to_de != '':
                    self.t1d.place (x = 280, y = 13)
                    self.to_scroll (self.t1d)

                self.gui_window.wm_attributes ('-transparentcolor', '#F0F3F4')
            self.combo['values'] = ('Standard (default)', 'Transparent')
            
    # main functions
        def main_f_en (self):
            self.get_secret ()

            if self.img_file_to_en == '':
                self.warning ('no_input_file')
                return
            elif self.output_path == '':
                self.warning ('no_output_file')
                return
            elif self.secret_en == '':
                self.warning ('no_secret')
                return
            elif self.secret_en.isascii () == False and self.kind_en == 'T':
                self.warning ('ascii')
                return
            else:
                try: 
                    self.progress_bar_step ('encode')
                    coder_class_instance_1 = en.coder_class ()
                    run_program_and_get_data = coder_class_instance_1.encoder (self.img_file_to_en, self.secret_en, self.output_path, self.kind_en)
                    error = run_program_and_get_data
                    if error == 1:
                        error = 0
                        return
                    else:
                        self.l5e.config (text = 'Image encoded succesfully!')
                        self.l5e.place (x = 180, y = 20)

                        self.t2e.unbind ('<<Drop>>')
                        self.t2e.config (state = DISABLED)
                        
                        self.b1e.config (command = lambda: self.warning ('clear_first')) 
                        self.b2e.config (command = lambda: self.warning ('clear_first'))          
                        self.b3e.config (command = lambda: self.warning ('clear_first'))
                        self.b4e.config (command = lambda: self.warning ('clear_first'))
                        self.b5e.place (x = 370, y = 20)

                        self.e1e.unbind ('<<Drop>>')
                        self.e2e.unbind ('<<Drop>>')

                        self.rb1.config (state = DISABLED)
                        self.rb2.config (state = DISABLED)
                        self.rb3.config (state = DISABLED)
                        self.rb4.config (state = DISABLED)
                except:
                    self.warning ('failure')

        def main_f_de (self):
            if self.img_file_to_de == '':
                self.warning ('no_input_file')
                return
            else:
                try:
                    self.progress_bar_step ('decode')
                    coder_class_instance_2 = en.coder_class ()
                    run_program_and_get_data = coder_class_instance_2.decoder (self.img_file_to_de)

                    if len (run_program_and_get_data) == 3:
                        self.secret_kind_de = run_program_and_get_data[0]
                        self.secret_de = run_program_and_get_data[1]
                        self.message = run_program_and_get_data[2]
                        
                        if self.secret_kind_de == 'T':
                            self.t2d.insert (END, self.secret_de)
                            self.t2d.config (state = DISABLED)
                            self.t2d.place (x = 45, y = 110)
                            self.b3d.place (x = 45, y = 300)

                        elif self.secret_kind_de == 'I':
                            self.display_img (self.secret_de)
                            self.b3d.place (x = 45, y = 300)

                    else:
                        self.message = run_program_and_get_data[0]
                            
                    self.l2d.config (text = self.message)
                    self.l2d.place (x = 45, y = 70)

                    self.b1d.config (command = lambda: self.warning ('clear_first'))           
                    self.b2d.config (command = lambda: self.warning ('clear_first'))

                    self.e1d.unbind ('<<Drop>>')
                except:
                    self.warning ('failure')

        def program_run (self):
            self.gui_window.mainloop ()
