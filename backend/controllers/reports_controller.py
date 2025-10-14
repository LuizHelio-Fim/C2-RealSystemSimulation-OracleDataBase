from flask import Blueprint, request, jsonify
from db.db_conn import get_connection, release_connection

bp = Blueprint('reports', __name__)

# ===== RELATÓRIOS ESSENCIAIS DO SISTEMA =====
# Apenas relatórios ativamente utilizados pelo frontend

@bp.route('/reports/dashboard', methods=['GET'])
def dashboard_summary():
    """Resumo geral do sistema para dashboard"""
    conn = None
    cur = None
    
    try:
        print("🔄 [DASHBOARD] Iniciando geração de relatório do dashboard...")
        
        # Testar conexão com banco
        conn = get_connection()
        if not conn:
            raise Exception("Falha ao estabelecer conexão com o banco de dados")
        
        cur = conn.cursor()
        print("✅ [DASHBOARD] Conexão com banco estabelecida com sucesso")
        
    except Exception as e:
        error_msg = f"Erro de conexão com banco: {str(e)}"
        print(f"❌ [DASHBOARD] {error_msg}")
        return jsonify({'error': error_msg, 'tipo': 'conexao_banco'}), 500
    
    try:
        print("📊 [DASHBOARD] Coletando contadores gerais...")
        
        # Contadores gerais com tratamento de valores NULL
        try:
            cur.execute("SELECT COALESCE(COUNT(*), 0) FROM CURSO")
            total_courses = cur.fetchone()[0]
            print(f"✅ [DASHBOARD] Total de cursos: {total_courses}")
        except Exception as e:
            print(f"❌ [DASHBOARD] Erro ao contar cursos: {e}")
            raise Exception(f"Erro ao acessar tabela CURSO: {str(e)}")
        
        try:
            cur.execute("SELECT COALESCE(COUNT(*), 0) FROM ALUNO")
            total_students = cur.fetchone()[0]
            print(f"✅ [DASHBOARD] Total de alunos: {total_students}")
        except Exception as e:
            print(f"❌ [DASHBOARD] Erro ao contar alunos: {e}")
            raise Exception(f"Erro ao acessar tabela ALUNO: {str(e)}")
        
        try:
            cur.execute("SELECT COALESCE(COUNT(*), 0) FROM PROFESSOR")
            total_professors = cur.fetchone()[0]
            print(f"✅ [DASHBOARD] Total de professores: {total_professors}")
        except Exception as e:
            print(f"❌ [DASHBOARD] Erro ao contar professores: {e}")
            raise Exception(f"Erro ao acessar tabela PROFESSOR: {str(e)}")
        
        try:
            cur.execute("SELECT COALESCE(COUNT(*), 0) FROM MATERIA")
            total_subjects = cur.fetchone()[0]
            print(f"✅ [DASHBOARD] Total de matérias: {total_subjects}")
        except Exception as e:
            print(f"❌ [DASHBOARD] Erro ao contar matérias: {e}")
            raise Exception(f"Erro ao acessar tabela MATERIA: {str(e)}")
        
        try:
            cur.execute("SELECT COALESCE(COUNT(*), 0) FROM OFERTA")
            total_offers = cur.fetchone()[0]
            print(f"✅ [DASHBOARD] Total de ofertas: {total_offers}")
        except Exception as e:
            print(f"❌ [DASHBOARD] Erro ao contar ofertas: {e}")
            raise Exception(f"Erro ao acessar tabela OFERTA: {str(e)}")
        
        try:
            cur.execute("SELECT COALESCE(COUNT(*), 0) FROM GRADE_ALUNO")
            total_enrollments = cur.fetchone()[0]
            print(f"✅ [DASHBOARD] Total de matrículas: {total_enrollments}")
        except Exception as e:
            print(f"❌ [DASHBOARD] Erro ao contar matrículas: {e}")
            raise Exception(f"Erro ao acessar tabela GRADE_ALUNO: {str(e)}")
        
        print("📅 [DASHBOARD] Coletando atividades recentes...")
        
        # Últimas atividades (baseado em data de nascimento como proxy) com tratamento NULL
        try:
            cur.execute("""
                SELECT 'Aluno' as TIPO, 
                       COALESCE(NOME, 'Nome não informado') as NOME, 
                       COALESCE(TO_CHAR(DATA_NASC, 'YYYY-MM-DD'), 'Data não informada') as DATA
                FROM ALUNO 
                WHERE DATA_NASC IS NOT NULL
                ORDER BY DATA_NASC DESC 
                FETCH FIRST 5 ROWS ONLY
            """)
            recent_students = cur.fetchall()
            print(f"✅ [DASHBOARD] Coletados {len(recent_students)} alunos recentes")
        except Exception as e:
            print(f"❌ [DASHBOARD] Erro ao buscar alunos recentes: {e}")
            recent_students = []
        
        try:
            cur.execute("""
                SELECT 'Professor' as TIPO, 
                       COALESCE(NOME, 'Nome não informado') as NOME, 
                       COALESCE(TO_CHAR(DATA_NASC, 'YYYY-MM-DD'), 'Data não informada') as DATA
                FROM PROFESSOR 
                WHERE DATA_NASC IS NOT NULL
                ORDER BY DATA_NASC DESC 
                FETCH FIRST 5 ROWS ONLY
            """)
            recent_professors = cur.fetchall()
            print(f"✅ [DASHBOARD] Coletados {len(recent_professors)} professores recentes")
        except Exception as e:
            print(f"❌ [DASHBOARD] Erro ao buscar professores recentes: {e}")
            recent_professors = []
        
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
        
        print("✅ [DASHBOARD] Relatório gerado com sucesso")
        return jsonify(report), 200
        
    except Exception as e:
        error_msg = f'Erro ao gerar dashboard: {str(e)}'
        error_type = 'sql_error' if 'ORA-' in str(e) else 'processamento'
        
        print(f"❌ [DASHBOARD] {error_msg}")
        
        # Log detalhado do erro
        import traceback
        print(f"📋 [DASHBOARD] Stack trace completo:\n{traceback.format_exc()}")
        
        return jsonify({
            'error': error_msg, 
            'tipo': error_type,
            'detalhes': str(e)
        }), 500
        
    finally:
        try:
            if cur:
                cur.close()
            if conn:
                release_connection(conn)
            print("🔒 [DASHBOARD] Conexões fechadas")
        except Exception as e:
            print(f"⚠️ [DASHBOARD] Erro ao fechar conexões: {e}")

