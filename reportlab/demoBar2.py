from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.lib import colors

# 创建一个 PDF 文件
pdf_file = "horizontal_bar_chart.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)

# 创建一个 Drawing 对象，用于绘制图形
drawing = Drawing(400, 200)

# 创建横向柱状图对象
bar_chart = HorizontalBarChart()
bar_chart.x = 50  # x 坐标
bar_chart.y = 50  # y 坐标
bar_chart.width = 300  # 图形宽度
bar_chart.height = 150  # 图形高度

# 数据：柱状图的每个系列
data = [
    [3, 7, 2, 4, 5],  # 第一个系列的值
    [5, 6, 4, 3, 6],  # 第二个系列的值
]

bar_chart.data = data

# 设置柱状图的类别标签
bar_chart.categoryAxis.categoryNames = ['A', 'B', 'C', 'D', 'E']

# 设置柱状图的样式
bar_chart.barWidth = 15  # 每个柱子的宽度
bar_chart.groupSpacing = 10  # 每组柱子之间的间隔
bar_chart.strokeColor = colors.black  # 边框颜色

# 设置柱子填充颜色
bar_chart.bars[0].fillColor = colors.blue
bar_chart.bars[1].fillColor = colors.red

# 将横向柱状图添加到 Drawing 对象中
drawing.add(bar_chart)

# 使用 c.draw() 将 Drawing 渲染到 PDF 页面上
drawing.drawOn(c, 50, 400)  # 在 (50, 400) 位置绘制图形

# 保存 PDF 文件
c.save()

print(f"PDF 文件 '{pdf_file}' 已生成！")
