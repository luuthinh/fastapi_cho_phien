# -*- coding:utf-8 -*-

import os
import io
import base64
import tempfile

from os import getcwd, remove
from PIL import Image
from image_process import cleanup, resize_image, crop_image

from typing import List
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import JSONResponse, Response, StreamingResponse
from starlette.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.post("/source/upload")
async def upload_file(files: List[UploadFile] = File(...), path_file: str = Form(...)):
    asolute_path = os.getcwd() + '/' + path_file
    if not os.path.isdir(asolute_path):
        # Tạo folder chứa file
        try:
            os.mkdir(asolute_path)
        except OSError as error:
            return JSONResponse(content={"error_message": "File not found"}, status_code=404)
    # Duyệt wa các file
    res_url = []
    for file in files:
        if not file.filename:
             return JSONResponse(content={"error_message": "Not file to upload"}, status_code=404)   
        # Kiểm tra đuôi file mở rộng của file upload
        file_name , file_extention = os.path.splitext(file.filename)
        print(file_name, file_extention)
        if file_extention.lower() not in ['.png','.jpg'] :
            return JSONResponse(content={"error_message": "Chỉ có thể tải file có đuôi mở rộng .png hoặc .jpg"}, status_code=404)
        
        im = Image.open(io.BytesIO(await file.read()))
        # Kiểm tra ảnh upload width=height crop

        crop_image(im).save(asolute_path + '/' + file.filename)
        res_url.append({'url': path_file  + '/' + file.filename, 
                        'filename': file.filename})
    return JSONResponse(content={"result": res_url}, status_code=200)

@app.get("/source/download/{file_path:path}")
def download_file(file_path: str):
    return FileResponse(path=getcwd() + "/" + file_path, media_type='application/octet-stream')

@app.get("/source/read/{file_path:path}")
def get_file(file_path:str, background_tasks: BackgroundTasks, width: int = 0, height: int = 0):
    # Kiểm tra thư mục đã tồn tại
    asolute_path = os.getcwd() + '/' + file_path
    if not os.path.isfile(asolute_path):
        return JSONResponse(content={
            "error_message": "File not found"
            }, status_code=404)
    path_temp = resize_image(asolute_path, width, height)
    file_name , file_extention = os.path.splitext(path_temp)  
    background_tasks.add_task(cleanup,path_temp)
    return FileResponse(path_temp, media_type='image/' + file_extention[1:] )

@app.delete("/source/delete/{file_path:path}")
def delete_file(file_path: str):
    try:
        remove(getcwd() + "/" + file_path)
        return JSONRepsponse(content={
            'removed': True,
            }, status_code=200)
    except FileNotFoundError:
        return JSONRepsponse(content={
            "removed": False,
            "error_message": "File not found"
            }, status_code=404)
