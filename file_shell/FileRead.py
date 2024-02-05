# 文件路径
file_path = "test.txt"

# 打开文件并读取第一行
with open(file_path, 'r') as file:
    first_line = file.readline()

# 输出第一行内容
print(f"The first line of the file is: {first_line}")
