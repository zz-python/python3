from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse
import asyncio
import json
import random
from datetime import datetime
from typing import AsyncGenerator

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    """返回HTML测试页面"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SSE 测试页面</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            #messages { 
                border: 1px solid #ccc; 
                padding: 10px; 
                max-height: 400px; 
                overflow-y: auto;
                background: #f5f5f5;
            }
            .msg { 
                padding: 8px; 
                margin: 5px 0; 
                border-radius: 4px;
                background: white;
                border-left: 3px solid #007bff;
            }
            .timestamp { color: #666; font-size: 12px; }
            .connected { color: green; font-weight: bold; }
            .disconnected { color: red; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>🚀 SSE 实时消息演示</h1>
        <div>
            <span id="status" class="disconnected">● 未连接</span>
            <button onclick="connect()">连接</button>
            <button onclick="disconnect()">断开</button>
        </div>
        <div id="messages"></div>
        
        <script>
            let eventSource = null;
            let messageCount = 0;
            
            function connect() {
                if (eventSource) {
                    eventSource.close();
                }
                
                // 建立SSE连接
                eventSource = new EventSource('/sse');
                
                // 连接成功
                eventSource.onopen = function() {
                    document.getElementById('status').className = 'connected';
                    document.getElementById('status').textContent = '● 已连接';
                    addMessage('系统', '连接成功', 'info');
                };
                
                // 接收消息
                eventSource.onmessage = function(event) {
                    messageCount++;
                    const data = JSON.parse(event.data);
                    addMessage('服务器', data.message, 'info');
                };
                
                // 监听特定事件类型
                eventSource.addEventListener('update', function(event) {
                    const data = JSON.parse(event.data);
                    addMessage('更新', data.content, 'update');
                });
                
                eventSource.addEventListener('notification', function(event) {
                    const data = JSON.parse(event.data);
                    addMessage('通知', data.content, 'notification');
                });
                
                eventSource.addEventListener('heartbeat', function(event) {
                    const data = JSON.parse(event.data);
                    document.getElementById('status').textContent = '● 已连接 (心跳: ' + data.timestamp + ')';
                });
                
                // 错误处理
                eventSource.onerror = function(error) {
                    document.getElementById('status').className = 'disconnected';
                    document.getElementById('status').textContent = '● 连接错误';
                    console.error('SSE错误:', error);
                    // 自动重连
                    setTimeout(connect, 3000);
                };
            }
            
            function disconnect() {
                if (eventSource) {
                    eventSource.close();
                    eventSource = null;
                    document.getElementById('status').className = 'disconnected';
                    document.getElementById('status').textContent = '● 已断开';
                    addMessage('系统', '连接已断开', 'info');
                }
            }
            
            function addMessage(type, content, className = 'info') {
                const div = document.getElementById('messages');
                const msg = document.createElement('div');
                msg.className = 'msg';
                const time = new Date().toLocaleTimeString();
                msg.innerHTML = `
                    <strong>${type}</strong> 
                    <span class="timestamp">[${time}]</span>
                    <br>${content}
                `;
                div.appendChild(msg);
                div.scrollTop = div.scrollHeight;
            }
            
            // 页面加载时自动连接
            window.onload = connect;
        </script>
    </body>
    </html>
    """

async def sse_generator() -> AsyncGenerator[str, None]:
    """SSE事件生成器"""
    count = 0
    while True:
        count += 1
        
        # 生成不同类型的消息
        if count % 3 == 0:
            # 普通消息
            message = {
                "message": f"这是第 {count} 条消息",
                "timestamp": datetime.now().isoformat()
            }
            yield f"data: {json.dumps(message)}\n\n"
        
        elif count % 3 == 1:
            # 更新事件
            update_data = {
                "content": f"数据已更新 (版本 {count})",
                "timestamp": datetime.now().isoformat()
            }
            yield f"event: update\n"
            yield f"data: {json.dumps(update_data)}\n\n"
        
        else:
            # 通知事件
            notification_data = {
                "content": f"您有 {random.randint(1, 10)} 条新通知",
                "timestamp": datetime.now().isoformat()
            }
            yield f"event: notification\n"
            yield f"data: {json.dumps(notification_data)}\n\n"
        
        await asyncio.sleep(2)  # 每2秒发送一次

@app.get("/sse")
async def sse_endpoint(request: Request):
    """SSE端点"""
    return StreamingResponse(
        sse_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 禁用缓冲
            "Access-Control-Allow-Origin": "*"  # 允许跨域
        }
    )

# 如果需要，添加一个简单的后台任务示例
@app.get("/send-message")
async def send_custom_message(message: str = "Hello, SSE!"):
    """发送自定义消息（仅作演示）"""
    return {"message": "消息已发送（实际应通过队列发送）"}

# uvicorn sse_demo:app --reload --host 0.0.0.0 --port 8000