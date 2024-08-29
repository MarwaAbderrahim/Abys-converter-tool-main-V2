############# Importation 
from ast import arg
from concurrent.futures import process
from tabnanny import verbose
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.constants import DISABLED, NORMAL
from os import listdir
from glob import glob
import os
from turtle import update
from PIL import Image, ImageTk
from DicomRTTool import DicomReaderWriter
import SimpleITK as sitk
import pydicom as dicom
import pandas as pd
import glob
from tqdm import tqdm
import cv2
from PIL import Image
import csv as csv_lib
import pydicom
import threading
import sys
import multiprocessing 
from multiprocessing import Process
import joblib
from joblib import Parallel, delayed
from tqdm.gui import tqdm_gui
from tkinter import ttk
import threading
from tkinter import _tkinter


global in_path_dicom_nifti
global convert_save
global root
global in_path_nifti_dicom  # Nouveau global pour la conversion NIfTI en DICOM
global convert_save_nifti_dicom  # Nouveau global pour le bouton de conversion

############# page 1 : Home page 
def call_home_page():
    root.geometry('600x750')
    home_page = Frame(root, bg=bg)
    home_page.grid(row=0, column=0, sticky='nsew')
    title = Label(home_page, text='Abys Medical Converter', bg=bg, fg='Black', font='Arial 30 ')
    title.pack(pady=(20,0))
    image = Image.open('utils/image.png')
    image=image.resize((350,150))
    photo = ImageTk.PhotoImage(image)
    label = Label(root, image=photo)
    label.image = photo
    label.grid(row=1,column=0)
    buttons_frame = Frame(home_page, bg=bg)
    buttons_frame.pack(padx=10, pady=40)

    dicom_to_nifti_button = Button(buttons_frame, text='DICOM\nto\nNIfTI', font='none 20 bold', width=15, bg='black', fg='white', command=dicom_to_nifti_page)
    dicom_to_nifti_button.pack(pady=(80, 0))

    # Nouveau bouton Nifti to DICOM
    nifti_to_dicom_button = Button(buttons_frame, text='NIfTI\nto\nDICOM', font='none 20 bold', width=15, bg='black', fg='white', command=nifti_to_dicom_page)
    nifti_to_dicom_button.pack(pady=(20, 0))


############# page 2 : Dicom to nifti page 
def dicom_to_nifti_page():
    global text_message_d_n
    global convert_save
    global progress_bar
    root.geometry('600x750')
    dicom_to_nifti = Frame(root, bg=bg)
    dicom_to_nifti.grid(row=0, column=0, sticky='nsew')

    title = Label(dicom_to_nifti, text='DICOM to NIfTI', bg='black',fg='white', font='Arial 15 bold')
    title.pack()

    open_buttons = Frame(dicom_to_nifti, bg=bg)
    open_buttons.pack(pady=(30,0))

    open_file = Button(open_buttons, text='Open file', font='none 20 bold', width=10, bg='coral',fg='black', command=call_open_file_dicom_to_nifti)
    open_file.grid(row=0, column=0, padx=(0,20))

    open_dir = Button(open_buttons, text='Open Dirs', font='none 20 bold', width=10, bg='coral',fg='black', command=call_open_dir_dicom_to_nifti)
    open_dir.grid(row=0, column=1, padx=(20,0))

    convert_save = Button(dicom_to_nifti, text='Convert & Save', state = NORMAL , font='none 20 bold', bg='coral',fg='black', command=call_convert_save_dicom_to_nifti)
    convert_save.pack(pady=(40,0))


    text_message_d_n = Label(dicom_to_nifti,text='Choose file or dir', font='none 9', bg='coral',fg='black')
    text_message_d_n.pack(pady=(20,0))

    progress_bar = ttk.Progressbar(root, mode='determinate', length=260)
    progress_bar.place(x=170, y=350)

    home_button = Button(dicom_to_nifti, text='Home', command=call_home_page, font='none 20 bold', width=15, bg='black',fg='white')
    home_button.place(x=170, y=450)

    home_button = Button(dicom_to_nifti, text='Restart', command=restart, font='none 20 bold', width=15, bg='black',fg='white')
    home_button.place(x=170, y=510)
    #home_button.pack(pady=(60,0))