@bp.route('/reports/course-statistics', methods=['GET'])
def course_statistics():
    """Relatório de estatísticas por curso usando COUNT() e SUM()"""
    conn = None
    cur = None
    
    try:
        print("🔄 [COURSE_STATS] Iniciando geração de estatísticas por curso...")
        
        # Testar conexão com banco
        conn = get_connection()
        if not conn:
            raise Exception("Falha ao estabelecer conexão com o banco de dados")
        
        cur = conn.cursor()
        print("✅ [COURSE_STATS] Conexão com banco estabelecida com sucesso")
        
    except Exception as e:
        error_msg = f"Erro de conexão com banco: {str(e)}"
        print(f"❌ [COURSE_STATS] {error_msg}")
        return jsonify({'error': error_msg, 'tipo': 'conexao_banco'}), 500
    
    try:
        print("📊 [COURSE_STATS] Executando consulta principal...")
        
        # Consulta melhorada com COALESCE para tratar NULLs
        cur.execute("""
            SELECT 
                COALESCE(c.ID, 0) as CURSO_ID,
                COALESCE(c.NOME, 'Nome não informado') as CURSO_NOME,
                COALESCE(c.CARGA_HORARIA_TOTAL, 0) as CARGA_TOTAL_CURSO,
                COALESCE(COUNT(DISTINCT a.MATRICULA), 0) as TOTAL_ALUNOS,
                COALESCE(COUNT(DISTINCT m.ID_MATERIA), 0) as TOTAL_MATERIAS,
                COALESCE(SUM(COALESCE(m.CARGA_HORARIA, 0)), 0) as CARGA_HORARIA_MATERIAS,
                COALESCE(COUNT(DISTINCT o.ID), 0) as TOTAL_OFERTAS,
                COALESCE(COUNT(DISTINCT ga.ID_ALUNO), 0) as TOTAL_MATRICULAS_ATIVAS,
                COALESCE(COUNT(DISTINCT CASE WHEN o.ANO = EXTRACT(YEAR FROM SYSDATE) THEN o.ID END), 0) as OFERTAS_ANO_ATUAL
            FROM CURSO c
            LEFT JOIN ALUNO a ON c.ID = a.ID_CURSO
            LEFT JOIN MATERIA m ON c.ID = m.ID_CURSO  
            LEFT JOIN OFERTA o ON c.ID = o.ID_CURSO
            LEFT JOIN GRADE_ALUNO ga ON o.ID = ga.ID_OFERTA
            GROUP BY c.ID, c.NOME, c.CARGA_HORARIA_TOTAL
            ORDER BY TOTAL_ALUNOS DESC, TOTAL_OFERTAS DESC
        """)
        
        courses = cur.fetchall()
        print(f"✅ [COURSE_STATS] Consulta executada. {len(courses)} cursos encontrados")
        
        if not courses:
            print("⚠️ [COURSE_STATS] Nenhum curso encontrado no banco")
            return jsonify({
                'resumo_geral': {
                    'total_cursos': 0,
                    'total_alunos_sistema': 0,
                    'total_materias_sistema': 0,
                    'total_ofertas_sistema': 0,
                    'total_matriculas_sistema': 0
                },
                'estatisticas_por_curso': [],
                'mensagem': 'Nenhum curso cadastrado no sistema'
            }), 200
        
        # Calcular totais gerais com tratamento de valores None
        try:
            total_students = sum(course[3] or 0 for course in courses)
            total_subjects = sum(course[4] or 0 for course in courses)
            total_offers = sum(course[6] or 0 for course in courses)
            total_enrollments = sum(course[7] or 0 for course in courses)
            
            print(f"📊 [COURSE_STATS] Totais calculados - Alunos: {total_students}, Ofertas: {total_offers}")
        except Exception as e:
            print(f"❌ [COURSE_STATS] Erro ao calcular totais: {e}")
            raise Exception(f"Erro no processamento dos dados: {str(e)}")
        
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
        
        print("🔄 [COURSE_STATS] Processando estatísticas por curso...")
        
        for i, course in enumerate(courses):
            try:
                # Calcular percentuais com proteção contra divisão por zero
                perc_alunos = (course[3] / total_students * 100) if total_students > 0 else 0
                perc_ofertas = (course[6] / total_offers * 100) if total_offers > 0 else 0
                
                # Calcular média com proteção contra divisão por zero
                media_alunos_por_oferta = round(course[7] / course[6], 2) if course[6] and course[6] > 0 else 0
                
                course_stats = {
                    'curso_id': course[0] or 0,
                    'curso_nome': course[1] or 'Nome não informado',
                    'carga_horaria_total_curso': course[2] or 0,
                    'total_alunos': course[3] or 0,
                    'total_materias': course[4] or 0,
                    'carga_horaria_materias': course[5] or 0,
                    'total_ofertas': course[6] or 0,
                    'total_matriculas_ativas': course[7] or 0,
                    'ofertas_ano_atual': course[8] or 0,
                    'percentual_alunos': round(perc_alunos, 2),
                    'percentual_ofertas': round(perc_ofertas, 2),
                    'media_alunos_por_oferta': media_alunos_por_oferta
                }
                
                report['estatisticas_por_curso'].append(course_stats)
                
            except Exception as e:
                print(f"⚠️ [COURSE_STATS] Erro ao processar curso {i+1}: {e}")
                # Continua processamento dos outros cursos
                continue
        
        print(f"✅ [COURSE_STATS] Relatório gerado com {len(report['estatisticas_por_curso'])} cursos")
        return jsonify(report), 200
        
    except Exception as e:
        error_msg = f'Erro ao gerar relatório de estatísticas: {str(e)}'
        error_type = 'sql_error' if 'ORA-' in str(e) else 'processamento'
        
        print(f"❌ [COURSE_STATS] {error_msg}")
        
        # Log detalhado do erro
        import traceback
        print(f"📋 [COURSE_STATS] Stack trace completo:\n{traceback.format_exc()}")
        
        return jsonify({
            'error': error_msg, 
            'tipo': error_type,
            'detalhes': str(e)
        }), 500
        
    finally:
        try:
            if cur:
                cur.close()
            if conn:
                release_connection(conn)
            print("🔒 [COURSE_STATS] Conexões fechadas")
        except Exception as e:
            print(f"⚠️ [COURSE_STATS] Erro ao fechar conexões: {e}")

