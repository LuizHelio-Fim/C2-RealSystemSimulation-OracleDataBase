from flask import Blueprint, request, jsonify
from db.db_conn import get_connection, release_connection

bp = Blueprint('reports', __name__)

@bp.route('/reports/student-enrollment/<int:student_id>', methods=['GET'])
def student_enrollment_report(student_id):
    """Relatório de matrículas de um aluno (grade sem notas)"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Informações do aluno
        cur.execute("""
            SELECT a.NOME, a.MATRICULA, c.NOME as CURSO_NOME
            FROM ALUNO a
            JOIN CURSO c ON a.ID_CURSO = c.ID
            WHERE a.MATRICULA = %s
        """, (student_id,))
        
        student_info = cur.fetchone()
        if not student_info:
            return jsonify({'error': 'Aluno não encontrado'}), 404
        
        # Matrículas do aluno (sem referências a avaliações)
        cur.execute("""
            SELECT m.NOME as MATERIA_NOME, o.ANO, o.SEMESTRE, 
                   ga.STATUS, p.NOME as PROFESSOR_NOME, c.NOME as CURSO_NOME
            FROM GRADE_ALUNO ga
            JOIN OFERTA o ON ga.ID_OFERTA = o.ID
            JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
            JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR
            JOIN CURSO c ON o.ID_CURSO = c.ID
            WHERE ga.ID_ALUNO = %s
            ORDER BY o.ANO DESC, o.SEMESTRE DESC, m.NOME
        """, (student_id,))
        
        enrollments = cur.fetchall()
        
        report = {
            'aluno_nome': student_info[0],
            'matricula': student_info[1],
            'curso_nome': student_info[2],
            'matriculas': []
        }
        
        for enrollment in enrollments:
            report['matriculas'].append({
                'materia_nome': enrollment[0],
                'ano': enrollment[1],
                'semestre': enrollment[2],
                'status': enrollment[3],
                'professor_nome': enrollment[4],
                'curso_nome': enrollment[5]
            })
        
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar relatório: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/reports/professor-workload/<int:professor_id>', methods=['GET'])
def professor_workload(professor_id):
    """Relatório de carga de trabalho de um professor"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Informações do professor
        cur.execute("SELECT NOME, EMAIL, STATUS FROM PROFESSOR WHERE ID_PROFESSOR = %s", (professor_id,))
        professor_info = cur.fetchone()
        if not professor_info:
            return jsonify({'error': 'Professor não encontrado'}), 404
        
        # Ofertas por semestre
        sql_offers = """
            SELECT o.ANO, o.SEMESTRE, m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME,
                   m.CARGA_HORARIA, COUNT(ga.ID_ALUNO) as TOTAL_ALUNOS
            FROM OFERTA o
            JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
            JOIN CURSO c ON o.ID_CURSO = c.ID
            LEFT JOIN GRADE_ALUNO ga ON o.ID = ga.ID_OFERTA
            WHERE o.ID_PROFESSOR = %s
            GROUP BY o.ANO, o.SEMESTRE, m.NOME, c.NOME, m.CARGA_HORARIA, o.ID
            ORDER BY o.ANO DESC, o.SEMESTRE DESC
        """
        cur.execute(sql_offers, (professor_id,))
        
        offers = cur.fetchall()
        
        # Organizar por semestre
        semesters = {}
        total_hours = 0
        total_students = 0
        
        for offer in offers:
            semester_key = f"{offer[0]}-{offer[1]}"
            if semester_key not in semesters:
                semesters[semester_key] = {
                    'ano': offer[0],
                    'semestre': offer[1],
                    'ofertas': [],
                    'carga_horaria_semestre': 0,
                    'total_alunos_semestre': 0
                }
            
            semesters[semester_key]['ofertas'].append({
                'materia_nome': offer[2],
                'curso_nome': offer[3],
                'carga_horaria': offer[4],
                'total_alunos': offer[5]
            })
            
            semesters[semester_key]['carga_horaria_semestre'] += offer[4] or 0
            semesters[semester_key]['total_alunos_semestre'] += offer[5] or 0
            total_hours += offer[4] or 0
            total_students += offer[5] or 0
        
        report = {
            'professor_nome': professor_info[0],
            'professor_email': professor_info[1],
            'professor_status': professor_info[2],
            'carga_horaria_total': total_hours,
            'total_alunos_atendidos': total_students,
            'semestres': list(semesters.values())
        }
        
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar relatório: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/reports/dashboard', methods=['GET'])
def dashboard_summary():
    """Resumo geral do sistema para dashboard"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Contadores gerais
        cur.execute("SELECT COUNT(*) FROM CURSO")
        total_courses = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM ALUNO")
        total_students = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM PROFESSOR")
        total_professors = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM MATERIA")
        total_subjects = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM OFERTA")
        total_offers = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM GRADE_ALUNO")
        total_enrollments = cur.fetchone()[0]
        
        # Últimas atividades (baseado em data de nascimento como proxy)
        cur.execute("""
            SELECT 'Aluno' as TIPO, NOME, TO_CHAR(DATA_NASC, 'YYYY-MM-DD') as DATA
            FROM ALUNO 
            ORDER BY DATA_NASC DESC 
            FETCH FIRST 5 ROWS ONLY
        """)
        recent_students = cur.fetchall()
        
        cur.execute("""
            SELECT 'Professor' as TIPO, NOME, TO_CHAR(DATA_NASC, 'YYYY-MM-DD') as DATA
            FROM PROFESSOR 
            ORDER BY DATA_NASC DESC 
            FETCH FIRST 5 ROWS ONLY
        """)
        recent_professors = cur.fetchall()
        
        recent_activities = list(recent_students) + list(recent_professors)
        recent_activities.sort(key=lambda x: x[2], reverse=True)
        recent_activities = recent_activities[:10]
        
        report = {
            'totais': {
                'cursos': total_courses,
                'alunos': total_students,
                'professores': total_professors,
                'materias': total_subjects,
                'ofertas': total_offers,
                'matriculas': total_enrollments
            },
            'atividades_recentes': [{'tipo': row[0], 'nome': row[1], 'data': row[2]} for row in recent_activities]
        }
        
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar dashboard: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)
