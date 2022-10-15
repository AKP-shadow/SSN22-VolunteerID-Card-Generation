import numpy as np
import pandas as pd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont,ImageFilter


def add_corners(img, code):
    height,width = img.size
    lum_img = Image.new('L', [height,width] , 0)
    
    draw = ImageDraw.Draw(lum_img)
    draw.pieslice([(0,0), (height,width)], 0, 360, 
                fill = 255, outline = "white")
    img_arr =np.array(img)
    lum_img_arr =np.array(lum_img)
    final_img_arr = np.dstack((img_arr,lum_img_arr))
    Image.fromarray(final_img_arr).save('./temp/'+str(code)+'_test.png')
    

   
 
def gen(code,name,designation) :
    id = Image.open("template.jpeg") #id card template
    name = name.upper()
    # try:
    path = "student_pics/" #location of the data such as images to be inserted in the id (BASED ON REGISTER NO)
    path += str(code)
    path += ".jpg"
    student_pic  = Image.open(path)

    #positioning of the image on the id based on template dimensions
    basewidth = id.size[0]//4
    wpercent = (basewidth/float(student_pic.size[0]))
    
    hsize = int((float(student_pic.size[1])*float(wpercent)))+200
    print("hsize:",hsize,"wpercent:",wpercent)
    image_alignment=(170,200)                                                      #IMAGE RESIZE ------------>CHANGE HERE!!
    # student_pic = student_pic.resize((basewidth,hsize), Image.Resampling.LANCZOS)
    
    
    student_pic = student_pic.resize(image_alignment, Image.Resampling.LANCZOS)
    add_corners(student_pic,code)
    student_pic_round = Image.open('./temp/'+str(code)+'_test.png')
    # student_pic_round.show()
    #Pasting student image onto the TEMPLATE
    temp=Image.open("template.jpeg")                                                #TEMPLATE-----------------> CHANGE HERE!!
    print(temp.size[0]//3,temp.size[0]//3)
    temp.paste(student_pic_round, (int(temp.size[0]*0.32) ,int(temp.size[1]*0.3)))        #IMAGE ALIGNMENT----------> CHANGE HERE!!
    
    
    

    #SCALING OF FONT_NAME                                                               
    if (len(name)<=11) :
        font_name = ImageFont.truetype("arial.ttf", 30, encoding="unic")
    elif (len(name)>11 and len(name)<=17):
        font_name = ImageFont.truetype("arial.ttf", 25, encoding="unic")
    elif(len(name)>17 and len(name)<=25) :
        font_name = ImageFont.truetype("arial.ttf", 20, encoding="unic")
    else :
        font_name = ImageFont.truetype("arial.ttf", 10, encoding="unic")
        
        
        
        
    if (len(designation)<=11) :                                                     #DESIGNATION FONT---------> CHANGE HERE!!
        font_designation = ImageFont.truetype("arial.ttf", 20, encoding="unic")
    elif (len(designation)>11 and len(designation)<=17):
        font_designation = ImageFont.truetype("arial.ttf", 18, encoding="unic")
    elif(len(designation)>17 and len(designation)<=25) :
        font_designation = ImageFont.truetype("arial.ttf", 15, encoding="unic")
    else :
        font_designation = ImageFont.truetype("arial.ttf", 12, encoding="unic")
        
        
        
        
        
    draw = ImageDraw.Draw(temp)
    w, h = draw.textsize(name, font=font_name)
    print(w)
    draw.text(((temp.size[0]-w)/2, temp.size[1]-((temp.size[1]-h)/4)-20), name, 'black', font_name)                            #NAME TEXT INSERTED HERE!!!
    draw.text(((temp.size[0]- len(designation)*12)//2, temp.size[1]-((temp.size[1]-h)/4)+20), designation.upper(), 'black', font=font_designation )    #DESIGNATION TEXT INSERTED HERE!!
   
   
   
    #saving the id
    svtext = "./ids/"
    svtext += str(code)+'_'+str(designation)
    svtext += ".png"
    temp.save(svtext)
    print("done")
    # except:
    #     pass


#reads superset file for id and name
data = pd.read_csv("student_data.csv")
flags = pd.DataFrame(data)

 
i = 0
j = 0
for i in range(len(flags)):
    gen(flags.loc[i,"Register No"],flags.loc[i,"Name"],flags.loc[i,"Designation"])

