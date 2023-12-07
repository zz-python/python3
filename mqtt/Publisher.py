import paho.mqtt.client as mqtt

# MQTT Broker 地址和端口
broker_address = "124.220.1.36"
port = 1883

# 创建 MQTT Client 实例
client = mqtt.Client("zzPublisher")

# 连接到 Broker
client.connect(broker_address, port)

# 发布消息
topic = "test/topic"
message = "Hello, MQTT!"
client.publish(topic, message)

# 断开连接
client.disconnect()
