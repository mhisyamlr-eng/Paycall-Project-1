import os
import json
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

DB_NAME = "counter.db"


# ======================
# Database init
# ======================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS counter (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
    conn.commit()
    conn.close()


def get_count():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM counter")
    count = cursor.fetchone()[0]
    conn.close()
    return count


# ======================
# HTTP Handler
# ======================
class RequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # ======================
    # GET
    # ======================
    def do_GET(self):
        parsed_path = urlparse(self.path)

        # 首页
        if parsed_path.path == "/":
            try:
                with open("index.html", "rb") as f:
                    self._set_headers(200, "text/html")
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self._set_headers(404)
                self.wfile.write(b"index.html not found")

        # 获取计数
        elif parsed_path.path == "/api/count":
            count = get_count()
            self._set_headers()
            self.wfile.write(json.dumps({
                "code": 0,
                "data": count
            }).encode())

        # 获取微信 OpenID
        elif parsed_path.path == "/api/wx_openid":
            wx_source = self.headers.get("x-wx-source")
            wx_openid = self.headers.get("x-wx-openid", "")
            self._set_headers(200, "text/plain")
            if wx_source:
                self.wfile.write(wx_openid.encode())
            else:
                self.wfile.write(b"")

        else:
            self._set_headers(404)
            self.wfile.write(b"Not Found")

    # ======================
    # POST
    # ======================
    def do_POST(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == "/api/count":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode())

            action = data.get("action")

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            if action == "inc":
                cursor.execute("INSERT INTO counter DEFAULT VALUES")
            elif action == "clear":
                cursor.execute("DELETE FROM counter")

            conn.commit()
            conn.close()

            count = get_count()
            self._set_headers()
            self.wfile.write(json.dumps({
                "code": 0,
                "data": count
            }).encode())

        else:
            self._set_headers(404)
            self.wfile.write(b"Not Found")


# ======================
# Run Server
# ======================
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 80))
    server = HTTPServer(("0.0.0.0", port), RequestHandler)
    print(f"Server running on port {port}")
    server.serve_forever()
