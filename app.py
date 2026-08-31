from flask import Flask
from routes.whatsapp_routes import whatsapp_bp
from routes.call_routes import call_bp

app = Flask(__name__)

app.register_blueprint(whatsapp_bp)
app.register_blueprint(call_bp)


@app.route("/")
def health_check():
    return {"status": "Johnny TEC OS is running"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
  
