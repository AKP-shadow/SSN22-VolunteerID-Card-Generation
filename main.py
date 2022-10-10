import pandas as pd
from pandas import read_excel
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def gen(code,country) :
    id = Image.open("template.png") #id card template
    country = country.upper()
    try:
        path = "C:\\Users\\aadhi\\OneDrive\\Desktop\\idcardgen\\idcardgen\\flags\\" #location of the data such as images to be inserted in the id
        path += code
        path += ".png"
        flag  = Image.open(path)

        #positioning of the image on the id based on template dimensions
        basewidth = 984
        wpercent = (basewidth/float(flag.size[0]))
        hsize = int((float(flag.size[1])*float(wpercent)))
        flag = flag.resize((basewidth,hsize), Image.Resampling.LANCZOS)

        #pasting the image on the template
        temp=Image.open("template.png")
        temp.paste(flag, (0,(1329-hsize)))

        #pasting the text on the id along with scaling font size
        temp.paste(id, (0,0),id)
        if (len(country)<=11) :
            font = ImageFont.truetype("arial.ttf", 100, encoding="unic")
        elif (len(country)>11 and len(country)<=17):
            font = ImageFont.truetype("arial.ttf", 70, encoding="unic")
        elif(len(country)>17 and len(country)<=25) :
            font = ImageFont.truetype("arial.ttf", 55, encoding="unic")
        else :
            font = ImageFont.truetype("arial.ttf", 40, encoding="unic")

        draw = ImageDraw.Draw(temp)
        w, h = draw.textsize(country, font=font)
        draw.text(((984-w)/2, 1329-((1329-h)/5)), country, 'white', font)

        #saving the id
        svtext = "./ids/disec_"
        svtext += country
        svtext += ".png"
        temp.save(svtext)
        #temp.convert("CMYK").save("testcmyk.jpeg")
        print("done")
    except:
        pass


#reads superset file for id and name
data = pd.read_csv("flagdata.csv")
flags = pd.DataFrame(data)

#reads set of id's to be generated
sheet = 'UNSC'
file = 'matrix.xlsx'

df = read_excel(file,sheet)
 
i = 0
j = 0
# print(df)
while (i<len(df)) :
    gen(flags.loc[i,"Code"],flags.loc[i,"Country"])
    i = i+1

# #log file for all ids created
# df.to_csv("./ids/disec_done.csv")
