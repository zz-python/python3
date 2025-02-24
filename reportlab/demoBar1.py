from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib import colors

# 创建PDF文件
def create_pdf_with_bar_chart(output_pdf):
    # 创建一个Canvas对象
    c = canvas.Canvas(output_pdf, pagesize=letter)

    # 创建一个Drawing对象
    d = Drawing(400, 200)

    # 创建柱状图
    bar_chart = VerticalBarChart()
    bar_chart.x = 0  # 柱状图的x坐标
    bar_chart.y = 50  # 柱状图的y坐标
    bar_chart.width = 300  # 柱状图的宽度
    bar_chart.height = 300

    # 设置柱状图的数据
    data = [
        [10, 20, 30, 40],  # 第一组数据
    ]
    bar_chart.data = data

    # 设置柱状图的类别标签
    bar_chart.categoryAxis.categoryNames = ['AAA', 'BBBB', 'CCC', 'DDD']

    # 设置柱状图的样式
    bar_chart.valueAxis.valueMin = 0  # 最小值
    bar_chart.valueAxis.valueMax = 50  # 最大值
    bar_chart.valueAxis.valueStep = 10  # 刻度间隔
    bar_chart.barSpacing = 5  # 柱子之间的间距
    bar_chart.barWidth = 1  # 柱子的宽度

    # 设置柱状图的颜色
    bar_chart.bars[0].fillColor = colors.blue  # 第一组柱子的颜色

    # 设置柱体的边框颜色
    bar_chart.bars[0].strokeColor = colors.transparent  # 设置柱体的边框颜色为黑色


    # 隐藏 X 和 Y 轴的线条，但保留文字
    bar_chart.categoryAxis.visibleTicks = False   # 隐藏 X 轴刻度
    bar_chart.categoryAxis.strokeColor = colors.HexColor('#D5D5D5')  # 隐藏 X 轴的线条
    bar_chart.valueAxis.strokeColor = colors.transparent     # 隐藏 Y 轴的线条

    # 修改 X 轴字体颜色
    #bar_chart.categoryAxis.labels.fontName = 'Helvetica'  # 字体
    bar_chart.categoryAxis.labels.fontSize = 10           # 字体大小
    bar_chart.categoryAxis.labels.fillColor = colors.Color(0, 0, 0, alpha=0.5)  # 字体颜色

    # 修改 Y 轴字体颜色
    #bar_chart.valueAxis.labels.fontName = 'Helvetica'  # 字体
    bar_chart.valueAxis.labels.fontSize = 10          # 字体大小
    bar_chart.valueAxis.labels.fillColor = colors.Color(0, 0, 0, alpha=0.5)  # 字体颜色

    # 隐藏 X 和 Y 轴
    # bar_chart.categoryAxis.visible = False  # 隐藏 X 轴
    # bar_chart.valueAxis.visible = False     # 隐藏 Y 轴

    # 添加 Y 轴背景网格线
    bar_chart.valueAxis.visibleGrid = True
    bar_chart.valueAxis.gridStrokeColor = colors.Color(0, 0, 0, alpha=0.1)  # 网格线颜色
    bar_chart.valueAxis.gridStrokeWidth = 0.5  # 网格线宽度
    bar_chart.valueAxis.gridStrokeDashArray = [2, 2]  # 网格线样式
    # 将柱状图添加到Drawing对象中
    d.add(bar_chart)

    # 将Drawing对象渲染到Canvas上
    d.drawOn(c, 50, 400)

    # 保存PDF
    c.save()

# 生成PDF
create_pdf_with_bar_chart("bar_chart_example.pdf")