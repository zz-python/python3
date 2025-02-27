from datetime import datetime
import pytz

# 获取当前时区
timezone = pytz.timezone('Asia/Shanghai')  # 设置为上海时区
current_time = datetime.now(timezone)  # 获取当前时区的时间

print("当前时间：", current_time)