from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# 创建PDF文件
def create_pdf_with_bar_chart(output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)

    # 表格数据
    data = [
        ["#", "Name", "Age", "Gender"],  # 表头
        [1, "John Doe", 28, "Male"],
        [2, "Jane Smith", 34, "Female"],
        [3, "Michael Johnson", 25, "Male"],
        [4, "Emily Davis", 29, "Female"],
    ]
    # 设置列的固定宽度
    col_widths = [150, 150, 150, 50]  # 为每一列设置固定宽度
    row_heights = [20, 40, 40, 40, 40]  # 每行的高度
    # 创建一个 Table 对象
    table = Table(data, colWidths=col_widths, rowHeights=row_heights)

    # 设置表格样式
    table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # 设置标题行的文字颜色
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),  # 设置标题行的背景颜色
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#f6f8fa')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 设置文字居中对齐
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # 设置标题字体为粗体
        ('FONTSIZE', (0, 0), (-1, -1), 12),  # 设置字体大小
    ]))

    # 设置表格的 x, y 坐标
    table.wrapOn(c, 0, 0)  # 计算表格的宽度和高度
    table.drawOn(c, 50, 300)  # 绘制表格

    # 保存 PDF 文件
    c.save()

# 生成PDF
create_pdf_with_bar_chart("table_example.pdf")