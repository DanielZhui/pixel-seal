from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from io import BytesIO
from PIL import Image
import os
import shutil

from .lib import add_watermark

app = FastAPI()
base_dir = os.path.dirname(os.path.abspath(__file__))
base_font_path = os.path.join(base_dir, "static/fonts/", "Amatic-Bold.ttf")

# 设置模板目录
templates = Jinja2Templates(directory="app/templates")

# 挂载静态文件（例如字体文件）
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload/")
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    text: str = Form(...),
    font_path: str = Form(base_font_path),
    font_size: int = Form(36),
    color: str = Form('255,255,255'),
    opacity: int = Form(128),
    density: int = Form(5),
    rotation: int = Form(45),
    margin: str = Form('10,10')
):
    # 解析颜色
    try:
        color_tuple = tuple(map(int, color.split(',')))
        if len(color_tuple) != 3:
            raise ValueError
    except ValueError:
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "error": "颜色格式错误，应为 R,G,B"
        })

    # 解析边距
    try:
        margin_tuple = tuple(map(int, margin.split(',')))
        if len(margin_tuple) != 2:
            raise ValueError
    except ValueError:
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "error": "边距格式错误，应为 x,y"
        })

    # 保存上传的文件到临时目录
    temp_input_path = f"app/temp/input_{file.filename}"
    with open(temp_input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 定义输出文件路径
    temp_output_path = os.path.join(base_dir, f"temp/output_{file.filename}")
    input_font_path = os.path.join(base_dir, "static/fonts/", font_path)

    # 处理水印
    try:
        add_watermark(
            input_image_path=temp_input_path,
            output_image_path=temp_output_path,
            watermark_text=text,
            font_path=input_font_path,
            font_size=font_size,
            color=color_tuple,
            opacity=opacity,
            density=density,
            rotation=rotation,
            margin=margin_tuple
        )
    except Exception as e:
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "error": f"处理水印时出错: {str(e)}"
        })

    # 读取处理后的图片并准备返回
    def iterfile():
        with open(temp_output_path, mode="rb") as file_like:
            yield from file_like

    def file_generator():
        try:
            with open(temp_output_path, mode="rb") as file:
                yield from file
        finally:
            try:
                os.unlink(temp_output_path)  # 删除文件
                os.unlink(temp_input_path)
            except Exception as e:
                print(f"Error while deleting file: {e}")

    # 清理临时文件
    # os.remove(temp_input_path)
    # os.remove(temp_output_path)

    # return StreamingResponse(file_generator(), media_type="image/jpeg", headers={
    #     "Content-Disposition": f"attachment; filename=watermarked_{file.filename}"
    # })

    return FileResponse(temp_output_path, media_type="image/jpeg", filename=f'watermarked_{file.filename}')

if __name__ == "__main__":
    temp_dir = os.path.join(base_dir, "temp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    uvicorn.run(app, host="0.0.0.0", port=8000)