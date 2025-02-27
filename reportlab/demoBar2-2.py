from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def draw_horizontal_bar_chart(pdf_canvas):
    # 数据
    labels = ["0.0.0.10", "0.0.0.8", "0.0.0.7", "::1234", "0.0.0.240"]
    values = [135, 30, 25, 12, 5]  # 数据值，用于决定条形图的长度
    
    # 设置坐标和条形图的基本配置
    x_start = 50
    y_start = 600
    bar_height = 10  # 每个条形图的高度
    bar_spacing = 30  # 条形图之间的垂直间距
    max_value = max(values)  # 获取最大值，用于标准化条形图的长度
    
    # 绘制横向条形图
    for i, value in enumerate(values):
        # 每个条形图的宽度根据值大小调整
        bar_width = 350  # 最大值300代表最大的条形宽度
        pdf_canvas.setFillColor(colors.HexColor('#d5d5d5'))  # 设置条形的颜色
        pdf_canvas.rect(x_start, y_start - (bar_height + bar_spacing) * i, bar_width, bar_height, fill=True, stroke=False)

        # 每个条形图的宽度根据值大小调整
        bar_width = (value / max_value) * 300  # 最大值300代表最大的条形宽度
        pdf_canvas.setFillColor(colors.HexColor('#336FF8'))  # 设置条形的颜色
        pdf_canvas.rect(x_start, y_start - (bar_height + bar_spacing) * i, bar_width, bar_height, fill=True, stroke=False)

        # 添加标签
        pdf_canvas.setFillColor(colors.black)  # 设置文本颜色为黑色
        pdf_canvas.drawString(x_start, y_start - (bar_height + bar_spacing) * i + 15, labels[i])  # 标签的位置

        # 添加数值
        styles = getSampleStyleSheet()
        print(styles['BodyText'])
        # 创建段落对象
        text_style = ParagraphStyle(
                name='TextStyle',
                parent=styles['BodyText']
            )
        paragraph = Paragraph(str(values[i]), text_style)
        paragraph.wrapOn(pdf_canvas, 400, 600)  # wrapOn 用于计算文本的实际尺寸 self.c.stringWidth(text) fontsize=12
        paragraph.drawOn(pdf_canvas, x_start+370, y_start - (bar_height + bar_spacing) * i)  # drawOn 用于将段落绘制到 Canvas 上

    # 绘制标题
    pdf_canvas.drawString(50, y_start + 50, "Top5")

    # 绘制刻度
    # x_end = 350
    # num_ticks = 5  # 刻度数量
    # tick_interval = x_end / num_ticks  # 刻度间隔
    # for i in range(num_ticks + 1):
    #     tick_position = x_start + i * tick_interval
    #     pdf_canvas.line(tick_position, y_start - (bar_height + bar_spacing) * (len(values)), tick_position, y_start - (bar_height + bar_spacing) * (len(values) + 0.3))  # 刻度线
    #     pdf_canvas.drawString(tick_position - 10, y_start - (bar_height + bar_spacing) * (len(values) + 5), str(int(i * (max_value / num_ticks))))  # 刻度值

def create_pdf():
    c = canvas.Canvas("test.pdf", pagesize=letter)
    draw_horizontal_bar_chart(c)  # 绘制横向条形图
    c.save()  # 保存PDF

create_pdf()
