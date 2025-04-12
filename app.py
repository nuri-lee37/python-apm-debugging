from flask import Flask
import psycopg2
from mako.template import Template
from jinja2 import Template as JinjaTemplate
from gevent import monkey
from gevent.pywsgi import WSGIServer

# Datadog tracing
monkey.patch_all()  # 반드시 ddtrace 전에 호출
from ddtrace import patch_all, tracer
patch_all()

app = Flask(__name__)

@app.route("/")
def hello():
    # Mako, Jinja2 템플릿 렌더링
    t1 = Template("Hello ${name}!")
    t2 = JinjaTemplate("Hello {{ name }}!")
    output1 = t1.render(name="Mako")
    output2 = t2.render(name="Jinja2")

    # PostgreSQL 연결 시도 (실제 쿼리 안 함)
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        conn.close()
        db_status = "DB connection successful"
    except Exception as e:
        db_status = f"DB connection failed: {str(e)}"
    finally:
        if conn:
            conn.close()

    return f"Hello, Datadog APM with Python 3.7.8! [{output1}, {output2}] | {db_status}"

if __name__ == "__main__":
    print("App starting...") 
    http_server = WSGIServer(("0.0.0.0", 8080), app)
    http_server.serve_forever()
