from flask import Flask, request, jsonify, render_template  # 新增render_template导入
from flask import Flask, request, jsonify
from sparkai.llm.llm import ChatSparkLLM
from sparkai.core.messages import ChatMessage

app = Flask(__name__)

# 配置你的专属 API 信息（替换为截图中的实际值）
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'  # 与你的 Spark Max 版本匹配
SPARKAI_APP_ID = 'd62b5131'  # 你的 APPID
SPARKAI_API_SECRET = 'OGU2NzE3NTA1MzdkZmNkOTY0Nzg1NWFk'  # 你的 APISecret
SPARKAI_API_KEY = '7fda40fb0172b0a4df1c81a85ed782b6'  # 你的 APIKey
SPARKAI_DOMAIN = 'generalv3.5'  # Spark Max 对应的 domain

# 初始化星火模型客户端
spark = ChatSparkLLM(
    spark_api_url=SPARKAI_URL,
    spark_app_id=SPARKAI_APP_ID,
    spark_api_key=SPARKAI_API_KEY,
    spark_api_secret=SPARKAI_API_SECRET,
    spark_llm_domain=SPARKAI_DOMAIN,
    streaming=False  # 非流式调用（如需实时返回，设为 True）
)
@app.route('/')
def index():
    return render_template('index.html')  # 假设前端页面是index.html
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': '请输入消息'}), 400
    
    # 构造请求消息
    messages = [ChatMessage(role="user", content=user_input)]
    # 调用模型
    response = spark.generate([messages])
    # 提取回复内容（根据返回格式调整，具体看 SDK 文档）
    answer = response.generations[0][0].text
    return jsonify({'reply': answer})

if __name__ == '__main__':
    app.run(debug=True)