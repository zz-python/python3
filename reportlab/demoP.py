from reportlab.graphics.shapes import Drawing, Circle
from reportlab.graphics import renderPDF
from reportlab.lib import colors

# 创建一个 Drawing 对象，指定宽度和高度
drawing = Drawing(400, 400)

# 创建多个点
points = [(100, 100), (150, 200), (200, 300), (250, 350)]

for point in points:
    x, y = point
    dot = Circle(x, y, 1)  # 绘制点
    dot.fillColor = colors.red  # 设置点的颜色为红色
    drawing.add(dot)  # 将点添加到 Drawing 对象中

# 保存为 PDF 文件
renderPDF.drawToFile(drawing, "multiple_points_example.pdf")
