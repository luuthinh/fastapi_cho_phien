# -*- coding:utf-8 -*-

import os 
import tempfile
from PIL import Image

# Cài đặt tempfile
if os.name == "posix":
    tempfile.tempdir = '/home/app/backend/tmp'

# xóa file tạm sau khi trả kết quả
def cleanup(path_file):
    os.remove(path_file)

# sửa kích thước ảnh,trả về path temp 
def resize_image(origin_path, width=0, height=0):
    im = Image.open(origin_path)
    if not width or not height:
        size = im.size
    else:
        size = (width,height)        
    with tempfile.NamedTemporaryFile(mode='w+b', suffix='.' + im.format, 
                                     delete=False) as temp:
        im.resize(size).save(temp)
        return temp.name

def crop_image(image, size = 800):
    width, height = image.size
    radio = width / height
    new_height= size
    new_width = int(800 * radio)
    image = image.resize((new_width,new_height))
    if radio > 1:
        left = (new_width - new_height)/2
        right = left + new_height
        top = 0
        bottom = new_height
    elif radio <= 1:
        left = 0
        right = new_width
        top = (new_height - new_width)/2
        bottom = top + new_width 
    return image.crop((left,top,right,bottom))        
