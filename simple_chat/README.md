# 安全云demo数据

## 创建虚拟环境
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 安装
```
pip install redis
pip install flask
```

## 调试
```
python .\main.py
```


## 打包
```
pip install pyinstaller
pyinstaller --add-data "templates;templates" --add-data "static;static" --onefile --name demo数据 main.py
```
