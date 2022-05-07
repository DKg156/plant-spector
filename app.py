"""
@author: Dhruv Khurana
"""

checkimport = 0
from tkinter import * 
from tkinter import filedialog
from tkinter.ttk import *
from pathlib import Path
from PIL import ImageTk,Image 
import numpy as np
import pandas as pd
from super_image import EdsrModel, ImageLoader
import requests
import os, glob
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.applications import resnet
from keras.applications.resnet import preprocess_input
from keras.models import load_model
from keras.preprocessing import image as im
from ipywidgets import FloatProgress
import textwrap
import re
import time


global supermodel,model1
supermodel = EdsrModel.from_pretrained('eugenesiow/edsr-base', scale=4)
file_path = r'C:/Users/dhruv/archive/plantvillage dataset/color/Plant Village'
filepaths = list(glob.glob(file_path+'/**/*.*'))
labels = list(map(lambda x: os.path.split(os.path.split(x)[0])[1], filepaths))
filepath = pd.Series(filepaths, name='Filepath').astype(str)
labels = pd.Series(labels, name='Label')
data = pd.concat([filepath, labels], axis=1)
data = data.sample(frac=1).reset_index(drop=True)
train, test = train_test_split(data, test_size=0.20, random_state=42)
test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
test_gen = test_datagen.flow_from_dataframe(
    dataframe=test,
    x_col='Filepath',
    y_col='Label',
    target_size=(100,100),
    class_mode='categorical',
    batch_size=32,
    shuffle=False
)
model1 = load_model('Color_95.34506797790527.h5')
print("Loading model....Success")

def imgimport() :
   global inputs,img,checkimport
   img_path = filedialog.askopenfilename(title="Select plant image", filetypes=(("JPG File", "*.jpg"),("PNG File", "*.png"), ("All Files", "*.*")))
   if img_path.endswith('.jpg') or img_path.endswith('.JPG') or img_path.endswith('.PNG') or img_path.endswith('.png') or img_path.endswith('.jpeg'):
      
      img = Image.open(img_path)
      img= img.resize((200,200))
      inputs = ImageLoader.load_image(img)
      canvas1.create_text(240,290,fill="blue",font="Helvetica 12 bold",text="Image imported successfully from System!",tag = "read")
      if(checkimport == 1):
          canvas1.delete("selected")
          canvas1.create_text(260,163,fill="black",font="Helvetica 9 ",text=Path(img_path).name,tag = "selected")
      else:
          canvas1.create_text(260,163,fill="black",font="Helvetica 9 ",text=Path(img_path).name,tag = "selected")
          checkimport = 1
      b_next = Button(f2, text='Next',style = 'W.TButton',command=lambda :next_to_predict())
      b_next.place(relx = 0.8, rely = 0.8, anchor = 'se')
      canvas1.delete("no_url")
   else: 
      messagebox.showerror("Plantspector Warning","Error: Sorry, file format not supported or no file selected!") 
def backf1():
    f1.tkraise()
    e_url.delete(0, END)
    canvas1.delete("no_url")

def btn_url(url):
    global img,inputs
    canvas1.delete("no_url")
    try:
        img = Image.open(requests.get(url, stream=True).raw)
        img= img.resize((200,200))
        inputs = ImageLoader.load_image(img)
        canvas1.delete("selected")
        canvas1.delete("read")
        canvas1.create_text(240,290,fill="blue",font="Arial 12 bold",text="Image downloaded successfully from URL!",tag = "read")
        b_next = Button(f2, text='Next',style = 'W.TButton',command=lambda :next_to_predict())
        b_next.place(relx = 0.8, rely = 0.8, anchor = 'se')
    except Exception as e:
        print(e)
        canvas1.create_text(250,240,fill="red",font="Calibri 11 bold",text="Error. Please try again!", tag = "no_url")
        messagebox.showerror("Plant Error",e) 

def topwindow(t):
    global dis_top
    dis_top = Toplevel(root)
    if t == 's':
        dis_top.title("Symptoms")
    else: 
        dis_top.title("Management")
    dis_top.geometry('500x325')
    
