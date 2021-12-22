import PIL
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        try:
            img = Image.open(os.path.join(folder,filename))
        except Exception as e:
            print(e)
        if img is not None:
            images.append(img)
    print("images Loaded from folder")
    return images

def generate_black_code_image(W,H,code,font_size=36,font_type="f.ttf"):
    
    black_image = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    # black_image = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    font = ImageFont.truetype(font_type,font_size)
    font.set_variation_by_name("Bold")
    d1 = ImageDraw.Draw(black_image)
    w, h = d1.textsize(str(code),font=font)
    d1.text(((W-w)/2,(H-1.5*h)/2), str(code), fill = (255, 255, 255, 255),font = font)
    return black_image



def generate_image(seed,foldername,code,codeW=500,codeH=100,width=900,height=1600,m=100,k=200,baseheight=100,th=50,Density=200,font_size=56,font_type="f.ttf"):
    print("Starting FlamClub Algo................................")
    print("Default value of width == 900....\nDefault value of height == 1600....\nDefault value of margin in width == 200....\nDefault value of margin in height == 100....\nDefault value of doodle height == 100....\nDefault value of distance b/w doodle == 50....\nDefault value of density of doodles == 200....\n")
    images = load_images_from_folder(foldername)



    # while True:
    #     foldername = input("Please enter folder path that contains the doodles")
    #     if foldername: break



    # width = int( input("Enter height of Document") or 900)
    # height = int( input("Enter width of Document") or 1600)
    # m =int( input("Enter margin in height of Document") or 100)
    # k =int( input("Enter margin in width of Document") or 200)
    # baseheight = int( input("Enter height of doodle") or 100)
    # # r = 5
    # while True:
    #     seed = input('Please Enter seed')
    #     if seed: break
    # th = int( input("Enter the distance between doodles") or 50)
    # Density = int( input("Enter density of doodles") or 200)


    res_images = []
    for img in images:
        if img.size[0]>img.size[1]:
            wpercent = (baseheight/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            a = baseheight
        else:
            hsize = baseheight
            wpercent = (baseheight/float(img.size[1]))
            a = int((float(img.size[0])*float(wpercent)))
        try:
            img = img.resize((a,hsize), Image.ANTIALIAS)
            # print(img.size[0])
            res_images.append(img)
        except Exception as e:
            print(e)

    points =[]

    random.seed(seed)
    for i in  range(Density):
        _x = random.randint(0,width-m)
        _y = random.randint(0,height-k)
        add =True
        for j in points:
            dist = np.linalg.norm(np.array(j)- np.array((_x,_y)))
            if(dist < th ):
                add= False
                break
            pass
        if add:
            points.append((_x,_y))

    transparent_image = Image.new('RGBA', (width, height), (0, 0, 0, 255))

    new_image = transparent_image.copy()
    # for i in points:
    #     draw = ImageDraw.Draw(new_image)
    #     leftUpPoint = (i[0]-r, i[1]-r)
    #     rightDownPoint = (i[0]+r, i[1]+r)
    #     twoPointList = [leftUpPoint, rightDownPoint]
    #     # draw.ellipse(twoPointList, fill=(255,0,0,255))

    random.seed(seed)
    for i in points:
        a = random.randint(0,360)
        b = 0.8+ (random.random())/2
        var = random.randint(0,len(res_images)-1)
        puti = res_images[var]
        img = img.resize((int(puti.size[0]*b),int(puti.size[1]*b)), Image.ANTIALIAS)
        puti = puti.rotate(a, PIL.Image.NEAREST, expand = 1)
        new_image.paste(puti, i,puti)

    mid_image = generate_black_code_image(codeW,codeH,code,font_size,font_type)



    text_h = int((new_image.size[1]-mid_image.size[1]*1)/2)
    text_w = int((new_image.size[0]-mid_image.size[0]*1)/2)
    print(text_w,text_h)
    new_image.paste(mid_image,(text_w,text_h), mid_image)
    new_image.show()

    new_image.save("New{}{}{}.png".format(seed,th,baseheight))

generate_image(123123123,"shapes2",353453)