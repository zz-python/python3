from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.graphics.charts.axes import XValueAxis, YValueAxis
from datetime import datetime

def draw_line_chart(pdf_canvas):
    # 创建一个 Drawing 对象，用于绘制图形
    drawing = Drawing(400, 200)

    # 创建一个 LinePlot 对象
    plot = LinePlot()

    # 示例日期数据
    dates = [datetime(2023, 10, 1), datetime(2023, 10, 2), datetime(2023, 10, 3), datetime(2023, 10, 4), datetime(2023, 10, 5)]
    values = [10, 20, 15, 25, 30]

    # 将日期转换为时间戳（数值）
    x_values = [date.timestamp() for date in dates]

    # 设置图表的数据
    plot.data = [list(zip(x_values, values))]
    print(plot.data)

    # 设置 X 轴和 Y 轴的范围
    plot.x = 50  # X 轴起始位置
    plot.y = 50  # Y 轴起始位置
    plot.height = 125  # 图表高度
    plot.width = 300   # 图表宽度


    # 自定义 X 轴标签格式：将时间戳转换为日期字符串
    def format_date(value):
        date = datetime.fromtimestamp(value)
        return date.strftime('%Y-%m-%d')  # 格式化日期

    # 设置 X 轴为数值轴，并自定义标签格式
    plot.xValueAxis = XValueAxis()

    plot.xValueAxis.labelTextFormat = format_date

    # 设置 X 轴标签的字体样式
    plot.xValueAxis.labels.fontName = 'Helvetica'
    plot.xValueAxis.labels.fontSize = 8
    plot.xValueAxis.labels.fillColor = Color(0, 0, 0)  # 黑色

    # 将图表添加到绘图对象中
    drawing.add(plot)

    # 使用 c.draw() 将 Drawing 渲染到 PDF 页面上
    drawing.drawOn(pdf_canvas, 50, 400)  # 在 (50, 400) 位置绘制图形

def create_pdf():
    c = canvas.Canvas("line_chart.pdf", pagesize=letter)
    draw_line_chart(c)  # 绘制横向条形图
    c.save()  # 保存PDF
    print(f"PDF 文件已生成！")

create_pdf()