def symptom(predresult):
    global dis_top
    if (predresult == 'Cherry (including sour) Powdery mildew'):
        topwindow('s')
        t = "Initial symptoms, often occurring 7 to 10 days after the onset of the first irrigation, are light roughly-circular, powdery looking patches on young, susceptible leaves (newly unfolded, and light green expanding leaves). Older leaves develop an age-related (ontogenic) resistance to powdery mildew and are naturally more resistant to infection than younger leaves." 
        dlbl = Label(dis_top, text = "Cherry Powdery mildew\n\n",font=("Arial", 15))
        dlbl.pack()
        dlbl.config(foreground="green")
        t = textwrap.fill(t, width=70)
        dlbl2 = Label(dis_top, text =t+"\n\n\n\n" ,font=("Arial", 12)).pack()
        dlbl3 = Label(dis_top, text ="Source:http://treefruit.wsu.edu/crop-protection/disease-management/cherry-powdery-mildew" ,font=("Arial", 8))
        dlbl3.pack()
        dlbl3.config(foreground="blue")
   
    elif (predresult == 'Grape Esca (Black Measles)'):
        topwindow('s')
        t = "The foliar symptom of Esca is an interveinal striping. The stripes, which start out as dark red in red cultivars and yellow in white cultivars, dry and become necrotic. Foliar symptoms may occur at any time during the growing season, but are most prevalent during July and August. They are often restricted to an individual shoot or to shoots originating from the same spur or cane. Symptomatic leaves can dry completely and drop prematurely. On berries, small, round, dark spots each bordered by a brown-purple ring, may occur." 
        dlbl = Label(dis_top, text = "Grape Esca (Black Measles)\n\n",font=("Arial", 15))
        dlbl.pack()
        dlbl.config(foreground="green")
        t = textwrap.fill(t, width=70)
        dlbl2 = Label(dis_top, text =t+"\n\n\n\n" ,font=("Arial", 12)).pack()
        dlbl3 = Label(dis_top, text ="Source:https://www2.ipm.ucanr.edu/agriculture/grape/esca-black-measles/" ,font=("Arial", 8))
        dlbl3.pack()
        dlbl3.config(foreground="blue")
         
    else:
         messagebox.showinfo(title="Symptoms", message="More info coming soon!!!")


def manage(predresult):
    global dis_top
    if (predresult == 'Cherry (including sour) Powdery mildew'):
        topwindow('m')
        t = " • Manage irrigation. In the arid west in a typical dry spring, early irrigation may stimulate early cherry powdery mildew infections.\n  •Pruning. Humid conditions favor cherry powdery mildew. A well pruned canopy will promote more air flow and leaf drying, reducing these humid conditions favorable for disease.\n The key to managing powdery mildew on the fruit is to keep the disease off of the leaves. Most synthetic fungicides are preventative, not eradicative, so be pro-active about disease prevention." 
        dlbl = Label(dis_top, text = "Cherry Powdery mildew\n\n",font=("Arial", 15))
        dlbl.pack()
        dlbl.config(foreground="green")
        t = textwrap.fill(t, width=70)
        dlbl2 = Label(dis_top, text =t+"\n\n\n\n" ,font=("Arial", 12)).pack()
        dlbl3 = Label(dis_top, text ="Source:http://treefruit.wsu.edu/crop-protection/disease-management/cherry-powdery-mildew" ,font=("Arial", 8))
        dlbl3.pack()
        dlbl3.config(foreground="blue")
   
    elif (predresult == 'Grape Esca (Black Measles)'):
        topwindow('m')
        t = "Preventative practices (delayed pruning, double pruning, and applications of pruning-wound protectants) are the most effective management approach for all trunk diseases. When adopted in young vineyards (i.e., under 5 years old) and used on an annual basis, these practices are likely to extend the profitable lifespan of a vineyard. In summer, when there is a reduced chance of rainfall, practice good sanitation by cutting off these cankered portions of the vine beyond the canker, to where wood appears healthy. Then remove diseased, woody debris from the vineyard and destroy it." 
        dlbl = Label(dis_top, text = "Grape Esca (Black Measles)\n\n",font=("Arial", 15))
        dlbl.pack()
        dlbl.config(foreground="green")
        t = textwrap.fill(t, width=70)
        dlbl2 = Label(dis_top, text =t+"\n\n\n\n" ,font=("Arial", 12)).pack()
        dlbl3 = Label(dis_top, text ="Source:https://www2.ipm.ucanr.edu/agriculture/grape/esca-black-measles/" ,font=("Arial", 8))
        dlbl3.pack()
        dlbl3.config(foreground="blue")
         
    else:
         messagebox.showinfo(title="Management", message="More info coming soon!!!")


