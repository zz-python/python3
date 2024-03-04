import subprocess
import chardet

# 启动子进程
process = subprocess.Popen("nginx -t", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# 等待子进程执行完毕并获取返回码
#return_code = process.wait()

# 判断返回码是否为非零值，表示执行失败
#if return_code != 0:
    #print("执行失败")
    #print(process.stdout)
#else:
    #print("执行成功")
    #print(process.stdout)
out = process.stdout
content = out.read()
if content:
    encoder = chardet.detect(content)
    encoding = encoder.get("encoding", "utf-8")
    outStr = content.decode(encoding, "ignore")
    print(f'---run shell retrun:{outStr}')
    if 'No such file or directory' in outStr or 'Invalid argument(s):' in outStr or 'error:' in outStr or '不是内部或外部命令，也不是可运行的程序' in outStr:
        outStr = ''
out.close()
if outStr.find("successful") != -1:
    print(f'执行成功zzzzz')