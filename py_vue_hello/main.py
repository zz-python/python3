from flask import Flask, render_template
 
 
#app = Flask(__name__)
app = Flask(__name__,
static_folder='./vite-web',  #设置静态文件夹目录
template_folder = "./vite-web",
static_url_path="")  #设置vue编译输出目录dist文件夹，为Flask模板文件目录 
 
@app.route('/')
def index():
    return render_template('index.html')
    
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)








