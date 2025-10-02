from flask import Blueprint, request, jsonify
from db.db_conn import get_connection, release_connection

bp = Blueprint('reports', __name__)

@bp.route('/reports/student-grades/<int:student_id>', methods=['GET'])
def student_grade_report(student_id):
    """Relatório de notas de um aluno específico"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT a.NOME as ALUNO_NOME, c.NOME as CURSO_NOME, 
               m.NOME as MATERIA_NOME, o.ANO, o.SEMESTRE,
               av.TIPO as AVALIACAO_TIPO, av.PESO, aa.NOTA,
               ga.STATUS, ga.MEDIA_FINAL, m.MEDIA_APROVACAO
        FROM ALUNO a
        JOIN CURSO c ON a.ID_CURSO = c.ID
        LEFT JOIN GRADE_ALUNO ga ON a.MATRICULA = ga.ID_ALUNO
        LEFT JOIN OFERTA o ON ga.ID_OFERTA = o.ID
        LEFT JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
        LEFT JOIN AVALIACAO av ON o.ID = av.ID_OFERTA
        LEFT JOIN AVALIACAO_ALUNO aa ON av.ID = aa.ID_AVALIACAO AND a.MATRICULA = aa.ID_ALUNO
        WHERE a.MATRICULA = :student_id
        ORDER BY o.ANO DESC, o.SEMESTRE DESC, m.NOME, av.DATA
        """
        # VULNERÁVEL: Usando concatenação de strings
        sql = sql.replace(':student_id', str(student_id))
        cur.execute(sql)
        rows = cur.fetchall()
        
        if not rows or rows[0][0] is None:
            return jsonify({'error': 'Aluno não encontrado'}), 404
        
        report = {
            'aluno_nome': rows[0][0],
            'curso_nome': rows[0][1],
            'materias': {}
        }
        
        for row in rows:
            if row[2]:  # Se tem matéria
                materia_key = f"{row[2]}_{row[3]}_{row[4]}"
                if materia_key not in report['materias']:
                    report['materias'][materia_key] = {
                        'materia_nome': row[2],
                        'ano': row[3],
                        'semestre': row[4],
                        'status': row[8],
                        'media_final': row[9],
                        'media_aprovacao': row[10],
                        'avaliacoes': []
                    }
                
                if row[5]:  # Se tem avaliação
                    report['materias'][materia_key]['avaliacoes'].append({
                        'tipo': row[5],
                        'peso': row[6],
                        'nota': row[7]
                    })
        
        # Converter dict para list
        report['materias'] = list(report['materias'].values())
        
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
        # VULNERÁVEL: Informações do professor
        sql_prof = "SELECT NOME, EMAIL, STATUS FROM PROFESSOR WHERE ID_PROFESSOR = " + str(professor_id)
        cur.execute(sql_prof)
        professor_info = cur.fetchone()
        if not professor_info:
            return jsonify({'error': 'Professor não encontrado'}), 404
        
        # VULNERÁVEL: Ofertas por semestre
        sql_offers = """
            SELECT o.ANO, o.SEMESTRE, m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME,
                   m.CARGA_HORARIA, COUNT(ga.ID_ALUNO) as TOTAL_ALUNOS
            FROM OFERTA o
            JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
            JOIN CURSO c ON o.ID_CURSO = c.ID
            LEFT JOIN GRADE_ALUNO ga ON o.ID = ga.ID_OFERTA
            WHERE o.ID_PROFESSOR = """ + str(professor_id) + """
            GROUP BY o.ANO, o.SEMESTRE, m.NOME, c.NOME, m.CARGA_HORARIA, o.ID
            ORDER BY o.ANO DESC, o.SEMESTRE DESC
        """
        cur.execute(sql_offers)
        
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
