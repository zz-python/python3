from zapv2 import ZAPv2

# 连接到 OWASP Zap 的 API
zap = ZAPv2()

# 打印 OWASP Zap 版本信息
print("ZAP Version: " + zap.core.version)

# 获取目标网站的 URL
target_url = "https://dev.secloud.ruijie.com.cn/cloud"

# 扫描目标网站
print("Scanning target: " + target_url)
scan_id = zap.spider.scan(target_url)

# 等待扫描完成
while int(zap.spider.status(scan_id)) < 100:
    print("Spider progress: " + zap.spider.status(scan_id) + "%")
    time.sleep(2)

print("Spider completed")

# 获取扫描结果
alerts = zap.core.alerts()
print("Alerts found:")
for alert in alerts:
    print(alert)
