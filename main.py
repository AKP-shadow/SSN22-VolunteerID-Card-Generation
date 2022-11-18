
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import os
import pandas as pd
import shutil
TEMPLATE_SIZE = (453,615)                               #TEMPLATE RESIZE ------------>CHANGE HERE!!
FONT_MAIN = "./fonts/Minion-Bold.otf"                         #FONT STYLE  ------------>CHANGE HERE!!



NAME_FONT_SIZE = 100
PROF_FONT_SIZE = 9*NAME_FONT_SIZE/24

NAME_ADJUSTMENT_PADDING_X_AXIS = 0
NAME_ADJUSTMENT_PADDING_Y_AXIS = -20
PROF_TEXT_COLOR = '#2c2d2d'
NAME_TEXT_COLOR = 'black'

INSTITUTION_NAME_SIZE = NAME_FONT_SIZE*18/24
DESIGNATION_ADJUSTMENT_PADDING_X_AXIS = 10
DESIGNATION_ADJUSTMENT_PADDING_Y_AXIS = 20
DESIGNATION_TEXT_COLOR = '#155e8b'


STUDENT_PIC_BORDER_COLOR = "#1d6dad"
STUDENT_PIC_ADJUSTMENT_X_AXIS = 0.305
STUDENT_PIC_ADJUSTMENT_Y_AXIS = 0.3
STUDENT_PIC_SIZE = (170,200)                                  #IMAGE RESIZE ------------>CHANGE HERE!!


# Get the list of all files and directories
def CreateDirectory(path):
    absolute_path = os.path.dirname(__file__)
    relative_path = f"ids/{path}"
    full_path = os.path.join(absolute_path, relative_path)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    else:
        shutil.rmtree(full_path)           # Removes all the subdirectories!
        os.makedirs(full_path)




 
def gen(name,institution_name,path) :
    institution_name = institution_name.strip('*')
 
    #Pasting student image onto the TEMPLATE
    temp=Image.open("template.png")                                                #TEMPLATE-----------------> CHANGE HERE!!
    print(temp.size)
    # temp = temp.resize(TEMPLATE_SIZE)
 
 
    t = NAME_FONT_SIZE
    font_name = ImageFont.truetype(FONT_MAIN, int(NAME_FONT_SIZE), encoding="unic")
    p = PROF_FONT_SIZE
    font_prof =  ImageFont.truetype(FONT_MAIN, int(PROF_FONT_SIZE), encoding="unic")
    if (len(name)<=16) :
        font_name = ImageFont.truetype(FONT_MAIN, int(NAME_FONT_SIZE), encoding="unic")
    elif (len(name)>16 and len(name)<=25):
        font_name = ImageFont.truetype(FONT_MAIN, int(NAME_FONT_SIZE*0.9), encoding="unic")
        t = int(NAME_FONT_SIZE*0.7)
    else :
        font_name = ImageFont.truetype(FONT_MAIN, int(NAME_FONT_SIZE*0.6), encoding="unic")
        t = int(NAME_FONT_SIZE*0.6)
        
        
        
    s=INSTITUTION_NAME_SIZE
    font_institution = ImageFont.truetype(FONT_MAIN, int(INSTITUTION_NAME_SIZE), encoding="unic", )
    if (len(institution_name)<=16) :                                                     #DESIGNATION FONT---------> CHANGE HERE!!
        font_institution = ImageFont.truetype(FONT_MAIN, int(INSTITUTION_NAME_SIZE), encoding="unic")
    elif (len(institution_name)>16 and len(institution_name)<=25):
        font_institution = ImageFont.truetype(FONT_MAIN, int(INSTITUTION_NAME_SIZE*0.8), encoding="unic")
        s = int(INSTITUTION_NAME_SIZE*0.8)
    elif(len(institution_name)>25 and len(institution_name)<=50) :
        font_institution = ImageFont.truetype(FONT_MAIN, int(INSTITUTION_NAME_SIZE*0.67), encoding="unic")
        s=int(INSTITUTION_NAME_SIZE*0.67)
 
        
        
    
            
    draw = ImageDraw.Draw(temp)
    l,k = draw.textsize(institution_name, font=font_institution)
    name = name.split('.')
    print(l,k)
    print(name)
    if len(name)>1:
        w, h = draw.textsize("".join(name[1:]), font=font_name)
        a, b = draw.textsize(name[0], font=font_name)
        filename = "".join(name[1:])
        
        draw.text((((temp.size[0]-w)/2-a/5) ,2*temp.size[1]/3-h/10), name[0]+'. ', PROF_TEXT_COLOR, font_prof)                            #NAME TEXT INSERTED HERE!!!
    # draw.text(((temp.size[0]-w)/2 + NAME_ADJUSTMENT_PADDING_X_AXIS, temp.size[1]-((temp.size[1]-h)/3)+NAME_ADJUSTMENT_PADDING_Y_AXIS), name[1], NAME_TEXT_COLOR, font_name,stroke_width=2)                            #NAME TEXT INSERTED HERE!!!
        draw.text((((temp.size[0]-w)/2+a/5), 0.6367*temp.size[1]), "".join(name[1:]), NAME_TEXT_COLOR, font_name,stroke_width=1)                            #NAME TEXT INSERTED HERE!!!
    else:
        w, h = draw.textsize(name[0], font=font_name)
        draw.text((((temp.size[0]-w)/2), 0.6367*temp.size[1]), name[0], NAME_TEXT_COLOR, font_name,stroke_width=1)                            #NAME TEXT INSERTED HERE!!!
        filename = name[0]
        
    draw.text((((temp.size[0]-l)/2+0.08*l),  2.1*temp.size[1]/3), institution_name, DESIGNATION_TEXT_COLOR, font=font_institution )    #DESIGNATION TEXT INSERTED HERE!!
   
    
    # temp.resize((453,615),Image.Resampling.LANCZOS)
    #saving the id
    svtext = f"./ids/{path}/"+str(filename.strip()+'_'+institution_name)+".png"
    temp.save(svtext)
    print("done")
    # except:
    #     pass


 
xl = pd.ExcelFile('Order of the Talk - RMS Speakers.xlsx')



# xl.parse(sheet_name)  # read a specific sheet to DataFrame
for sheet_no in range(len( pd.read_excel('Order of the Talk - RMS Speakers.xlsx',sheet_name=None))-1):
    CreateDirectory(xl.sheet_names[sheet_no])
    df = pd.read_excel('Order of the Talk - RMS Speakers.xlsx',sheet_name=sheet_no)
    start=0
    
    for i in df.iloc[:,0]:
        if i == "S. No. ":
            break
        
        start+=1
    start+=1
    for speaker in range(len(df.index)-start):
        if not  df.iloc[:,0].isnull()[start+speaker] and not df.iloc[start+speaker,0]=="S. No. ":
            gen(df.iloc[start+speaker,1],df.iloc[start+speaker,2],xl.sheet_names[sheet_no])
            # print(df.iloc[start+speaker,1])
            # print(df.iloc[start+speaker,2])
    