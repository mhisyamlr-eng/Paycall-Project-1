import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from db import init_db, Counter, db

app = Flask(__name__)
CORS(app)

# ======================
# 首页 (Home)
# ======================
@app.route("/", methods=["GET"])
def home():
    return send_from_directory(".", "index.html")


# ======================
# 更新计数
# ======================
@app.route("/api/count", methods=["POST"])
def update_count():
    data = request.get_json()
    action = data.get("action")

    if action == "inc":
        counter = Counter()
        db.session.add(counter)
        db.session.commit()

    elif action == "clear":
        db.session.query(Counter).delete()
        db.session.commit()

    count = Counter.query.count()

    return jsonify({
        "code": 0,
        "data": count
    })


# ======================
# 获取计数
# ======================
@app.route("/api/count", methods=["GET"])
def get_count():
    count = Counter.query.count()
    return jsonify({
        "code": 0,
        "data": count
    })


# ======================
# 小程序获取微信 OpenID
# ======================
@app.route("/api/wx_openid", methods=["GET"])
def get_wx_openid():
    if request.headers.get("x-wx-source"):
        return request.headers.get("x-wx-openid", "")
    return ""


# ======================
# 启动服务
# ======================
if __name__ == "__main__":
    init_db(app)
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)
