import subprocess

# 从master接口获取ip
masterIpArray = ["192.168.1.243", "192.168.1.233", "192.168.1.1"]
masterIpArray = sorted(masterIpArray)
print(f"从master获取设备ip", masterIpArray)

# 文件路径
# file_path = "test.conf"
file_path = "/etc/nginx/smb/smb.conf"
nginxIpArray = []
with open(file_path, 'r') as file:
    for line in file:
        if "location" in line:
            start_index = line.find("/snos_red_") + 1
            end_index = line.find("/", start_index)
            nginxIpArray.append(line[start_index+9:end_index])
nginxIpArray = sorted(nginxIpArray) 
print(f"nginx已配置ip", nginxIpArray)

if ( masterIpArray == nginxIpArray):
    print("masterIpArray,nginxIpArray数组相等")
else:
    with open(file_path, 'w') as file:
        for index, element in enumerate(masterIpArray):
            file.write("location  /snos_red_" + element + "/ {\n")
            file.write("proxy_pass https://" + element + ";\n")
            file.write("}\n")
    print("nginx配置重新写入完成")
    # 执行nginx配置文件检查
    commandT = ["nginx", "-t"]
    resultT = subprocess.run(commandT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if resultT.returncode == 0:
        print("nginx配置检查执行成功")
        # 执行reload
        commandReload = ["nginx", "-s", "reload"]
        resultReload = subprocess.run(commandReload, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if resultReload.returncode == 0:
            print("nginx reload执行成功")
        else:
            print("nginx reload执行失败，错误信息：")
            print(resultReload.stderr)
    else:
        print("nginx配置检查执行失败，错误信息：")
        print(resultT.stderr)    
