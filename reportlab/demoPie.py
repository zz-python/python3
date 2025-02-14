from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib import colors  # 导入颜色模块

# 创建PDF文件
def create_pdf_with_pie_chart(output_pdf):
    # 创建一个Canvas对象
    c = canvas.Canvas(output_pdf, pagesize=letter)

    # 添加标题
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Pie Chart Example")

    # 创建一个Drawing对象
    d = Drawing(400, 200)

    # 创建饼图
    pie = Pie()
    pie.x = 100  # 饼图的x坐标
    pie.y = -150   # 饼图的y坐标
    pie.width = 300  # 饼图的宽度
    pie.height = 300  # 饼图的高度

    # 设置饼图的数据
    pie.data = [10, 20, 30, 40]  # 数据值
    pie.labels = ['A', 'B', 'C', 'D']  # 标签

    # 设置饼图的颜色
    pie.slices.strokeWidth = 1  # 边框宽度
    pie.slices[0].fillColor = colors.red  # 第一块颜色
    pie.slices[1].fillColor = colors.green  # 第二块颜色
    pie.slices[2].fillColor = colors.blue  # 第三块颜色
    pie.slices[3].fillColor = colors.yellow  # 第四块颜色

    # 将饼图添加到Drawing对象中
    d.add(pie)

    # 将Drawing对象渲染到Canvas上
    d.drawOn(c, 0, 400)

    # 保存PDF
    c.save()

# 生成PDF
create_pdf_with_pie_chart("pie_chart_example.pdf")