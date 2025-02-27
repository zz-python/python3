from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.lib import colors

# 创建一个 PDF 文件
pdf_file = "test.pdf"
c = canvas.Canvas(pdf_file, pagesize=A4)


drawing = Drawing(400, 200)  # 设置画布大小为 400x200

rect = Rect(0, 0, 400, 200,rx=10, ry=10, strokeWidth=1, strokeColor=colors.HexColor("#ecf0f1"), fillColor=None)

# 将矩形添加到绘图对象
drawing.add(rect)

# 定义文字内容和位置
right_aligned_texts = [
    ("Right Aligned Line 11111", 150, colors.HexColor("#3498db")),  # 第一行靠右文字
    ("Right Aligned Line 2", 120, colors.HexColor("#e74c3c")),  # 第二行靠右文字
]

left_aligned_texts = [
    ("Left Aligned Line 11111111", 90, colors.HexColor("#2ecc71")),  # 第一行靠左文字
    ("Left Aligned Line 2", 60, colors.HexColor("#9b59b6")),  # 第二行靠左文字
]

# 添加靠右对齐的文字
x_right = 400  # 靠右对齐的 x 坐标
for text, y, color in right_aligned_texts:
    string = String(
        x_right, y, text,  # 文字位置和内容
        fontName="Helvetica",  # 字体
        fontSize=14,  # 字体大小
        fillColor=color,  # 文字颜色
        textAnchor="end",  # 靠右对齐
    )
    drawing.add(string)

# 添加靠左对齐的文字
x_left = 0  # 靠左对齐的 x 坐标
for text, y, color in left_aligned_texts:
    string = String(
        x_left, y, text,  # 文字位置和内容
        fontName="Helvetica",  # 字体
        fontSize=14,  # 字体大小
        fillColor=color,  # 文字颜色
        textAnchor="start",  # 靠左对齐
    )
    drawing.add(string)
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