def predict():    
    global inputs,b4
    b4['state'] = DISABLED
    myprogress = Progressbar(f3, orient=HORIZONTAL, length=200, mode='determinate')
    myprogress.place(relx = 0.9, rely = 0.25, anchor = 'se')
    lbl1 = Label(f3, text="")
    lbl1.place(relx = 0.94, rely = 0.30, anchor = 'se')
    lbl1.config(text='Enhancing image resolution by EDSR...')
    mylbl = Label(f3, text="")
    mylbl.place(relx = 0.97, rely = 0.25, anchor = 'se')
    mylbl.config(text=str(myprogress['value'])+'%')
    f3.update_idletasks()
    global supermodel
    super_im = supermodel(inputs)
    ImageLoader.save_image(super_im, './scaled_4x.png')
    myprogress['value'] = 30
    mylbl.config(text=str(myprogress['value'])+'%')
    f3.update_idletasks()
    time.sleep(2)
    lbl2 = Label(f3, text="")
    lbl2.place(relx = 0.85, rely = 0.35, anchor = 'se')
    lbl2.config(text='Loading ResNet model...')
    global model1,test_gen,canvas3
    labels = (test_gen.class_indices)
    labels = dict((v,k) for k,v in labels.items())
    en = (Image.open("./scaled_4x.png"))
    re_en= en.resize((200,200))
    re_en.save("./scaled_4x.png")
    enhanced = im.load_img("./scaled_4x.png", target_size = (100,100))
    myprogress['value'] += 40
    mylbl.config(text=str(myprogress['value'])+'%')
    f3.update_idletasks()
    time.sleep(2)
    x = im.img_to_array(enhanced)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    result = model1.predict(x)
    max_prob_index = np.unravel_index(result.argmax(), result.shape)
    max_prob = "{:.2f}".format(result[max_prob_index])
    result_index=np.argmax(result,axis=1)
    lbl3 = Label(f3, text="")
    lbl3.place(relx = 0.80, rely = 0.40, anchor = 'se')
    lbl3.config(text='Detecting disease...')
    pred_class = [labels[k] for k in result_index]
    pred_result = re.split('[_]+',pred_class[0])
    pred_result = ' '.join(pred_result)
    myprogress['value'] += 30
    mylbl.config(text=str(myprogress['value'])+'%')
    f3.update_idletasks()
    time.sleep(2)
    global b5
    if (pred_result.find('healthy') != -1):
        canvas3.create_text(250,260,fill="green",font="Times 13",text="✅ Your plant is disease-free!")
        canvas3.create_text(250,285,fill="green",font="Calibri 17 bold",text=pred_result)
        canvas3.create_text(250,310,fill="black",font="Arial 12",text="Confidence: "+str(max_prob))
    else:   
        canvas3.create_text(250,250,fill="red",font="Times 13 ",text="⚠️ Your plant has disease!")
        canvas3.create_text(250,275,fill="red",font="Calibri 16 bold",text=pred_result)
        canvas3.create_text(250,300,fill="black",font="Arial 12",text="Confidence: "+str(max_prob))
        canvas3.create_text(250,330,fill="green",font="Times 14 ",text="Check prevention strategies below")
        b5 = Button(f3, text='Symptoms',style = 'W.TButton',command= lambda :symptom(pred_result)).place(relx = 0.75, rely = 0.8, anchor = 'se')
        b6 = Button(f3, text='Management',style = 'W.TButton',command= lambda :manage(pred_result)).place(relx = 0.5, rely = 0.8, anchor = 'se')
        



