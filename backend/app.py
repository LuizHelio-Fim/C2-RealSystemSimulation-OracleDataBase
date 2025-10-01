from flask import Flask
from flask_cors import CORS
from controllers import student_controller

app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem (para desenvolvimento)

@app.route("/")
def home():
    return {"msg": "SGE - Sistema de Gestão de Estudantes"}

# Registrar rotas
app.register_blueprint(student_controller.bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)