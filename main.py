import numpy as np
import pandas as pd
from PIL import Image,ImageDraw,ImageFont,ImageOps
from cairosvg import svg2png
from io import BytesIO
import os
 
TEMPLATE_SIZE = (453,615)                               #TEMPLATE RESIZE ------------>CHANGE HERE!!
IMAGE_SIZE = (170,200)                                  #IMAGE RESIZE ------------>CHANGE HERE!!
FONT_MAIN = "./fonts/arial.ttf"                         #FONT STYLE  ------------>CHANGE HERE!!

# Get the list of all files and directories
def get_file_names(path):
    dir_list = os.listdir(path)
    return dir_list




def frame(im, border_color,thickness=5):
    # Get input image width and height, and calculate output width and height
    iw, ih = im.size
    ow, oh = iw+2*thickness, ih+2*thickness

    # Draw outer black rounded rect into memory as PNG
    outer = f'<svg width="{ow}" height="{oh}" style="background-color:none"><rect rx="20" ry="20" width="{ow}" height="{oh}" fill="#1d6dad"/></svg>'
    png   = svg2png(bytestring=outer)
    outer = Image.open(BytesIO(png))

    # Draw inner white rounded rect, offset by thickness into memory as PNG
    inner = f'<svg width="{ow}" height="{oh}"><rect x="{thickness}" y="{thickness}" rx="20" ry="20" width="{iw}" height="{ih}" fill="white"/></svg>'
    png   = svg2png(bytestring=inner)
    inner = Image.open(BytesIO(png)).convert('L')

    # Expand original canvas with black to match output size
    expanded = ImageOps.expand(im, border=thickness, fill=(29, 109, 173)).convert('RGB')

    # Paste expanded image onto outer black border using inner white rectangle as mask
    outer.paste(expanded, None, inner)
    return outer
 
def gen(name,designation) :
    id = Image.open("template.jpeg") #id card template
    name = name.upper()
    # try:
    path = "student_pics/" #location of the data such as images to be inserted in the id (BASED ON REGISTER NO)
    path += str(name+'_'+designation)
    path += ".jpg"
    student_pic  = Image.open(path)

    #positioning of the image on the id based on template dimensions
    basewidth = id.size[0]//4
    wpercent = (basewidth/float(student_pic.size[0]))
    
    hsize = int((float(student_pic.size[1])*float(wpercent)))+200
    print("hsize:",hsize,"wpercent:",wpercent)
    # student_pic = student_pic.resize((basewidth,hsize), Image.Resampling.LANCZOS)
    
    
    student_pic = student_pic.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
    student_pic_background = frame(student_pic,(29, 109, 173))
    # rectangle(student_pic)
    #Pasting student image onto the TEMPLATE
    temp=Image.open("template.jpeg")                                                #TEMPLATE-----------------> CHANGE HERE!!
 
    
    temp.paste(student_pic_background, (int(temp.size[0]*0.3) ,int(temp.size[1]*0.3)))        #IMAGE ALIGNMENT----------> CHANGE HERE!!
    print(int(temp.size[0]-IMAGE_SIZE[0]//2))
 

    if (len(name)<=11) :
        font_name = ImageFont.truetype(FONT_MAIN, 30, encoding="unic")
    elif (len(name)>11 and len(name)<=17):
        font_name = ImageFont.truetype(FONT_MAIN, 25, encoding="unic")
    elif(len(name)>17 and len(name)<=25) :
        font_name = ImageFont.truetype(FONT_MAIN, 20, encoding="unic")
    else :
        font_name = ImageFont.truetype(FONT_MAIN, 10, encoding="unic")
        
        
        
        
    if (len(designation)<=11) :                                                     #DESIGNATION FONT---------> CHANGE HERE!!
        font_designation = ImageFont.truetype(FONT_MAIN, 20, encoding="unic")
    elif (len(designation)>11 and len(designation)<=17):
        font_designation = ImageFont.truetype(FONT_MAIN, 18, encoding="unic")
    elif(len(designation)>17 and len(designation)<=25) :
        font_designation = ImageFont.truetype(FONT_MAIN, 15, encoding="unic")
    else :
        font_designation = ImageFont.truetype(FONT_MAIN, 12, encoding="unic")
        
        
            
        
    draw = ImageDraw.Draw(temp)
    w, h = draw.textsize(name, font=font_name)
    print(w)
    draw.text(((temp.size[0]-w)/2, temp.size[1]-((temp.size[1]-h)/4)-20), name, 'black', font_name)                            #NAME TEXT INSERTED HERE!!!
    draw.text(((temp.size[0]- len(designation)*12)//2, temp.size[1]-((temp.size[1]-h)/4)+20), designation, 'black', font=font_designation )    #DESIGNATION TEXT INSERTED HERE!!
   
    
    temp.resize((453,615),Image.Resampling.LANCZOS)
    #saving the id
    svtext = "./ids/"
    svtext += str(name+'_'+designation)+'_'+str(designation)
    svtext += ".png"
    temp.resize(TEMPLATE_SIZE).save(svtext)
    print(temp.size)
    print("done")
    # except:
    #     pass


#main file
for i in get_file_names('.\student_pics'):
    name = i.split('_')[0]
    designation = i.split('_')[1][:-4]
    gen(name,designation)

