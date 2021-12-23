import os
from PIL import Image, ImageDraw, ImageFont
import PIL

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

def generate_res_images(foldername,baseheight=100):

    images = load_images_from_folder(foldername)
    res_images_temp = []
    i=0
    # os.makedirs(foldername+"resized")
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
            i+=1
            img = img.resize((a,hsize), Image.ANTIALIAS)
            # print(img.size[0])
            res_images_temp.append(img)
            img.save(foldername+"resized" + "/"+"{}_doodle_resized".format(i)+".png")
        except Exception as e:
            print(e)
generate_res_images("shapes2")