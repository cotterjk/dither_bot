import random
import json
import os
from PIL import Image
from PIL.ImageOps import colorize, grayscale
from datetime import datetime

pos_ind_x, pos_ind_y = 3, 3 #position index to select detail phrase and emoji

colors_light = ['aquamarine','bisque','burlywood','cadetblue','coral','cornflowerblue','cornsilk','crimson','darkorange','darksalmon','darkseagreen','deepskyblue','hotpink','khaki','lavenderblush','lemonchiffon','lightblue','lightcoral','lightgreen','lightpink','lightsalmon','lightskyblue','lightsteelblue','lightyellow','mediumaquamarine','moccasin','palegoldenrod','palegreen','paleturquoise','papayawhip','peachpuff','pink','plum','powderblue','salmon','sandybrown','seagreen','skyblue','springgreen','tan','thistle','tomato','turquoise','violet','wheat','yellow','yellowgreen']
colors_dark = ['brown','darkcyan','darkgoldenrod','darkgreen','darkmagenta','darkolivegreen','darkred','darkslategray','dimgray','dodgerblue','firebrick','goldenrod','gray','green','indianred','indigo','maroon','mediumorchid','midnightblue','navy','olive','olivedrab','orangered','orchid','palevioletred','peru','purple','rebeccapurple','rosybrown','royalblue','saddlebrown','sienna','slateblue','slategray','slategrey','steelblue','teal']
choice_colors_light = random.choice(colors_light)
choice_colors_dark = random.choice(colors_dark)

#———RANDOM IMAGE SELECTION———#
src_folders = os.listdir("source_photos/")
if ".DS_Store" in src_folders: src_folders.remove(".DS_Store")
src_folder_choice = random.choice(src_folders)

src_photos = os.listdir("source_photos/" + src_folder_choice + "/")
if ".DS_Store" in src_photos: src_photos.remove(".DS_Store")
src_photo_choice = random.choice(src_photos)

img = Image.open("source_photos/" + src_folder_choice + "/" + src_photo_choice)

#———PRE-PROCESSINGS———#

re_size = 256
w, h = img.size
c_size = random.randint(300, min(w,h)-100)
crop_x = random.randint(0, w-c_size)
crop_y = random.randint(0, h-c_size)

#———PROCESS IMAGE———#
img = img.crop((crop_x,crop_y,(crop_x+c_size),(crop_y+c_size)))
img = img.resize((re_size,re_size))
img = img.convert("1",dither=Image.FLOYDSTEINBERG) # convert to 1-bit dithered
img = img.convert("L") #convert for colorization

#———COLOR———#
img = colorize(img, black=choice_colors_dark, white=choice_colors_light)

cap_string = "placeholder caption string 👀"
cap_string = "⚫️🎨 " + choice_colors_dark + " / " + choice_colors_light + " 🎨⚪️"

#———CAPTION FILM INFO———#
cap_string += ("\n🎞  film developed " + src_folder_choice + ", " + str(src_photos.index(src_photo_choice)+1) + " of " + str(len(src_photos)) + " 🎞")

#———CALCULATE DETAIL LOCATION———#
super_detail_str = "  micro" if c_size < (min(w,h)/3.0) else " "
ccx = crop_x + (c_size/2.0) #'center (of) crop, x'
ccy = crop_y + (c_size/2.0) #'center (of) crop, x'

if   ccx < (w/3.0)  :   pos_ind_x = 0
elif ccx < (w/1.5)  :   pos_ind_x = 1
else                :   pos_ind_x = 2

if   ccy < (h/3.0)  :   pos_ind_y = 0
elif ccy < (h/1.5)  :   pos_ind_y = 1
else                :   pos_ind_y = 2

pos_string_matrix = [
    ['top left','top center','top right'],
    ['middle left','middle center','middle right'],
    ['bottom left','bottom center','bottom right']
]
pos_emoji_matrix = [
    ['↖️','⬆️','↗️'],
    ['⬅️','⏺️','➡️'],
    ['↙️','⬇️','↘️']
]

cap_string += ("\n🔍 " + pos_string_matrix[pos_ind_y][pos_ind_x] + " " + pos_emoji_matrix[pos_ind_y][pos_ind_x] + super_detail_str + " detail 🔎")

#———OUTPUT———#

caption_dict = {
    "cap" : cap_string
}

print(caption_dict["cap"])

with open('cron_status.txt', 'a') as f:
    f.write(("run at " + datetime.now().strftime("%H:%M:%S")) + "\n")
    f.close()

with open("to_post/caption.json", "w") as outfile:
    json.dump(caption_dict, outfile)
img = img.resize((2048,2048),Image.NEAREST) #to cover up instagram's upscaling blending
# img.show()
img = img.save("to_post/d_img.png")
