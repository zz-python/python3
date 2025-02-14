from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# 创建一个PDF文件
c = canvas.Canvas("example.pdf", pagesize=letter)

# 设置字体和大小
c.setFont("Helvetica", 12)

# 添加文本
c.drawString(100, 750, "Hello, World!")
c.drawString(100, 730, "This is a PDF generated using ReportLab.")

# 添加一个矩形
c.rect(100, 700, 200, 50)

# 保存PDF
c.save()