from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.lib import colors
from reportlab.graphics.charts.axes import XValueAxis, YValueAxis
from reportlab.graphics.charts.axes import XCategoryAxis

def draw_line_chart(pdf_canvas):
    # 创建一个 Drawing 对象，用于绘制图形
    drawing = Drawing(200, 200)

    # 数据：每个点表示一个 (x, y) 坐标对
    data = [
        (0, 0), (1, 3), (2, 5), (3, 6), (4, 4), (5, 7), (6, 9)
    ]
    x_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']  # X 轴的文本标签

    # 创建一个折线图对象
    line_plot = LinePlot()
    line_plot.x = 0  # x 坐标
    line_plot.y = 0  # y 坐标
    line_plot.width = 400  # 图形宽度
    line_plot.height = 150  # 图形高度

    # 将数据设置为折线图的数据
    line_plot.data = [data]  # 折线图只显示一个数据系列
    line_plot.lines[0].strokeColor = colors.blue  # 设置线条颜色为蓝色


    # 设置 X 轴和 Y 轴的标签
    line_plot.xValueAxis = XValueAxis()
    line_plot.yValueAxis = YValueAxis()

    def format_date(value):
        return f"time{value}"  # 格式化日期

    line_plot.xValueAxis.labelTextFormat = format_date

    # 设置 Y 轴范围
    line_plot.yValueAxis.valueMin = 0
    line_plot.yValueAxis.valueMax = 20
    line_plot.yValueAxis.valueStep = 5

    # 设置 X 轴的文本标签
    #line_plot.xValueAxis.categoryNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']

    # 修改 X 轴标签的字体颜色
    line_plot.xValueAxis.labels.fontSize = 10
    line_plot.xValueAxis.labels.fillColor = colors.Color(0, 0, 0, alpha=0.5)
    # 修改 Y 轴标签的字体颜色
    line_plot.yValueAxis.labels.fontSize = 10
    line_plot.yValueAxis.labels.fillColor = colors.Color(0, 0, 0, alpha=0.5)

    #line_plot.xValueAxis.visibleLabels = False  # 隐藏 X 轴标签
    #line_plot.yValueAxis.visibleLabels = False  # 隐藏 Y 轴标签
    line_plot.xValueAxis.visibleTicks = False   # 隐藏 X 轴刻度
    line_plot.yValueAxis.visibleTicks = False   # 隐藏 Y 轴刻度
     # 隐藏 X 和 Y 轴的线条，但保留文字
    line_plot.xValueAxis.strokeColor = colors.Color(0, 0, 0, alpha=0.1)  # X 轴的线条
    line_plot.yValueAxis.strokeColor = colors.transparent     # 隐藏 Y 轴的线条

    line_plot.yValueAxis.visibleGrid = True
    line_plot.yValueAxis.gridStrokeColor = colors.Color(0, 0, 0, alpha=0.1)  # 网格线颜色
    line_plot.yValueAxis.gridStrokeWidth = 0.5  # 网格线宽度
    line_plot.yValueAxis.gridStrokeDashArray = [2, 2]  # 网格线样式

    # 将折线图添加到 Drawing 对象中
    drawing.add(line_plot)

    # 使用 c.draw() 将 Drawing 渲染到 PDF 页面上
    drawing.drawOn(pdf_canvas, 50, 400)  # 在 (50, 400) 位置绘制图形

def create_pdf():
    c = canvas.Canvas("line_chart.pdf", pagesize=letter)
    draw_line_chart(c)  # 绘制横向条形图
    c.save()  # 保存PDF
    print(f"PDF 文件已生成！")

create_pdf()

