from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.lib import colors

# 创建一个 PDF 文件
pdf_file = "test.pdf"
c = canvas.Canvas(pdf_file, pagesize=A4)
print(f"A4={A4},letter={letter}")
# 创建一个 Drawing 对象，用于绘制图形
drawing = Drawing(500, 200)

# 添加第一行文字
text1 = String(100, 150, "Hello, ReportLab!")
text1.fontName = "Helvetica"
text1.fontSize = 20
text1.fillColor = colors.HexColor("#3498db")
drawing.add(text1)

# 添加第二行文字
text2 = String(100, 120, "This is a drawing with text.")
text2.fontName = "Times-Roman"
text2.fontSize = 14
text2.fillColor = colors.HexColor("#2ecc71")
drawing.add(text2)

drawing.add(text1)

# 创建矩形 (Rect)
# 参数：x, y, width, height, strokeWidth, strokeColor, fillColor
rect = Rect(30, 0, 500, 200,rx=10, ry=10, strokeWidth=1, strokeColor=colors.HexColor("#ecf0f1"), fillColor=None)

# 将矩形添加到绘图对象
drawing.add(rect)

# 数据：每个点表示一个 (x, y) 坐标对
data = [
    (0, 2), (1, 3), (2, 5), (3, 6), (4, 4), (5, 7), (6, 9)
]

# 创建一个折线图对象
line_plot = LinePlot()
line_plot.x = 50  # x 坐标
line_plot.y = 10  # y 坐标
line_plot.width = 400  # 图形宽度
line_plot.height = 150  # 图形高度

# 将数据设置为折线图的数据
line_plot.data = [data]  # 折线图只显示一个数据系列
line_plot.lines[0].strokeColor = colors.blue  # 设置线条颜色为蓝色

# 将折线图添加到 Drawing 对象中
drawing.add(line_plot)

# 使用 c.draw() 将 Drawing 渲染到 PDF 页面上
drawing.drawOn(c, 0, 400)  # 在 (50, 400) 位置绘制图形


# x = 0  # 矩形左上角的 x 坐标
# y = 300  # 矩形左上角的 y 坐标
# width = 500  # 矩形的宽度
# height = 200  # 矩形的高度
# rx = 10  # 圆角的 x 半径
# #ry = 20  # 圆角的 y 半径
# c.setStrokeColor(colors.HexColor("#ecf0f1"))  # 设置边框宽度
# c.roundRect(x, y, width, height, rx, stroke=1, fill=0)

# 保存 PDF 文件
c.save()

print(f"PDF 文件 '{pdf_file}' 已生成！")
