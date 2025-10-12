from flask import Blueprint, request, jsonify
from db.db_conn import get_connection, release_connection

bp = Blueprint('reports', __name__)

# ===== RELATÓRIOS ESSENCIAIS DO SISTEMA =====
# Apenas relatórios ativamente utilizados pelo frontend

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

@bp.route('/reports/course-statistics', methods=['GET'])
def course_statistics():
    """Relatório de estatísticas por curso usando COUNT() e SUM()"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT 
                c.ID as CURSO_ID,
                c.NOME as CURSO_NOME,
                c.CARGA_HORARIA_TOTAL as CARGA_TOTAL_CURSO,
                COUNT(DISTINCT a.MATRICULA) as TOTAL_ALUNOS,
                COUNT(DISTINCT m.ID_MATERIA) as TOTAL_MATERIAS,
                SUM(CASE WHEN m.CARGA_HORARIA IS NOT NULL THEN m.CARGA_HORARIA ELSE 0 END) as CARGA_HORARIA_MATERIAS,
                COUNT(DISTINCT o.ID) as TOTAL_OFERTAS,
                COUNT(DISTINCT ga.ID_ALUNO) as TOTAL_MATRICULAS_ATIVAS,
                COUNT(DISTINCT CASE WHEN o.ANO = EXTRACT(YEAR FROM SYSDATE) THEN o.ID END) as OFERTAS_ANO_ATUAL
            FROM CURSO c
            LEFT JOIN ALUNO a ON c.ID = a.ID_CURSO
            LEFT JOIN MATERIA m ON c.ID = m.ID_CURSO  
            LEFT JOIN OFERTA o ON c.ID = o.ID_CURSO
            LEFT JOIN GRADE_ALUNO ga ON o.ID = ga.ID_OFERTA
            GROUP BY c.ID, c.NOME, c.CARGA_HORARIA_TOTAL
            ORDER BY TOTAL_ALUNOS DESC, TOTAL_OFERTAS DESC
        """)
        
        courses = cur.fetchall()
        
        # Calcular totais gerais
        total_students = sum(course[3] for course in courses)
        total_subjects = sum(course[4] for course in courses)
        total_offers = sum(course[6] for course in courses)
        total_enrollments = sum(course[7] for course in courses)
        
        report = {
            'resumo_geral': {
                'total_cursos': len(courses),
                'total_alunos_sistema': total_students,
                'total_materias_sistema': total_subjects,
                'total_ofertas_sistema': total_offers,
                'total_matriculas_sistema': total_enrollments
            },
            'estatisticas_por_curso': []
        }
        
        for course in courses:
            # Calcular percentuais
            perc_alunos = (course[3] / total_students * 100) if total_students > 0 else 0
            perc_ofertas = (course[6] / total_offers * 100) if total_offers > 0 else 0
            
            report['estatisticas_por_curso'].append({
                'curso_id': course[0],
                'curso_nome': course[1],
                'carga_horaria_total_curso': course[2],
                'total_alunos': course[3],
                'total_materias': course[4],
                'carga_horaria_materias': course[5],
                'total_ofertas': course[6],
                'total_matriculas_ativas': course[7],
                'ofertas_ano_atual': course[8],
                'percentual_alunos': round(perc_alunos, 2),
                'percentual_ofertas': round(perc_ofertas, 2),
                'media_alunos_por_oferta': round(course[7] / course[6], 2) if course[6] > 0 else 0
            })
        
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar relatório: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/reports/offers-complete', methods=['GET'])
def offers_complete_report():
    """Relatório completo de ofertas com múltiplos JOINs"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT 
                o.ID as OFERTA_ID,
                o.ANO,
                o.SEMESTRE,
                c.NOME as CURSO_NOME,
                m.NOME as MATERIA_NOME,
                m.PERIODO as PERIODO_MATERIA,
                m.CARGA_HORARIA as CARGA_HORARIA_MATERIA,
                p.NOME as PROFESSOR_NOME,
                p.EMAIL as PROFESSOR_EMAIL,
                p.STATUS as PROFESSOR_STATUS,
                COUNT(ga.ID_ALUNO) as TOTAL_MATRICULADOS,
                c.CARGA_HORARIA_TOTAL as CARGA_TOTAL_CURSO
            FROM OFERTA o
            INNER JOIN CURSO c ON o.ID_CURSO = c.ID
            INNER JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
            INNER JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR
            LEFT JOIN GRADE_ALUNO ga ON o.ID = ga.ID_OFERTA
            GROUP BY o.ID, o.ANO, o.SEMESTRE, c.NOME, m.NOME, m.PERIODO, 
                     m.CARGA_HORARIA, p.NOME, p.EMAIL, p.STATUS, c.CARGA_HORARIA_TOTAL
            ORDER BY o.ANO DESC, o.SEMESTRE DESC, c.NOME, m.NOME
        """)
        
        offers = cur.fetchall()
        
        # Estatísticas gerais
        total_offers = len(offers)
        total_students = sum(offer[10] for offer in offers)
        active_professors = len(set(offer[7] for offer in offers)) if offers else 0
        active_courses = len(set(offer[3] for offer in offers)) if offers else 0
        
        report = {
            'resumo_geral': {
                'total_ofertas': total_offers,
                'total_matriculados': total_students,
                'professores_ativos': active_professors,
                'cursos_ativos': active_courses,
                'media_alunos_por_oferta': round(total_students / total_offers, 2) if total_offers > 0 else 0
            },
            'todas_ofertas': []
        }
        
        # Lista completa para tabela detalhada
        for offer in offers:
            report['todas_ofertas'].append({
                'oferta_id': offer[0],
                'periodo': f"{offer[1]}/{offer[2]}º",
                'curso_nome': offer[3],
                'materia_nome': offer[4],
                'periodo_materia': f"{offer[5]}º período",
                'carga_horaria': f"{offer[6]}h",
                'professor_nome': offer[7],
                'professor_email': offer[8],
                'professor_status': offer[9],
                'total_matriculados': offer[10],
                'ocupacao_percentual': f"{(offer[10] / 40 * 100):.1f}%" if offer[10] > 0 else "0%"
            })
        
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar relatório de ofertas: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)
