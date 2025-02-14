from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.lib import colors

# 创建一个 PDF 文件
pdf_file = "line_chart.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)

# 创建一个 Drawing 对象，用于绘制图形
drawing = Drawing(400, 200)

# 数据：每个点表示一个 (x, y) 坐标对
data = [
    (0, 2), (1, 3), (2, 5), (3, 6), (4, 4), (5, 7), (6, 9)
]

# 创建一个折线图对象
line_plot = LinePlot()
line_plot.x = 50  # x 坐标
line_plot.y = 50  # y 坐标
line_plot.width = 300  # 图形宽度
line_plot.height = 150  # 图形高度

# 将数据设置为折线图的数据
line_plot.data = [data]  # 折线图只显示一个数据系列
line_plot.lines[0].strokeColor = colors.blue  # 设置线条颜色为蓝色

# 将折线图添加到 Drawing 对象中
drawing.add(line_plot)

# 使用 c.draw() 将 Drawing 渲染到 PDF 页面上
drawing.drawOn(c, 50, 400)  # 在 (50, 400) 位置绘制图形

# 保存 PDF 文件
c.save()

print(f"PDF 文件 '{pdf_file}' 已生成！")
