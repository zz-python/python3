from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册支持中文的字体（例如：SimSun）
pdfmetrics.registerFont(TTFont('SimHei', 'SimHei.ttf'))

# 创建绘图对象
drawing = Drawing(400, 200)

# 创建垂直条形图
chart = VerticalBarChart()
chart.width = 350
chart.height = 150
chart.data = [
    (13, 5, 20, 22, 37, 45, 19, 4),
    (5, 20, 46, 38, 23, 21, 6, 14)
]
chart.strokeColor = colors.black

# 设置类别名称（中文）
chart.categoryAxis.categoryNames = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月']

# 设置字体为支持中文的字体
chart.categoryAxis.labels.fontName = 'SimHei'
chart.categoryAxis.labels.fontSize = 12

# 将图表添加到绘图对象中
drawing.add(chart)

# 保存绘图对象为 PDF 文件
from reportlab.graphics import renderPDF
renderPDF.drawToFile(drawing, 'test.pdf', 'Vertical Bar Chart with Chinese')