############# page 2 : Functions to open dicom files            



# def _start_thread():
#           p1 = threading.Thread(target=call_convert_save_dicom_to_nifti())
#           p1.start()
  

def call_open_file_dicom_to_nifti():
    global flag_dicom_nifti
    global in_path_dicom_nifti
    global text_message_d_n
    in_path_dicom_nifti = filedialog.askdirectory()
    if in_path_dicom_nifti: 
        flag_dicom_nifti = 1
        text_message_d_n.config(text='You opened: \n' + in_path_dicom_nifti)
    else:
       messagebox.showerror("Error", "try again")

def call_open_dir_dicom_to_nifti():
    global flag_dicom_nifti 
    global in_path_dicom_nifti
    global text_message_d_n
    global file
    in_path_dicom_nifti = filedialog.askdirectory()
    # in_path_dicom_nifti=manager.Value(any,in_path_dicom_nifti)
    if in_path_dicom_nifti:
        flag_dicom_nifti = 2
        text_message_d_n.config(text='You opened: \n' + in_path_dicom_nifti) 
    else:
        messagebox.showerror("Error", "try again")    
 
############# page 2 : Functions to convert dicom files
def call_convert_save_dicom_to_nifti():
    global progress_bar
    global image
    global images
    global out_path
    global file
    global convert_save
    global root
    global num_files
    global text_message_d_n
    if flag_dicom_nifti == 1 and in_path_dicom_nifti:
        progress_bar['maximum'] = 1
        out_path = filedialog.asksaveasfilename()
        text_message_d_n.config(text='Conversion...')
        if out_path:
            print("out_path", out_path)
            reader = DicomReaderWriter()
            reader.walk_through_folders(in_path_dicom_nifti)
            reader.get_images()
            sitk.WriteImage(reader.dicom_handle, out_path + '.nii.gz')
            text_message_d_n.config(text='Conversion is finished\n'+'File saved at\n' + out_path + '.nii.gz')
            progress_bar['value'] = 1
    if flag_dicom_nifti == 2 and in_path_dicom_nifti:
        images =[f.path for f in os.scandir(in_path_dicom_nifti) if f.is_dir()]
        out_path = filedialog.askdirectory()
        print (out_path)
        num_files = sum([True for f in os.scandir(in_path_dicom_nifti) if f.is_dir()])
        print(num_files)
        if out_path : 
            convert_save['state'] = DISABLED             
            def pa():
              nonlocal result
              result=Parallel(n_jobs=-2, backend='threading')(delayed(fonct)(image, out_path) for i, image in (enumerate(images))) 
            
            result = None
            progress_bar['maximum'] = num_files  # number of items that loops in Parallel
            
            process = threading.Thread(target=pa)
            process.start()
            """
            update progress bar
            """

            while progress_bar['value'] < num_files+1:
               progress_bar['value'] = n
               percentage = round(float(float(n)/float(num_files)*100), 2) #calculate the percentage
               t = "Converting..."+" | Progress: "+str(n)+"/"+str(num_files)+" | Percentage: "+str(percentage)+"%"
               progr = tk.Label(root, text=t, font='none 12', bg='black',fg='white')
               progr.grid(row=0, column=0)
               root.update_idletasks()
            # root.update()# prevent freezin
            # process.join()
            # progr.destroy()
            text_message_d_n.config(text='Conversion is finished\n'+'Files saved at\n' + out_path)
            progress_bar.destroy()
            convert_save['state'] = NORMAL
            # process.join()
        else:
                 messagebox.showerror("Error", "try again")
n=0
def fonct(k, out_path):
    global n
    reader = DicomReaderWriter()
    reader.walk_through_folders(k)
    reader.get_images()
    sitk.WriteImage(reader.dicom_handle, out_path + '/' + os.path.basename(k) + '.nii.gz') 
    n=n+1      

