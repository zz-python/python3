from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# 创建 PDF 文件
pdf_file = "example_with_paragraph.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=letter)

# 创建一个样式对象
styles = getSampleStyleSheet()

# 创建一个段落对象
text = "This is a paragraph that will be kept with the next element on the same page."
paragraph = Paragraph(text, styles['Normal'])

text2 = "zzzzzzzzzzzzzzzzzzzz."
paragraph2 = Paragraph(text2, styles['Normal'])

# 创建一个表格数据
data = [
    ["#", "Name", "Age", "Gender"],
    [1, "John Doe", 28, "Male"],
    [2, "Jane Smith", 34, "Female"],
    [3, "Michael Johnson", 25, "Male"],
]

# 创建一个表格
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

# 设置段落的 `getKeepWithNext` 属性
paragraph.keepWithNext = True  # 保证段落和下一个对象（如表格）在同一页显示

# 页面的元素
elements = [paragraph, table, PageBreak(), paragraph2]

# 生成 PDF
doc.build(elements)

print(f"PDF 文件 '{pdf_file}' 已生成！")