def next_to_predict():
    global img,canvas3,b4,bimage
    canvas3 = Canvas(f3,width=500,height=500)
    bimage = ImageTk.PhotoImage(Image.open("Maiden1.jpg"))
    canvas3.create_image(0,0,anchor=NW,image=bimage)
    canvas3.place(relx = 0.5, rely = 0.5, anchor = 'center')
    f3.tkraise()
    img.thumbnail((200,200))
    img1 = ImageTk.PhotoImage(img)
    lbl = Label(f3)
    lbl.place(relx = 0.07, rely = 0.03, anchor = 'nw')
    lbl.configure(image=img1)
    lbl.image = img1
    b4 = Button(f3, text='Detect',style = 'W.TButton',state = NORMAL,command=lambda :predict())
    b4.place(relx = 0.8, rely = 0.12, anchor = 'ne')
    bback = Button(f3, text='Back',style = 'W.TButton',command= lambda : backf2()).place(relx = 0.3, rely = 0.9, anchor = 'se')
    
def backf2():
    canvas1.delete("no_url")
    f2.tkraise()
    for widget in f3.winfo_children():
       widget.destroy()
    canvas1.delete("read")






root = Tk() 
#img = PhotoImage(file='doctor.ico')
#root.tk.call('wm', 'iconphoto', root._w, img)
root.title('Plantspector') 
root.geometry("500x500")
root.resizable(0, 0) 
style = Style() 
style.configure('W.TButton', font = ('Calibri', 11),foreground = 'black',highlightbackground = 'blue')
f1 = Frame(root, width=500, height=500)
f2 = Frame(root, width=500, height=500)
f3 = Frame(root, width=500, height=500)

f1.grid(row=0, column=0, sticky = 'news')
f2.grid(row=0, column=0, sticky = 'news')
f3.grid(row=0, column=0, sticky = 'news')

canvas=Canvas(f1,width=500,height=500)
image=ImageTk.PhotoImage(Image.open("Maiden1.jpg"))
canvas.create_image(0,0,anchor=NW,image=image)
canvas.place(relx = 0.5, rely = 0.5, anchor = 'center')
canvas.create_text(230,20,fill="black",font="Times 13",text="Welcome")
canvas.create_text(230,170,fill="darkblue",font="Arial 17 bold ",text="PLANTSPECTOR")
canvas.create_text(240,200,fill="black",font="Calibri 14 bold ",text="An Intelligent Framework for Plant Disease Detection")
b1 = Button(f1, text='Start', style = 'W.TButton',command=lambda :f2.tkraise()).place(relx = 0.75, rely = 0.75, anchor = 'se')
canvas1 = Canvas(f2,width=500,height=500)
#image1 = ImageTk.PhotoImage(Image.open("Plant wallpaper2.jpg"))
canvas1.create_image(0,0,anchor=NW,image=image)
canvas1.place(relx = 0.5, rely = 0.5, anchor = 'center')
b2 = Button(f2, text='Back',style = 'W.TButton',command= lambda : backf1()).place(relx = 0.4, rely = 0.8, anchor = 'se')
canvas1.create_text(240,70,fill="darkblue",font="Calibri 14 bold",text="Import your image from System or Web")
canvas1.create_text(250,450,fill="blue",font="Arial 9",text="Images of all sizes are automatically resized. Formats accepted: jpg, png")
b = Button(f2, text='Browse image',style = 'W.TButton',command= lambda :imgimport()).place(relx = 0.55, rely = 0.25, anchor = 'ne')
canvas1.create_text(70,220,fill="black",font="Calibri 11 bold",text="URL")
e_url = Entry(f2)
e_url.place(x = 90,y = 205,width=300,height=25)
b3 = Button(f2, text='Download',style = 'W.TButton',command= lambda :btn_url(e_url.get())).place(relx = 0.96, rely = 0.41, anchor = 'ne')

f1.tkraise()
root.mainloop() 
