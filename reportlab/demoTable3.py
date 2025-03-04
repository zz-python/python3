from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


pdfmetrics.registerFont(TTFont('SimHei', 'simhei.ttf')) 

# 获取 ReportLab 默认样式
styles = getSampleStyleSheet()
styleN = styles['Normal']
styleN.fontName = 'SimHei'  # 使用 SimHei 解决中文乱码

def create_pdf(file_name):
    c = canvas.Canvas(file_name, pagesize=A4)
    
    # 1️⃣ 创建表格数据（使用 Paragraph 让文本自动换行）
    data = [
        [Paragraph('序号', styleN), Paragraph('描述', styleN)],
        ['1', Paragraph("这是一个很长的文本，需要自动换行并调整行高的情况。如果文本超出单元格宽度，它应该自动换行，并且表格的行高应该随之调整。111111111111", styleN)],
        ['2', Paragraph("文本示例。", styleN)]
    ]

    # 2️⃣ 计算每行的真实高度
    col_widths = [50, 300]  # 设置列宽
    row_heights = []
    
    for row in data:
        max_height = 0
        for i, cell in enumerate(row):
            if isinstance(cell, Paragraph):
                # 计算该单元格文本的换行后高度
                w, h = cell.wrap(col_widths[i], 0)  # 这里 max_height 设置为 0，自动计算高度
                max_height = max(max_height, h)
                print("max_height:", max_height)
            else:
                max_height = max(max_height, 20)  # 普通字符串的默认高度
        row_heights.append(max_height)

    # 3️⃣ 创建表格，并设置样式
    print("行高:", row_heights)
    table = Table(data, colWidths=col_widths, rowHeights=row_heights)

    table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, -1), 0.1, colors.HexColor('#000000')),# 设置行边框的颜色
        ('LINEBELOW', (0, 0), (-1, -1), 0.1, colors.HexColor('#000000')),# 设置行边框的颜色
        ('LINEBEFORE', (0, 0), (0, -1), 0.1, colors.HexColor('#000000')),  # 设置左边框为红色
        ('LINEAFTER', (-1, 0), (-1, -1), 0.1, colors.HexColor('#000000')),  # 设置右边框为绿色
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f6f8fa')),# 表头背景色
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 文字对齐
        ("LEFTPADDING", (0, 0), (-1, -1), 0),  # 所有单元格的左侧内边距
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),  # 所有单元格的右侧内边距
        ("TOPPADDING", (0, 0), (-1, -1), 0),  # 所有单元格的顶部内边距
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),  # 所有单元格的底部内边距
    ]))

    # 4️⃣ 计算表格的总高度
    table_total_height = sum(row_heights)
    print("表格总高度:", table_total_height)

    # 5️⃣ 将表格绘制到 Canvas
    table.wrapOn(c, 0, 0)  # 计算实际大小
    table.drawOn(c, 50, A4[1] - 100 - table_total_height)  # (x, y) 位置，确保表格能正确显示

    c.save()

# 生成 PDF
create_pdf("test.pdf")
