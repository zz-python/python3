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
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # 表头背景色
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # 表头文本颜色
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 所有单元格内容居中
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # 表头字体
    ('FONTSIZE', (0, 0), (-1, -1), 12),  # 所有单元格字体大小
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # 表头下边距
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # 表格内容背景色
    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # 边框颜色和宽度
])

# 将样式应用到表格
table.setStyle(style)

# 将表格添加到文档中
elements = [table]

# 生成 PDF
doc.build(elements)

print(f"PDF 文件 '{pdf_file}' 已生成！")