def restart():
    os.execv(sys.executable, ['python'] + sys.argv)

import numpy as np
import pydicom
import os
import SimpleITK as sitk
import time
from tqdm import tqdm

def writeSlices(series_tag_values, new_img, i, out_dir):
    image_slice = new_img[:,:,i]
    writer = sitk.ImageFileWriter()
    writer.KeepOriginalImageUIDOn()

    # Tags shared by the series.
    list(map(lambda tag_value: image_slice.SetMetaData(tag_value[0], tag_value[1]), series_tag_values))

    # Slice specific tags.
    image_slice.SetMetaData("0008|0012", time.strftime("%Y%m%d")) # Instance Creation Date
    image_slice.SetMetaData("0008|0013", time.strftime("%H%M%S")) # Instance Creation Time

    # Setting the type to CT preserves the slice location.
    image_slice.SetMetaData("0008|0060", "CT")  # set the type to CT so the thickness is carried over

    # (0020, 0032) image position patient determines the 3D spacing between slices.
    image_slice.SetMetaData("0020|0032", '\\'.join(map(str,new_img.TransformIndexToPhysicalPoint((0,0,i))))) # Image Position (Patient)
    image_slice.SetMetaData("0020,0013", str(i)) # Instance Number

    # Write to the output directory and add the extension dcm, to force writing in DICOM format.
    writer.SetFileName(os.path.join(out_dir,'slice' + str(i).zfill(4) + '.dcm'))
    writer.Execute(image_slice)

def call_open_file_nifti_to_dicom():
    global flag_nifti_dicom
    global in_path_nifti_dicom
    global text_message_n_d

    # Ouvrir une boîte de dialogue pour sélectionner un fichier NIfTI
    in_path_nifti_dicom = filedialog.askopenfilename(
        title="Open NIfTI File",
        filetypes=[("NIfTI files", "*.nii;*.nii.gz;*.nrrd;*.nhdr"), ("All files", "*.*")]
    )
    
    if in_path_nifti_dicom:
        flag_nifti_dicom = 1
        text_message_n_d.config(text='You opened: \n' + in_path_nifti_dicom)
    else:
        messagebox.showerror("Error", "Try again")

def call_open_dir_nifti_to_dicom():
    global flag_nifti_dicom
    global in_path_nifti_dicom
    global text_message_n_d
    in_path_nifti_dicom = filedialog.askdirectory()
    if in_path_nifti_dicom:
        flag_nifti_dicom = 2
        text_message_n_d.config(text='You opened: \n' + in_path_nifti_dicom)
    else:
        messagebox.showerror("Error", "try again")

def convert_nifti_to_dicom(nifti_file, out_dir):
    new_img = sitk.ReadImage(nifti_file)
    modification_time = time.strftime("%H%M%S")
    modification_date = time.strftime("%Y%m%d")
    direction = new_img.GetDirection()
    series_tag_values = [("0008|0031", modification_time),
                         ("0008|0021", modification_date),
                         ("0008|0008", "DERIVED\\SECONDARY"),
                         ("0020|000e", "1.2.826.0.1.3680043.2.1125." + modification_date + ".1" + modification_time),
                         ("0020|0037", '\\'.join(map(str, (direction[0], direction[3], direction[6],
                                                            direction[1], direction[4], direction[7])))),
                         ("0008|103e", "Created-SimpleITK")]
    list(map(lambda i: writeSlices(series_tag_values, new_img, i, out_dir), tqdm(range(new_img.GetDepth()))))

def nifti2dicom_mfiles(nifti_dir, out_dir=''):
    files = os.listdir(nifti_dir)
    for file in files:
        in_path = os.path.join(nifti_dir, file)
        out_path = os.path.join(out_dir, file)
        os.makedirs(out_path, exist_ok=True)
        convert_nifti_to_dicom(in_path, out_path)
    print("La conversion de NIfTI vers dicom est terminée.")

import glob
import os
import tkinter as tk
from tkinter import filedialog, messagebox, DISABLED, NORMAL

