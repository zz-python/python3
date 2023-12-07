import paho.mqtt.client as mqtt
import time

# MQTT Broker 地址和端口
broker_address = "124.220.1.36"
port = 1883

# 回调函数，处理接收到的消息
def on_message(client, userdata, message):
    print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")

# 创建 MQTT Client 实例
client = mqtt.Client("zzSubscriber")

# 设置消息接收回调函数
client.on_message = on_message

# 连接到 Broker
client.connect(broker_address, port)

# 订阅主题
topic = "test/topic"
client.subscribe(topic)

# 开始消息循环
client.loop_start()

# 等待接收消息
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # 中断时断开连接
    client.loop_stop()
    client.disconnect()
