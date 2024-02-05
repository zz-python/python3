# 文件路径
file_path = "test.conf"

# 要写入文件的文本内容
text_content = "location ~ /snos_red_([\d\.]+)/ {\n"

# 打开文件并写入内容
with open(file_path, 'w') as file:
    file.write(text_content)
    file.write("set $target_ip $1;\n")
    file.write("proxy_pass https://$target_ip;\n")
    file.write("}")

print(f"文件 '{file_path}' 已成功创建并写入文本.")