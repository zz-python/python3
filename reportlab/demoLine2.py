from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Polygon
from reportlab.pdfgen import canvas

pdf_file = "line_chart.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)

# 创建一个 Drawing 对象，指定宽度和高度
drawing = Drawing(400, 200)

# 定义多边形的顶点坐标，注意这里是一个扁平的列表
polygon_points = [0, 0, 250, 0, 250, 250, 150, 150, 50, 150, 0, 100]

gradient_fill = colors.Color(0, 0, 1)  # Blue

# 创建多边形对象，使用关键字参数 points 传递顶点
polygon = Polygon(
    points=polygon_points,  # 使用扁平化的坐标列表
    fillColor=gradient_fill,  # 填充颜色
    strokeColor=colors.transparent,  # 边框颜色
    strokeWidth=0,  # 边框宽度为2
)

# 将多边形添加到 Drawing 对象中
drawing.add(polygon)

# 使用 c.draw() 将 Drawing 渲染到 PDF 页面上
drawing.drawOn(c, 50, 400)  # 在 (50, 400) 位置绘制图形

# 保存 PDF 文件
c.save()
