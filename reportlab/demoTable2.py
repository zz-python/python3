from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# 创建PDF文件
def create_table_img(output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)

    # 表格数据
    data = [
        ["#", "Name", "Age", "Gender"],  # 表头
        [1, "John Doe", 28, "Male"],
        [2, "Jane Smith", 34, "Female"],
        [3, "Michael Johnson", 25, "Male"],
        [4, "     Emily Davis", 29, "Female"],
    ]
    # 设置列的固定宽度
    col_widths = [150, 150, 150, 50]  # 为每一列设置固定宽度
    row_heights = [20, 40, 40, 40, 40]  # 每行的高度
    # 创建一个 Table 对象
    table = Table(data, colWidths=col_widths, rowHeights=row_heights)

    style = TableStyle([
        ('COLWIDTH', (0, 0), (-1, -1), 20),
        # colors.grey
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f6f8fa')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        # 屏蔽 Y 轴边框颜色
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#f6f8fa')),
        # 设置行的颜色
        ('LINEABOVE', (0, 0), (-1, -1), 0.1, colors.HexColor('#f6f8fa')),
        ('LINEBELOW', (0, 0), (-1, -1), 0.1, colors.HexColor('#f6f8fa')),
        # 合并 （'SPAN',(第一个方格的左上角坐标)，(第二个方格的左上角坐标))，合并后的值为靠上一行的值，按照长方形合并
        # ('SPAN', (0, 0), (0, 1)),
        # ('width', (0, 0), (-1, -1), 0),
        # 设置边框线条的粗细
        # ('LINEWIDTH', (0, 0), (-1, -1), 1),
        # 自动换行 测试无效
        # ("WORDWRAP", (0, 0), (-1, -1), 1),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ])

    # 设置表格样式
    table.setStyle(style)

    # 设置表格的 x, y 坐标
    table.wrapOn(c, 0, 0)  # 计算表格的宽度和高度
    table.drawOn(c, 50, 300)  # 绘制表格

    # 逐行处理，手动将图片绘制到单元格中
    for i in range(0, len(data)-1):
        print(i, i)
        x = 50 + col_widths[0]  # 水平位置：第一列宽度
        y = 300 + 10 + i * 40 # 垂直位置：根据行高度计算
        width = 40  # 图片宽度
        height = 20  # 图片高度
        c.drawImage("test.png", x, y, width, height)
    # 保存 PDF 文件
    c.save()

# 生成PDF
create_table_img("table_example.pdf")