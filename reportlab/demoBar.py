from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib import colors

# 创建PDF文件
def create_pdf_with_bar_chart(output_pdf):
    # 创建一个Canvas对象
    c = canvas.Canvas(output_pdf, pagesize=letter)

    # 添加标题
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Bar Chart Example")

    # 创建一个Drawing对象
    d = Drawing(400, 200)

    # 创建柱状图
    bar_chart = VerticalBarChart()
    bar_chart.x = 50  # 柱状图的x坐标
    bar_chart.y = 50  # 柱状图的y坐标
    bar_chart.width = 300  # 柱状图的宽度
    bar_chart.height = 200  # 柱状图的高度

    # 设置柱状图的数据
    data = [
        [10, 20, 30, 40],  # 第一组数据
        [15, 25, 35, 45],  # 第二组数据
    ]
    bar_chart.data = data

    # 设置柱状图的类别标签
    bar_chart.categoryAxis.categoryNames = ['A', 'B', 'C', 'D']

    # 设置柱状图的样式
    bar_chart.valueAxis.valueMin = 0  # 最小值
    bar_chart.valueAxis.valueMax = 50  # 最大值
    bar_chart.valueAxis.valueStep = 10  # 刻度间隔
    bar_chart.barSpacing = 5  # 柱子之间的间距

    # 设置柱状图的颜色
    bar_chart.bars[0].fillColor = colors.blue  # 第一组柱子的颜色
    bar_chart.bars[1].fillColor = colors.green  # 第二组柱子的颜色

    # 将柱状图添加到Drawing对象中
    d.add(bar_chart)

    # 将Drawing对象渲染到Canvas上
    d.drawOn(c, 50, 400)

    # 保存PDF
    c.save()

# 生成PDF
create_pdf_with_bar_chart("bar_chart_example.pdf")