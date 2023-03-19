 
from PIL import Image,ImageDraw,ImageFont
import os
import pandas as pd
import shutil
TEMPLATE_SIZE = (453,615)                               #TEMPLATE RESIZE ------------>CHANGE HERE!!
FONT_MAIN = "./fonts/Sukar black.ttf"                         #FONT STYLE  ------------>CHANGE HERE!!
FONT_SECON = "./fonts/BarlowCondensed-Black.ttf"


NAME_FONT_SIZE = 107
PROF_FONT_SIZE = 9*NAME_FONT_SIZE/24

NAME_ADJUSTMENT_PADDING_X_AXIS = 0.6367
NAME_ADJUSTMENT_PADDING_Y_AXIS = 0.62
PROF_TEXT_COLOR = '#2c2d2d'
NAME_TEXT_COLOR = 'white'

INSTITUTION_NAME_SIZE = NAME_FONT_SIZE*18/24
DESIGNATION_ADJUSTMENT_PADDING_X_AXIS = 10
DESIGNATION_ADJUSTMENT_PADDING_Y_AXIS = 40
DESIGNATION_TEXT_COLOR = 'white'


STUDENT_PIC_BORDER_COLOR = "#1d6dad"
STUDENT_PIC_ADJUSTMENT_X_AXIS = 0.305
STUDENT_PIC_ADJUSTMENT_Y_AXIS = 0.3
STUDENT_PIC_SIZE = (170,200)                                  #IMAGE RESIZE ------------>CHANGE HERE!!


# Get the list of all files and directories
def CreateDirectory(path):
    absolute_path = os.path.dirname(__file__)
    relative_path = f"test/{path}"
    full_path = os.path.join(absolute_path, relative_path)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
 




 
def gen(name,designation,event_name) :
    temp=Image.open(f"./templates/{event_name}.png") 
    print(name,designation,event_name)                  #TEMPLATE-----------------> CHANGE HERE!!
    print(temp.size)
    # temp = temp.resize(TEMPLATE_SIZE)
 
 
    t = NAME_FONT_SIZE
    font_name = ImageFont.truetype(FONT_MAIN, int(NAME_FONT_SIZE), encoding="unic" )
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
    font_institution = ImageFont.truetype(FONT_SECON, int(INSTITUTION_NAME_SIZE), encoding="unic", )
    if (len(designation)<=16) :                                                     #DESIGNATION FONT---------> CHANGE HERE!!
        font_institution = ImageFont.truetype(FONT_MAIN, int(INSTITUTION_NAME_SIZE), encoding="unic")
    elif (len(designation)>16 and len(designation)<=25):
        font_institution = ImageFont.truetype(FONT_MAIN, int(INSTITUTION_NAME_SIZE*0.8), encoding="unic")
        s = int(INSTITUTION_NAME_SIZE*0.8)
    elif(len(designation)>25 and len(designation)<=50) :
        font_institution = ImageFont.truetype(FONT_MAIN, int(INSTITUTION_NAME_SIZE*0.67), encoding="unic")
        s=int(INSTITUTION_NAME_SIZE*0.67)
 
        
        
    
            
    draw = ImageDraw.Draw(temp)
    l = draw.textlength(designation, font=font_institution)
    
    name = name.split(' ')
    print(l)
    print(name)
    h = font_name.getsize("S")[1]
    # print(h)

    w = draw.textlength(" ".join(name[0:]).strip('\n'), font=font_name)
    draw.text((((temp.size[0]-w)/2), NAME_ADJUSTMENT_PADDING_Y_AXIS*temp.size[1])," ".join(name), NAME_TEXT_COLOR, font_name,stroke_width=1)                            #NAME TEXT INSERTED HERE!!!
    filename = name[0]
        
    draw.text((((temp.size[0]-l)/2),  2*temp.size[1]/3+t/1.3), designation, DESIGNATION_TEXT_COLOR, font=font_institution )    #DESIGNATION TEXT INSERTED HERE!!
   
    
    CreateDirectory(f"{event_name}")
 
    svtext = f"./test/{event_name}/"+name[0]+".png"
    temp.save(svtext)
    print("done")
 
 
 
 


# gen("Shiva Shanmugam","3rd, CSE","RAPID FIRE")
xl = pd.read_excel('organizers.xlsx')
print(xl.columns)

for i in xl.index:
    person = xl.iloc[i]
    gen(person['Name'],person['Year']+", "+person['Department'],person['Event'].strip())

 