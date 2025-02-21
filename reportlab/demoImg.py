from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib import colors

# 创建PDF文件
def create_pdf_with_bar_chart(output_pdf):
    # 创建一个Canvas对象
    c = canvas.Canvas(output_pdf, pagesize=letter)

    # 读取并绘制图像
    image_path = "test.png"  # 图片路径
    x, y = 100, 500  # 图像位置 (x, y)
    width, height = 40, 30  # 图像的宽度和高度

    # 使用 drawImage 方法绘制图片
    c.drawImage(image_path, x, y, width, height)

    # 保存PDF
    c.save()

# 生成PDF
create_pdf_with_bar_chart("img_example.pdf")