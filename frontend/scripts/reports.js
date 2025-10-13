// reports.js - Funções para gerar e exibir relatórios

// ===== FUNÇÕES DE RELATÓRIOS =====

async function loadCourseStatisticsReport() {
  try {
    console.log('🔄 [FRONTEND] Iniciando carregamento de estatísticas por curso...');
    showLoading('Carregando estatísticas por curso...');
    
    const data = await apiService.getCourseStatistics();
    console.log('✅ [FRONTEND] Dados recebidos:', data);
    
    // Detectar se estamos na view específica ou na view geral de reports
    const courseStatsContent = document.getElementById('courseStatisticsContent');
    const reportContent = document.getElementById('reportContent');
    const targetContainer = courseStatsContent || reportContent;
    targetContainer.innerHTML = `
      <div class="report-section">
        <h2>📊 Estatísticas por Curso</h2>
        
        <!-- Resumo Geral -->
        <div class="dashboard-grid" style="margin-bottom: 2rem;">
          <div class="stat-card">
            <span class="stat-number">${data.resumo_geral.total_cursos}</span>
            <span class="stat-label">Total de Cursos</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">${data.resumo_geral.total_alunos_sistema}</span>
            <span class="stat-label">Total de Alunos</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">${data.resumo_geral.total_ofertas_sistema}</span>
            <span class="stat-label">Total de Ofertas</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">${data.resumo_geral.total_matriculas_sistema}</span>
            <span class="stat-label">Total de Matrículas</span>
          </div>
        </div>
        
        <!-- Tabela Detalhada -->
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Curso</th>
                <th>Total Alunos</th>
                <th>Total Matérias</th>
                <th>Carga Horária (Matérias)</th>
                <th>Total Ofertas</th>
                <th>Matrículas Ativas</th>
                <th>% Alunos</th>
                <th>Média Alunos/Oferta</th>
              </tr>
            </thead>
            <tbody>
              ${data.estatisticas_por_curso.map(curso => `
                <tr>
                  <td><strong>${curso.curso_nome}</strong></td>
                  <td>${curso.total_alunos}</td>
                  <td>${curso.total_materias}</td>
                  <td>${curso.carga_horaria_materias}h</td>
                  <td>${curso.total_ofertas}</td>
                  <td>${curso.total_matriculas_ativas}</td>
                  <td>${curso.percentual_alunos}%</td>
                  <td>${curso.media_alunos_por_oferta}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
    
    hideLoading();
  } catch (error) {
    console.error('❌ [FRONTEND] Erro ao carregar estatísticas por curso:', error);
    
    // Extrair detalhes do erro se disponível
    let errorMessage = 'Erro ao carregar relatório de estatísticas por curso';
    let errorDetails = '';
    
    if (error.message) {
      errorDetails = error.message;
    }
    
    // Se o erro contém informações do backend
    if (error.response) {
      try {
        const errorData = JSON.parse(error.response);
        if (errorData.error) {
          errorDetails = errorData.error;
        }
        if (errorData.tipo) {
          errorMessage += ` (${errorData.tipo})`;
        }
        console.error('📋 [FRONTEND] Detalhes do backend:', errorData);
      } catch (parseError) {
        console.error('⚠️ [FRONTEND] Erro ao parsear resposta do backend:', parseError);
      }
    }
    
    // Mostrar container com erro detalhado
    const courseStatsContent = document.getElementById('courseStatisticsContent');
    const reportContent = document.getElementById('reportContent');
    const targetContainer = courseStatsContent || reportContent;
    
    if (targetContainer) {
      targetContainer.innerHTML = `
        <div class="error-container" style="
          padding: 2rem; 
          background: #fef2f2; 
          border: 1px solid #fecaca; 
          border-radius: 8px;
          color: #991b1b;
        ">
          <h3>❌ Erro no Relatório</h3>
          <p><strong>Problema:</strong> ${errorMessage}</p>
          ${errorDetails ? `<p><strong>Detalhes:</strong> ${errorDetails}</p>` : ''}
          <p><strong>Sugestões:</strong></p>
          <ul>
            <li>Verifique se o backend está rodando</li>
            <li>Verifique a conexão com o banco de dados</li>
            <li>Consulte os logs do servidor para mais detalhes</li>
          </ul>
        </div>
      `;
    }
    
    showNotification(errorMessage, 'error');
    hideLoading();
  }
}

