
from PIL import Image,ImageDraw,ImageFont,ImageOps
from cairosvg import svg2png
from io import BytesIO
import os
 
TEMPLATE_SIZE = (453,615)                               #TEMPLATE RESIZE ------------>CHANGE HERE!!
FONT_MAIN = "./fonts/arial.ttf"                         #FONT STYLE  ------------>CHANGE HERE!!



NAME_FONT_SIZE = 35
NAME_ADJUSTMENT_PADDING_X_AXIS = 0
NAME_ADJUSTMENT_PADDING_Y_AXIS = -20
NAME_TEXT_COLOR = 'black'

DESIGNATION_FONT_SIZE = 30
DESIGNATION_ADJUSTMENT_PADDING_X_AXIS = 10
DESIGNATION_ADJUSTMENT_PADDING_Y_AXIS = 20
DESIGNATION_TEXT_COLOR = 'black'


STUDENT_PIC_BORDER_COLOR = "#1d6dad"
STUDENT_PIC_ADJUSTMENT_X_AXIS = 0.305
STUDENT_PIC_ADJUSTMENT_Y_AXIS = 0.3
STUDENT_PIC_SIZE = (170,200)                                  #IMAGE RESIZE ------------>CHANGE HERE!!


# Get the list of all files and directories
def get_file_names(path):
    dir_list = os.listdir(path)
    return dir_list




def frame(im, border_color,thickness=5):
    # Get input image width and height, and calculate output width and height
    iw, ih = im.size
    ow, oh = iw+2*thickness, ih+2*thickness
    # Draw outer black rounded rect into memory as PNG
    outer = f'<svg width="{ow}" height="{oh}" style="background-color:none"><rect rx="20" ry="20" width="{ow}" height="{oh}" fill="{border_color}"/></svg>'
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
 
def gen(name,designation,format) :
    id = Image.open("template.jpeg") #id card template
    # name = name.upper()
    # try:
    path = "./student_pics/ComSoc/" #location of the data such as images to be inserted in the id (BASED ON REGISTER NO)
    path += str(name+'_'+designation)
    path += format
    # print(path)
    student_pic  = Image.open(path)

    #positioning of the image on the id based on template dimensions
    basewidth = id.size[0]//4
    wpercent = (basewidth/float(student_pic.size[0]))
    
    hsize = int((float(student_pic.size[1])*float(wpercent)))+200
    # print("hsize:",hsize,"wpercent:",wpercent)
    # student_pic = student_pic.resize((basewidth,hsize), Image.Resampling.LANCZOS)
    
    
    student_pic = student_pic.resize(STUDENT_PIC_SIZE, Image.Resampling.LANCZOS)
    student_pic_background = frame(student_pic,border_color=STUDENT_PIC_BORDER_COLOR)
    # rectangle(student_pic)
    #Pasting student image onto the TEMPLATE
    temp=Image.open("template.jpeg")                                                #TEMPLATE-----------------> CHANGE HERE!!
    temp = temp.resize(TEMPLATE_SIZE)
    
    # temp.paste(student_pic, (int(temp.size[0]*0.315) ,int(temp.size[1]*0.3)))        #IMAGE ALIGNMENT----------> CHANGE HERE!!
    temp.paste(student_pic_background, (int(temp.size[0]*STUDENT_PIC_ADJUSTMENT_X_AXIS) ,int(temp.size[1]*STUDENT_PIC_ADJUSTMENT_Y_AXIS)),student_pic_background)        #IMAGE ALIGNMENT----------> CHANGE HERE!!
    # print(int(temp.size[0]-STUDENT_PIC_SIZE[0]//2))
 
    t = NAME_FONT_SIZE
    if (len(name)<=11) :
        font_name = ImageFont.truetype(FONT_MAIN, int(NAME_FONT_SIZE), encoding="unic")
    elif (len(name)>11 and len(name)<=17):
        font_name = ImageFont.truetype(FONT_MAIN, int(NAME_FONT_SIZE*0.9), encoding="unic")
        t = int(NAME_FONT_SIZE*0.9)
    elif(len(name)>17 and len(name)<=25) :
        font_name = ImageFont.truetype(FONT_MAIN, int(NAME_FONT_SIZE*0.75), encoding="unic")
        t  = int(NAME_FONT_SIZE*0.75)
    else :
        font_name = ImageFont.truetype(FONT_MAIN, int(NAME_FONT_SIZE*0.6), encoding="unic")
        t = int(NAME_FONT_SIZE*0.6)
        
        
        
    s=DESIGNATION_FONT_SIZE
    if (len(designation)<=11) :                                                     #DESIGNATION FONT---------> CHANGE HERE!!
        font_designation = ImageFont.truetype(FONT_MAIN, int(DESIGNATION_FONT_SIZE), encoding="unic")
    elif (len(designation)>11 and len(designation)<=17):
        font_designation = ImageFont.truetype(FONT_MAIN, int(DESIGNATION_FONT_SIZE*0.8), encoding="unic")
        s = int(DESIGNATION_FONT_SIZE*0.8)
    elif(len(designation)>17 and len(designation)<=25) :
        font_designation = ImageFont.truetype(FONT_MAIN, int(DESIGNATION_FONT_SIZE*0.67), encoding="unic")
        s=int(DESIGNATION_FONT_SIZE*0.67)
    else :
        font_designation = ImageFont.truetype(FONT_MAIN, int(DESIGNATION_FONT_SIZE*0.5), encoding="unic")
        s = int(DESIGNATION_FONT_SIZE*0.5)
        
        
    
            
    print(s)
    draw = ImageDraw.Draw(temp)
    w, h = draw.textsize(name, font=font_name)
    draw.text(((temp.size[0]-w)/2 + NAME_ADJUSTMENT_PADDING_X_AXIS, temp.size[1]-((temp.size[1]-h)/4)+NAME_ADJUSTMENT_PADDING_Y_AXIS), name, NAME_TEXT_COLOR, font_name)                            #NAME TEXT INSERTED HERE!!!
    desig_adjust_old = len(designation)*DESIGNATION_ADJUSTMENT_PADDING_X_AXIS * (0.05*s)
    if len(designation)>10:
        desig_adjust_old = len(designation) * DESIGNATION_ADJUSTMENT_PADDING_X_AXIS * ( 0.046*s)
    if len(designation)>15:
        desig_adjust_old = len(designation) * DESIGNATION_ADJUSTMENT_PADDING_X_AXIS * (0.049*s)
    if len(designation)>=20:
        desig_adjust_old = len(designation) * DESIGNATION_ADJUSTMENT_PADDING_X_AXIS * (0.047*s)
    if len(designation)>=25:
        desig_adjust_old = len(designation) * DESIGNATION_ADJUSTMENT_PADDING_X_AXIS * (0.052*s)
 
    draw.text(((temp.size[0]- desig_adjust_old)//2, temp.size[1]-((temp.size[1]-h)/4)+DESIGNATION_ADJUSTMENT_PADDING_Y_AXIS), designation, DESIGNATION_TEXT_COLOR, font=font_designation )    #DESIGNATION TEXT INSERTED HERE!!
   
    
    temp.resize((453,615),Image.Resampling.LANCZOS)
    #saving the id
    svtext = "./ids/"
    svtext += str(name+'_'+designation)+'_'+str(designation)
    svtext += ".png"
    temp.save(svtext)
    print("done")
    # except:
    #     pass


#main file
for i in get_file_names('.\student_pics\ComSoc'):
    name = i.split('_')[0]
    designation = i.split('_')[1][:-4]
    format = i.split('_')[1][-4:]
    if format=='jpeg':
        format= format
    gen(name,designation,format)

