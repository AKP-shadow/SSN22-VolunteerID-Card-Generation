import pandas as pd
from pandas import read_excel
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def gen(code, country) :
    id = Image.open("disec.png") #id card template
    country = country.upper()

    path = "C:\\Users\\thean\\Downloads\\MUN\\ID\\flags\\" #location of the data such as images to be inserted in the id
    path += code
    path += ".png"
    flag  = Image.open(path)

    #positioning of the image on the id based on template dimensions
    basewidth = 984
    wpercent = (basewidth/float(flag.size[0]))
    hsize = int((float(flag.size[1])*float(wpercent)))
    flag = flag.resize((basewidth,hsize), Image.ANTIALIAS)

    #pasting the image on the template
    temp=Image.open("temp.png")
    temp.paste(flag, (0,(1329-hsize)))

    #pasting the text on the id along with scaling font size
    temp.paste(id, (0,0),id)
    if (len(country)<=11) :
        font = ImageFont.truetype("Metropolis-Black.ttf", 100, encoding="unic")
    elif (len(country)>11 and len(country)<=17):
        font = ImageFont.truetype("Metropolis-Black.ttf", 70, encoding="unic")
    elif(len(country)>17 and len(country)<=25) :
        font = ImageFont.truetype("Metropolis-Black.ttf", 55, encoding="unic")
    else :
        font = ImageFont.truetype("Metropolis-Black.ttf", 40, encoding="unic")

    draw = ImageDraw.Draw(temp)
    w, h = draw.textsize(country, font=font)
    draw.text(((984-w)/2, 1329-((1329-h)/5)), country, 'white', font)

    #saving the id
    svtext = "disec_"
    svtext += country
    svtext += ".png"
    temp.save(svtext)
    #temp.convert("CMYK").save("testcmyk.jpeg")
    print("done")


#reads superset file for id and name
data = pd.read_csv("flagdata.csv")
flags = pd.DataFrame(data)

#reads set of id's to be generated
sheet = 'DISEC'
file = 'matrix.xlsx'

df = read_excel(file,sheet)

cnt = set(df["Country"]).intersection(set(flags["Country"]))

#calls the function to gnerate
merg = pd.merge(df, flags, on='Country')
i = 0
j = 0
while (i<len(merg)) :
    gen(merg.loc[i,"Code"],merg.loc[i,"Country"])
    i = i+1

#log file for all ids created
merg.to_csv("disec_done.csv")
