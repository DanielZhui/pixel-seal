from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from io import BytesIO
import os
import uuid
import shutil

from .lib import add_watermark

app = FastAPI()

# 设置模板目录
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# 挂载静态文件（例如字体文件）
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# 确保临时目录存在
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload/", response_class=HTMLResponse)
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    text: str = Form(...),
    font_path: str = Form('static/fonts/arial.ttf'),
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

    # 读取上传的文件到 BytesIO 对象
    try:
        contents = await file.read()
        input_image = BytesIO(contents)
    except Exception as e:
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "error": f"读取上传文件时出错: {str(e)}"
        })

    # 生成唯一 ID
    unique_id = str(uuid.uuid4())
    output_filename = f"{unique_id}.jpg"
    output_path = os.path.join(TEMP_DIR, output_filename)

    # 处理水印并保存到临时目录
    try:
        output_image = add_watermark(
            input_image_bytes=input_image,
            watermark_text=text,
            font_path=font_path,
            font_size=font_size,
            color=color_tuple,
            opacity=opacity,
            density=density,
            rotation=rotation,
            margin=margin_tuple
        )
        # 保存到临时目录
        with open(output_path, "wb") as f:
            f.write(output_image.getbuffer())
    except Exception as e:
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "error": f"处理水印时出错: {str(e)}"
        })

    # 跳转到预览页面
    return RedirectResponse(url=f"/preview/{unique_id}", status_code=303)

@app.get("/preview/{image_id}", response_class=HTMLResponse)
async def preview_image(request: Request, image_id: str):
    # 构建图片的URL
    image_url = f"/temp/{image_id}.jpg"
    return templates.TemplateResponse("preview.html", {"request": request, "image_id": image_id, "image_url": image_url})

@app.get("/temp/{image_name}", response_class=StreamingResponse)
async def get_temp_image(image_name: str):
    image_path = os.path.join(TEMP_DIR, image_name)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="图片不存在")

    def iterfile():
        with open(image_path, mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="image/jpeg")

@app.get("/download/{image_id}", response_class=StreamingResponse)
async def download_image(image_id: str):
    image_name = f"{image_id}.jpg"
    image_path = os.path.join(TEMP_DIR, image_name)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="图片不存在")

    def iterfile():
        with open(image_path, mode="rb") as file_like:
            yield from file_like

    # 删除图片后发送
    response = StreamingResponse(iterfile(), media_type="image/jpeg")
    response.headers["Content-Disposition"] = f"attachment; filename=watermarked_{image_id}.jpg"

    # 异步删除文件 (Note: Uvicorn 和 FastAPI 目前不支持异步文件操作很方便，请确保此操作不会影响性能)
    try:
        os.remove(image_path)
    except Exception as e:
        print(f"删除临时文件出错: {str(e)}")

    return response

# 定期清理临时目录（可选）
# 这里建议使用外部工具（如cron作业）或后台任务来定期清理过期的临时文件

if __name__ == "__main__":
    # 确保字体文件存在
    font_file_path = os.path.join(os.path.dirname(__file__), 'static', 'fonts', 'arial.ttf')
    if not os.path.exists(font_file_path):
        print(f"字体文件不存在: {font_file_path}")
        exit(1)

    # 确保临时目录存在
    os.makedirs(TEMP_DIR, exist_ok=True)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")