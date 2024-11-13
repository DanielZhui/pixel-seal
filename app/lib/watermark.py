from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
from io import BytesIO

def add_watermark(
    input_image_bytes: BytesIO,
    watermark_text: str,
    font_path: str = 'static/fonts/arial.ttf',  # 默认字体路径，请根据需要更改
    font_size: int = 36,
    color: tuple = (255, 255, 255),
    opacity: int = 128,  # 透明度范围 0-255
    density: int = 5,  # 每行和每列的水印数量
    rotation: int = 45,  # 水印旋转角度
    margin: tuple = (10, 10)  # x 和 y 方向的边距
) -> BytesIO:
    # 打开原始图片
    original = Image.open(input_image_bytes).convert("RGBA")

    # 处理EXIF方向
    original = ImageOps.exif_transpose(original)

    width, height = original.size

    # 创建一个新的透明图层用于绘制水印
    txt_layer = Image.new('RGBA', original.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # 确定字体路径的绝对路径
    font_abspath = os.path.join(os.path.dirname(os.path.dirname(__file__)), font_path)

    try:
        font = ImageFont.truetype(font_abspath, font_size)
    except IOError:
        print(f"无法加载字体文件：{font_abspath}，使用默认字体。")
        font = ImageFont.load_default()

    text_width, text_height = draw.textsize(watermark_text, font=font)

    # 计算每个水印的间隔
    x_spacing = (width - 2 * margin[0]) / density
    y_spacing = (height - 2 * margin[1]) / density

    for i in range(density):
        x = int(margin[0] + i * x_spacing)
        for j in range(density):
            y = int(margin[1] + j * y_spacing)

            # 创建单独的水印图层以便旋转
            watermark = Image.new('RGBA', (text_width, text_height), (255, 255, 255, 0))
            watermark_draw = ImageDraw.Draw(watermark)
            watermark_draw.text((0, 0), watermark_text, font=font, fill=color + (opacity,))
            rotated_watermark = watermark.rotate(rotation, expand=1)

            # 计算新的位置，以使旋转后的水印居中于当前点
            rw, rh = rotated_watermark.size
            x_position = x - rw // 2
            y_position = y - rh // 2

            # 确保水印不超出图片范围
            if x_position + rw > width:
                x_position = width - rw
            if y_position + rh > height:
                y_position = height - rh
            if x_position < 0:
                x_position = 0
            if y_position < 0:
                y_position = 0

            # 合并旋转后的水印到主图层
            txt_layer.paste(rotated_watermark, (x_position, y_position), rotated_watermark)
    # 合并原始图片和水印
    combined = Image.alpha_composite(original, txt_layer)

    # 保存结果到 BytesIO 对象
    output_buffer = BytesIO()
    combined = combined.convert("RGB")  # 如果不需要透明背景
    combined.save(output_buffer, format="JPEG")
    output_buffer.seek(0)

    return output_buffer