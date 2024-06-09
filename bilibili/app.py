from dotenv import load_dotenv
#导入load_dotenv函数，用于加载.env文件
from flask import Flask, jsonify, request
# 从 flask 模块导入了 Flask 类（用于创建 Flask 应用实例）
# jsonify 函数（用于将 Python 对象转换为 JSON 格式的响应）和 request 对象（用于处理 HTTP 请求）。
# 准备使用flask框架
from errors.errors import InvalidAPIUsage
# 从 errors.errors 模块导入了 InvalidAPIUsage 类，这是一个自定义的异常类，用于处理 API 使用错误
from tools.bilibili_tools.routes import bili_tools
# 从 tools.bilibili_tools.routes 模块导入了 bili_tools，这是一个 Flask 蓝图，用于组织和重用视图函数。
from gevent import pywsgi

app = Flask(__name__)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code

# 这是一个错误处理函数，当抛出 InvalidAPIUsage 异常时，它将被调用。
# 它将异常转换为 JSON 格式的响应，并返回相应的 HTTP 状态码。
@app.before_request
def log_request_info():
    app.logger.debug('Body: %s', request.get_data())

# 这是一个请求处理前的钩子函数，它将请求的数据记录到日志中。
app.register_blueprint(bili_tools, url_prefix='/bilibili/v1')

# 将 bili_tools 蓝图注册到 Flask 应用上，并为其路由添加了 URL 前缀 /bilibili/v1。
if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True)
    
    # server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    # server.serve_forever()
