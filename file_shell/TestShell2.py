import subprocess

# 要执行的Shell指令，使用参数列表
command = ["nginx", "-s", "reload"]

# 使用subprocess模块执行Shell指令
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# 输出结果
if result.returncode == 0:
    print("执行成功，输出结果：")
    print(result.stdout)
else:
    print("执行失败，错误信息：")
    print(result.stderr)