def call_convert_save_nifti_to_dicom():
    global progress_bar_nifti_dicom
    global convert_save_nifti_dicom
    global root
    global text_message_n_d
    global flag_nifti_dicom
    global in_path_nifti_dicom

    if flag_nifti_dicom == 1 and in_path_nifti_dicom:
        progress_bar_nifti_dicom['maximum'] = 1
        out_path = filedialog.askdirectory()
        text_message_n_d.config(text='Conversion...')
        if out_path:
            convert_nifti_to_dicom(in_path_nifti_dicom, out_path)
            text_message_n_d.config(text='Conversion is finished\n' + 'Files saved at\n' + out_path)
            # Mettre à jour la barre de progression
            progress_bar_nifti_dicom['value'] = 1
    elif flag_nifti_dicom == 2 and in_path_nifti_dicom:
        nifti_files = glob.glob(os.path.join(in_path_nifti_dicom, '*.nii.*'))
        out_path = filedialog.askdirectory()
        num_files_nifti = len(nifti_files)
        if out_path:
            convert_save_nifti_dicom['state'] = DISABLED
            progress_bar_nifti_dicom['maximum'] = num_files_nifti
            for i, file in enumerate(nifti_files):
                out_path_file = os.path.join(out_path, os.path.basename(file))
                convert_nifti_to_dicom(file, out_path_file)
                progress_bar_nifti_dicom['value'] = i + 1
                root.update_idletasks()

            text_message_n_d.config(text='Conversion is finished\n' + 'Files saved at\n' + out_path)
            convert_save_nifti_dicom['state'] = NORMAL



############# page 3 : Nifti to DICOM page 
def nifti_to_dicom_page():
    global text_message_n_d
    global convert_save_nifti_dicom
    global progress_bar_nifti_dicom
    root.geometry('600x750')
    nifti_to_dicom = Frame(root, bg=bg)
    nifti_to_dicom.grid(row=0, column=0, sticky='nsew')

    title = Label(nifti_to_dicom, text='NIfTI to DICOM', bg='black', fg='white', font='Arial 15 bold')
    title.pack()

    open_buttons = Frame(nifti_to_dicom, bg=bg)
    open_buttons.pack(pady=(30, 0))

    open_file = Button(open_buttons, text='Open file', font='none 20 bold', width=10, bg='coral', fg='black', command=call_open_file_nifti_to_dicom)
    open_file.grid(row=0, column=0, padx=(0, 20))

    open_dir = Button(open_buttons, text='Open Dirs', font='none 20 bold', width=10, bg='coral', fg='black', command=call_open_dir_nifti_to_dicom)
    open_dir.grid(row=0, column=1, padx=(20, 0))

    convert_save_nifti_dicom = Button(nifti_to_dicom, text='Convert & Save', state=NORMAL, font='none 20 bold', bg='coral', fg='black', command=call_convert_save_nifti_to_dicom)
    convert_save_nifti_dicom.pack(pady=(40, 0))

    text_message_n_d = Label(nifti_to_dicom, text='Choose file or dir', font='none 9', bg='coral', fg='black')
    text_message_n_d.pack(pady=(20, 0))

    progress_bar_nifti_dicom = ttk.Progressbar(root, mode='determinate', length=260)
    progress_bar_nifti_dicom.place(x=170, y=350)

    home_button = Button(nifti_to_dicom, text='Home', command=call_home_page, font='none 20 bold', width=15, bg='black', fg='white')
    home_button.place(x=170, y=450)

    home_button = Button(nifti_to_dicom, text='Restart', command=restart, font='none 20 bold', width=15, bg='black', fg='white')
    home_button.place(x=170, y=510)

############# The main function 
if __name__ == '__main__':
    multiprocessing .freeze_support()
    bg = 'white'
    root = Tk()
    root.geometry('600x750')
    root.title('Abys Converter')
    root.iconbitmap('utils/logo.ico')
    root.resizable(width=0, height=0)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    call_home_page()
    root.mainloop()
    
    
