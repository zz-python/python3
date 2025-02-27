from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

def draw_horizontal_bar_chart(c):
    # 注册中文字体（假设字体文件路径为 'SimHei.ttf'）
    pdfmetrics.registerFont(TTFont('SimHei', 'SimHei.ttf'))

    # 设置字体为 SimHei（黑体）
    c.setFont("SimHei", 12)

    # 绘制中文字符串
    c.drawString(100, 750, "你好，世界！")  # X, Y 坐标和要绘制的中文文本

def create_pdf():
    c = canvas.Canvas("test.pdf", pagesize=letter)
    draw_horizontal_bar_chart(c)  # 绘制横向条形图
    c.save()  # 保存PDF

create_pdf()
