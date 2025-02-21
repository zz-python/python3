from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# 创建一个 PDF 文件
pdf_file = "table_example.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=letter)

# 表格数据
data = [
    ["#", "Name", "Age", "Gender"],  # 表头
    [1, "John Doe", 28, "Male"],
    [2, "Jane Smith", 34, "Female"],
    [3, "Michael Johnson", 25, "Male"],
    [4, "Emily Davis", 29, "Female"],
]

# 创建一个 Table 对象
table = Table(data)

# 自定义表格样式
# style = TableStyle([
#     ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # 表头背景色
#     ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # 表头文本颜色
#     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 所有单元格内容居中
#     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # 表头字体
#     ('FONTSIZE', (0, 0), (-1, -1), 12),  # 所有单元格字体大小
#     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # 表头下边距
#     ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # 表格内容背景色
#     ('GRID', (0, 0), (-1, -1), 1, colors.black),  # 边框颜色和宽度
# ])
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

# 将样式应用到表格
table.setStyle(style)

# 将表格添加到文档中
elements = [table]

# 生成 PDF
doc.build(elements)

print(f"PDF 文件 '{pdf_file}' 已生成！")