@bp.route('/reports/offers-complete', methods=['GET'])
def offers_complete_report():
    """Relatório completo de ofertas com múltiplos JOINs"""
    conn = None
    cur = None
    
    try:
        print("🔄 [OFFERS_REPORT] Iniciando geração de relatório de ofertas...")
        
        # Estabelecer conexão com banco
        conn = get_connection()
        if not conn:
            raise Exception("Falha ao estabelecer conexão com o banco de dados")
        
        cur = conn.cursor()
        print("✅ [OFFERS_REPORT] Conexão com banco estabelecida com sucesso")
        
        print("📊 [OFFERS_REPORT] Executando consulta principal...")
        
        # Consulta melhorada com COALESCE para tratar NULLs
        cur.execute("""
            SELECT 
                COALESCE(o.ID, 0) as OFERTA_ID,
                COALESCE(o.ANO, 0) as ANO,
                COALESCE(o.SEMESTRE, 0) as SEMESTRE,
                COALESCE(c.NOME, 'Curso não informado') as CURSO_NOME,
                COALESCE(m.NOME, 'Matéria não informada') as MATERIA_NOME,
                COALESCE(m.PERIODO, 0) as PERIODO_MATERIA,
                COALESCE(m.CARGA_HORARIA, 0) as CARGA_HORARIA_MATERIA,
                COALESCE(p.NOME, 'Professor não informado') as PROFESSOR_NOME,
                COALESCE(p.EMAIL, 'Email não informado') as PROFESSOR_EMAIL,
                COALESCE(p.STATUS, 'Status não informado') as PROFESSOR_STATUS,
                COALESCE(COUNT(ga.ID_ALUNO), 0) as TOTAL_MATRICULADOS,
                COALESCE(c.CARGA_HORARIA_TOTAL, 0) as CARGA_TOTAL_CURSO
            FROM OFERTA o
            INNER JOIN CURSO c ON o.ID_CURSO = c.ID
            INNER JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
            INNER JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR
            LEFT JOIN GRADE_ALUNO ga ON o.ID = ga.ID_OFERTA
            GROUP BY o.ID, o.ANO, o.SEMESTRE, c.NOME, m.NOME, m.PERIODO, 
                     m.CARGA_HORARIA, p.NOME, p.EMAIL, p.STATUS, c.CARGA_HORARIA_TOTAL
            ORDER BY COALESCE(o.ANO, 0) DESC, COALESCE(o.SEMESTRE, 0) DESC, 
                     COALESCE(c.NOME, 'ZZZ'), COALESCE(m.NOME, 'ZZZ')
        """)
        
        offers = cur.fetchall()
        print(f"✅ [OFFERS_REPORT] Consulta executada. {len(offers)} ofertas encontradas")
        
        if not offers:
            print("⚠️ [OFFERS_REPORT] Nenhuma oferta encontrada no banco")
            return jsonify({
                'resumo_geral': {
                    'total_ofertas': 0,
                    'total_matriculados': 0,
                    'professores_ativos': 0,
                    'cursos_ativos': 0,
                    'media_alunos_por_oferta': 0
                },
                'todas_ofertas': [],
                'mensagem': 'Nenhuma oferta cadastrada no sistema'
            }), 200
        
        # Estatísticas gerais com tratamento de valores None
        total_offers = len(offers)
        total_students = sum(offer[10] or 0 for offer in offers)
        
        # Usar set para contar únicos, tratando valores None
        professor_names = {offer[7] for offer in offers if offer[7] and offer[7] != 'Professor não informado'}
        course_names = {offer[3] for offer in offers if offer[3] and offer[3] != 'Curso não informado'}
        
        active_professors = len(professor_names)
        active_courses = len(course_names)
        
        print(f"📊 [OFFERS_REPORT] Estatísticas - Ofertas: {total_offers}, Matriculados: {total_students}")
        
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
        
        print("🔄 [OFFERS_REPORT] Processando detalhes das ofertas...")
        
        # Lista completa para tabela detalhada com tratamento de erros
        processed_offers = 0
        for i, offer in enumerate(offers):
            try:
                # Usar campos diretos da consulta
                total_matriculados = offer[10] or 0
                carga_total_curso = offer[11] or 0
                
                offer_detail = {
                    'oferta_id': offer[0] or 0,
                    'periodo': f"{offer[1] or 0}/{offer[2] or 0}º",
                    'curso_nome': offer[3] or 'Curso não informado',
                    'materia_nome': offer[4] or 'Matéria não informada',
                    'periodo_materia': f"{offer[5] or 0}º período",
                    'carga_horaria': f"{offer[6] or 0}h",
                    'professor_nome': offer[7] or 'Professor não informado',
                    'professor_email': offer[8] or 'Email não informado',
                    'professor_status': offer[9] or 'Status não informado',
                    'total_matriculados': total_matriculados,
                    'carga_total_curso': carga_total_curso
                }
                
                report['todas_ofertas'].append(offer_detail)
                processed_offers += 1
                
            except Exception as e:
                print(f"⚠️ [OFFERS_REPORT] Erro ao processar oferta {i+1}: {e}")
                # Continua processamento das outras ofertas
                continue
        
        print(f"✅ [OFFERS_REPORT] Relatório gerado com {processed_offers} ofertas processadas")
        return jsonify(report), 200
        
    except Exception as e:
        error_msg = f'Erro ao gerar relatório de ofertas: {str(e)}'
        error_type = 'sql_error' if 'ORA-' in str(e) else 'processamento'
        
        print(f"❌ [OFFERS_REPORT] {error_msg}")
        
        # Log detalhado do erro
        import traceback
        print(f"📋 [OFFERS_REPORT] Stack trace completo:\n{traceback.format_exc()}")
        
        return jsonify({
            'error': error_msg, 
            'tipo': error_type,
            'detalhes': str(e)
        }), 500
        
    finally:
        try:
            if cur:
                cur.close()
                print("🔒 [OFFERS_REPORT] Cursor fechado")
            if conn:
                release_connection(conn)
                print("🔒 [OFFERS_REPORT] Conexão liberada")
        except Exception as e:
            print(f"⚠️ [OFFERS_REPORT] Erro ao fechar conexões: {e}")
