from flask import Flask
from flask_cors import CORS
from controllers import (
    student_controller,
    course_controller,
    professor_controller,
    subject_controller,
    offer_controller,
    evaluation_controller,
    grade_student_controller,
    student_evaluation_controller,
    reports_controller
)

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {
        "msg": "SGE - Sistema de Gestão de Estudantes",
        "version": "1.0.0",
        "endpoints": {
            "students": "/api/students",
            "courses": "/api/courses", 
            "professors": "/api/professors",
            "subjects": "/api/subjects",
            "offers": "/api/offers",
            "evaluations": "/api/evaluations",
            "enrollments": "/api/enrollments",
            "student_evaluations": "/api/student-evaluations",
            "reports": "/api/reports"
        }
    }

# Registrar todas as rotas dos controladores
app.register_blueprint(student_controller.bp, url_prefix="/api")
app.register_blueprint(course_controller.bp, url_prefix="/api")
app.register_blueprint(professor_controller.bp, url_prefix="/api")
app.register_blueprint(subject_controller.bp, url_prefix="/api")
app.register_blueprint(offer_controller.bp, url_prefix="/api")
app.register_blueprint(evaluation_controller.bp, url_prefix="/api")
app.register_blueprint(grade_student_controller.bp, url_prefix="/api")
app.register_blueprint(student_evaluation_controller.bp, url_prefix="/api")
app.register_blueprint(reports_controller.bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)