async function loadOffersCompleteReport() {
  try {
    console.log('🔄 [FRONTEND] Iniciando carregamento de relatório de ofertas...');
    showLoading('Carregando relatório de ofertas...');
    
    const data = await apiService.getOffersCompleteReport();
    console.log('✅ [FRONTEND] Dados recebidos:', data);
    
    // Detectar se estamos na view específica ou na view geral de reports
    const offersCompleteContent = document.getElementById('offersCompleteContent');
    const reportContent = document.getElementById('reportContent');
    const targetContainer = offersCompleteContent || reportContent;
    targetContainer.innerHTML = `
      <div class="report-section">
        <h2>📋 Relatório Completo de Ofertas</h2>
        
        <!-- Resumo Geral -->
        <div class="dashboard-grid" style="margin-bottom: 2rem;">
          <div class="stat-card">
            <span class="stat-number">${data.resumo_geral.total_ofertas}</span>
            <span class="stat-label">Total de Ofertas</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">${data.resumo_geral.total_matriculados}</span>
            <span class="stat-label">Total Matriculados</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">${data.resumo_geral.professores_ativos}</span>
            <span class="stat-label">Professores Ativos</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">${data.resumo_geral.media_alunos_por_oferta}</span>
            <span class="stat-label">Média Alunos/Oferta</span>
          </div>
        </div>
        
        <!-- Tabela de Ofertas -->
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Período</th>
                <th>Curso</th>
                <th>Matéria</th>
                <th>Período Mat.</th>
                <th>Carga Hor.</th>
                <th>Professor</th>
                <th>Email Professor</th>
                <th>Status Prof.</th>
                <th>Matriculados</th>
                <th>Ocupação</th>
              </tr>
            </thead>
            <tbody>
              ${data.todas_ofertas.map(oferta => `
                <tr>
                  <td>${oferta.oferta_id}</td>
                  <td>${oferta.periodo}</td>
                  <td>${oferta.curso_nome}</td>
                  <td><strong>${oferta.materia_nome}</strong></td>
                  <td>${oferta.periodo_materia}</td>
                  <td>${oferta.carga_horaria}</td>
                  <td>${oferta.professor_nome}</td>
                  <td>${oferta.professor_email}</td>
                  <td><span class="status ${oferta.professor_status.toLowerCase()}">${oferta.professor_status}</span></td>
                  <td><strong>${oferta.total_matriculados}</strong></td>
                  <td>${oferta.ocupacao_percentual}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
    
    hideLoading();
  } catch (error) {
    console.error('❌ [FRONTEND] Erro ao carregar relatório de ofertas:', error);
    
    // Extrair detalhes do erro se disponível
    let errorMessage = 'Erro ao carregar relatório de ofertas';
    let errorDetails = '';
    
    if (error.message) {
      errorDetails = error.message;
    }
    
    // Se o erro contém informações do backend
    if (error.response) {
      try {
        const errorData = JSON.parse(error.response);
        if (errorData.error) {
          errorDetails = errorData.error;
        }
        if (errorData.tipo) {
          errorMessage += ` (${errorData.tipo})`;
        }
        console.error('📋 [FRONTEND] Detalhes do backend:', errorData);
      } catch (parseError) {
        console.error('⚠️ [FRONTEND] Erro ao parsear resposta do backend:', parseError);
      }
    }
    
    // Mostrar container com erro detalhado
    const offersCompleteContent = document.getElementById('offersCompleteContent');
    const reportContent = document.getElementById('reportContent');
    const targetContainer = offersCompleteContent || reportContent;
    
    if (targetContainer) {
      targetContainer.innerHTML = `
        <div class="error-container" style="
          padding: 2rem; 
          background: #fef2f2; 
          border: 1px solid #fecaca; 
          border-radius: 8px;
          color: #991b1b;
        ">
          <h3>❌ Erro no Relatório</h3>
          <p><strong>Problema:</strong> ${errorMessage}</p>
          ${errorDetails ? `<p><strong>Detalhes:</strong> ${errorDetails}</p>` : ''}
          <p><strong>Sugestões:</strong></p>
          <ul>
            <li>Verifique se o backend está rodando</li>
            <li>Verifique a conexão com o banco de dados</li>
            <li>Consulte os logs do servidor para mais detalhes</li>
          </ul>
        </div>
      `;
    }
    
    showNotification(errorMessage, 'error');
    hideLoading();
  }
}