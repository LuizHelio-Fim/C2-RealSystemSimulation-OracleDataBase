// Sistema de notificações empilhadas
let notificationContainer = null;
let notificationCount = 0;
let recentNotifications = new Map(); // Cache de notificações recentes

function showNotification(message, type = 'info') {
  // Verificar se já existe uma notificação idêntica recente (últimos 2 segundos)
  const notificationKey = `${type}:${message}`;
  const now = Date.now();
  
  if (recentNotifications.has(notificationKey)) {
    const lastTime = recentNotifications.get(notificationKey);
    if (now - lastTime < 2000) { // 2 segundos
      return; // Ignorar notificação duplicada
    }
  }
  
  // Registrar esta notificação
  recentNotifications.set(notificationKey, now);
  
  // Limpar notificações antigas do cache (mais de 5 segundos)
  for (const [key, time] of recentNotifications.entries()) {
    if (now - time > 5000) {
      recentNotifications.delete(key);
    }
  }

  // Criar container se não existir
  if (!notificationContainer) {
    notificationContainer = document.createElement("div");
    notificationContainer.id = "notificationContainer";
    notificationContainer.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 10000;
      display: flex;
      flex-direction: column;
      gap: 10px;
      pointer-events: none;
    `;
    document.body.appendChild(notificationContainer);
  }

  const notification = document.createElement("div");
  const notificationId = `notification-${notificationCount++}`;
  notification.id = notificationId;
  notification.style.cssText = `
    padding: 1rem 1.5rem;
    background: ${type === "success" ? "#10b981" : type === "error" ? "#ef4444" : "#3b82f6"};
    color: white;
    border-radius: 8px;
    animation: slideInRight 0.3s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    max-width: 350px;
    pointer-events: auto;
    cursor: pointer;
    word-wrap: break-word;
  `;
  notification.textContent = message;
  
  // Clique para remover
  notification.onclick = () => removeNotification(notification);
  
  notificationContainer.appendChild(notification);

  // Auto-remover após 5 segundos
  setTimeout(() => {
    removeNotification(notification);
  }, 5000);
}

function removeNotification(notification) {
  if (notification && notification.parentNode) {
    notification.style.animation = "slideOutRight 0.3s ease";
    setTimeout(() => {
      if (notification.parentNode) {
        notification.remove();
        
        // Remover container se vazio
        if (notificationContainer && notificationContainer.children.length === 0) {
          notificationContainer.remove();
          notificationContainer = null;
        }
      }
    }, 300);
  }
}

// Estado da aplicação
const appState = {
  students: [],
  courses: [],
  professors: [],
  subjects: [],
  offers: [],
  enrollments: [],
  currentSection: 'dashboard'
}

// Inicialização da aplicação
document.addEventListener("DOMContentLoaded", async () => {
  console.log("DOM carregado, iniciando aplicação...") // Debug
  
  try {
    // Carregar dados da API
    const success = await dataManager.loadAllData();
    console.log("Dados carregados:", success) // Debug
    
    if (success) {
      // Sincronizar dados com appState
      appState.students = dataManager.state.students;
      appState.courses = dataManager.state.courses;
      appState.professors = dataManager.state.professors;
      appState.subjects = dataManager.state.subjects;
      appState.offers = dataManager.state.offers;
      appState.enrollments = dataManager.state.enrollments;
      
      // Carregar todas as tabelas
      loadStudentsTable();
      loadCoursesTable();
      loadProfessorsTable();
      loadSubjectsTable();
      loadOffersTable();
      loadEnrollmentsTable();
      updateDashboard();
    }
  } catch (error) {
    console.error("Erro ao carregar dados:", error)
    showNotification("Erro ao carregar dados. Verifique se o backend está rodando.", "error")
  }

  // Animar estatísticas da splash screen
  setTimeout(() => {
    animateSplashStats()
  }, 500)

  // Mostrar aplicação principal após splash
  setTimeout(() => {
    console.log("Mostrando aplicação principal...") // Debug
    const appContainer = document.getElementById("appContainer")
    if (appContainer) {
      appContainer.classList.add("active")
      console.log("Aplicação principal ativada") // Debug
    } else {
      console.error("Container da aplicação não encontrado!") // Debug
    }
  }, 4500)

  // Inicializar navegação
  initNavigation()
})



// Animação dos números da splash screen com efeito escalonado
function animateSplashStats() {
  const stats = [
    { id: "totalStudents", value: appState.students.length, delay: 0 },
    { id: "totalCourses", value: appState.courses.length, delay: 200 },
    { id: "totalProfessors", value: appState.professors.length, delay: 400 },
    { id: "totalSubjects", value: appState.subjects.length, delay: 600 },
    { id: "totalOffers", value: appState.offers.length, delay: 800 },
    { id: "totalEnrollments", value: appState.enrollments.length, delay: 1000 }
  ];

  // Adicionar animação escalonada aos cards
  stats.forEach((stat, index) => {
    setTimeout(() => {
      const card = document.getElementById(stat.id).closest('.stat-card');
      if (card) {
        card.style.animationDelay = `${index * 0.1}s`;
      }
      animateNumber(stat.id, stat.value, 2000);
    }, stat.delay);
  });
}

function animateNumber(elementId, target, duration = 2000) {
  const element = document.getElementById(elementId);
  if (!element) return;
  
  const startTime = performance.now();
  const startValue = 0;
  
  function updateNumber(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // Função de easing cubic-bezier para suavidade
    const easeOutQuart = 1 - Math.pow(1 - progress, 4);
    const current = Math.floor(startValue + (target - startValue) * easeOutQuart);
    
    element.textContent = current;
    
    if (progress < 1) {
      requestAnimationFrame(updateNumber);
    } else {
      element.textContent = target;
    }
  }
  
  requestAnimationFrame(updateNumber);
}

// Sistema de navegação
function initNavigation() {
  const navItems = document.querySelectorAll(".nav-item")
  navItems.forEach((item) => {
    item.addEventListener("click", function () {
      const view = this.getAttribute("data-view")
      switchView(view)

      navItems.forEach((nav) => nav.classList.remove("active"))
      this.classList.add("active")
    })
  })
}

function switchView(viewName) {
  const views = document.querySelectorAll(".view")
  views.forEach((view) => (view.style.display = "none"))

  const targetView = document.getElementById(viewName + "View")
  if (targetView) {
    targetView.style.display = "block"
    // Definir a seção atual para edição inline
    appState.currentSection = viewName;
    
    // Carregar dados automaticamente para as novas views de relatório
    if (viewName === 'courseStatistics') {
      loadCourseStatisticsReport();
    } else if (viewName === 'offersComplete') {
      loadOffersCompleteReport();
    }
  }
}

// Atualizar estatísticas do dashboard
function updateDashboard() {
  document.getElementById("dashStudents").textContent = appState.students.length
  document.getElementById("dashCourses").textContent = appState.courses.length
  document.getElementById("dashProfessors").textContent = appState.professors.length
  document.getElementById("dashSubjects").textContent = appState.subjects.length
  document.getElementById("dashOffers").textContent = appState.offers.length
  
  // Verificar se o elemento existe antes de tentar acessá-lo
  const dashEnrollmentsElement = document.getElementById("dashEnrollments");
  if (dashEnrollmentsElement) {
    dashEnrollmentsElement.textContent = appState.enrollments.length;
  }
}

// Funções de carregamento de tabelas
function loadStudentsTable() {
  const tbody = document.getElementById("studentsTableBody")
  tbody.innerHTML = ""

  if (appState.students.length === 0) {
    tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 3rem;">Nenhum aluno cadastrado</td></tr>'
    return
  }

  // Ordenar por ID (matrícula) em ordem decrescente
  const sortedStudents = [...appState.students].sort((a, b) => {
    const idA = parseInt(a.matricula || a.id || 0);
    const idB = parseInt(b.matricula || b.id || 0);
    return idB - idA;
  });

  sortedStudents.forEach((student) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${student.matricula || student.id}</td>
      <td>${student.cpf || 'N/A'}</td>
      <td>${student.nome || 'N/A'}</td>
      <td>${student.data_nasc ? formatDate(student.data_nasc) : 'N/A'}</td>
      <td>${student.telefone || 'N/A'}</td>
      <td>${student.email || 'N/A'}</td>
      <td>${student.periodo ? student.periodo + 'º' : 'N/A'}</td>
      <td><span class="status-badge ${student.status_curso ? student.status_curso.toLowerCase() : 'ativo'}">${student.status_curso || 'Ativo'}</span></td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="startInlineEdit('student', ${student.matricula || student.id}, this.closest('tr'))" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteStudent(${student.matricula || student.id})" title="Excluir">🗑️</button>
        </div>
      </td>
    `
    tbody.appendChild(row)
  })
}

function loadCoursesTable() {
  const tbody = document.getElementById("coursesTableBody")
  tbody.innerHTML = ""

  if (appState.courses.length === 0) {
    tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 3rem;">Nenhum curso cadastrado</td></tr>'
    return
  }

  // Ordenar por ID em ordem decrescente
  const sortedCourses = [...appState.courses].sort((a, b) => {
    const idA = parseInt(a.id || 0);
    const idB = parseInt(b.id || 0);
    return idB - idA;
  });

  sortedCourses.forEach((course) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${course.id}</td>
      <td>${course.nome || 'N/A'}</td>
      <td>${course.carga_horaria_total || 'N/A'}h</td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="startInlineEdit('course', ${course.id}, this.closest('tr'))" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteCourse(${course.id})" title="Excluir">🗑️</button>
        </div>
      </td>
    `
    tbody.appendChild(row)
  })
}

function loadProfessorsTable() {
  const tbody = document.getElementById("professorsTableBody")
  tbody.innerHTML = ""

  if (appState.professors.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="8" style="text-align: center; padding: 3rem;">Nenhum professor cadastrado</td></tr>'
    return
  }

  // Ordenar por ID em ordem decrescente
  const sortedProfessors = [...appState.professors].sort((a, b) => {
    const idA = parseInt(a.id_professor || a.id || 0);
    const idB = parseInt(b.id_professor || b.id || 0);
    return idB - idA;
  });

  sortedProfessors.forEach((professor) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${professor.id_professor || professor.id}</td>
      <td>${professor.cpf || 'N/A'}</td>
      <td>${professor.nome || 'N/A'}</td>
      <td>${professor.data_nasc ? formatDate(professor.data_nasc) : 'N/A'}</td>
      <td>${professor.telefone || 'N/A'}</td>
      <td>${professor.email || 'N/A'}</td>
      <td><span class="status-badge ${professor.status ? professor.status.toLowerCase() : 'ativo'}">${professor.status || 'Ativo'}</span></td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="startInlineEdit('professor', ${professor.id_professor || professor.id}, this.closest('tr'))" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteProfessor(${professor.id_professor || professor.id})" title="Excluir">🗑️</button>
        </div>
      </td>
    `
    tbody.appendChild(row)
  })
}

function loadSubjectsTable() {
  const tbody = document.getElementById("subjectsTableBody")
  tbody.innerHTML = ""

  if (appState.subjects.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="6" style="text-align: center; padding: 3rem;">Nenhuma matéria cadastrada</td></tr>'
    return
  }

  // Ordenar por ID da matéria em ordem decrescente
  const sortedSubjects = [...appState.subjects].sort((a, b) => {
    const idA = parseInt(a.id_materia || 0);
    const idB = parseInt(b.id_materia || 0);
    return idB - idA;
  });

  sortedSubjects.forEach((subject) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${subject.id_materia}</td>
      <td>${subject.id_curso}</td>
      <td>${subject.periodo}º</td>
      <td>${subject.nome || 'N/A'}</td>
      <td>${subject.carga_horaria || 'N/A'}h</td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="startInlineEdit('subject', '${subject.id_materia},${subject.id_curso}', this.closest('tr'))" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteSubject(${subject.id_materia}, ${subject.id_curso})" title="Excluir">🗑️</button>
        </div>
      </td>
    `
    tbody.appendChild(row)
  })
}

function loadOffersTable() {
  const tbody = document.getElementById("offersTableBody")
  tbody.innerHTML = ""

  if (appState.offers.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="6" style="text-align: center; padding: 3rem;">Nenhuma oferta cadastrada</td></tr>'
    return
  }

  // Ordenar por ID em ordem decrescente
  const sortedOffers = [...appState.offers].sort((a, b) => {
    const idA = parseInt(a.id || 0);
    const idB = parseInt(b.id || 0);
    return idB - idA;
  });

  sortedOffers.forEach((offer) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${offer.id}</td>
      <td>${offer.ano}</td>
      <td>${offer.semestre}º</td>
      <td data-id="${offer.id_professor}">${offer.professor_nome || '-'} (ID: ${offer.id_professor})</td>
      <td data-id="${offer.id_materia}" data-curso-id="${offer.id_curso}">${offer.materia_nome || '-'} (ID: ${offer.id_materia})</td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="startInlineEdit('offer', ${offer.id}, this.closest('tr'))" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteOffer(${offer.id})" title="Excluir">🗑️</button>
        </div>
      </td>
    `
    tbody.appendChild(row)
  })
}



function loadEnrollmentsTable() {
  const tbody = document.getElementById("enrollmentsTableBody")
  tbody.innerHTML = ""

  if (appState.enrollments.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="5" style="text-align: center; padding: 3rem;">Nenhuma matrícula encontrada</td></tr>'
    return
  }

  appState.enrollments.forEach((enrollment) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${enrollment.matricula}</td>
      <td>${enrollment.id_oferta}</td>
      <td><span class="status-badge ${enrollment.status?.toLowerCase()}">${enrollment.status}</span></td>
      <td>${enrollment.aluno_nome}</td>
      <td>${enrollment.materia_nome}</td>
    `
    tbody.appendChild(row)
  })
}



// Sistema de busca/filtro nas tabelas
function filterTable(tableId, searchValue) {
  const table = document.getElementById(tableId)
  const tbody = table.querySelector("tbody")
  const rows = tbody.getElementsByTagName("tr")
  const filter = searchValue.toLowerCase()

  for (let i = 0; i < rows.length; i++) {
    const row = rows[i]
    const cells = row.getElementsByTagName("td")
    let found = false

    for (let j = 0; j < cells.length; j++) {
      const cell = cells[j]
      if (cell.textContent.toLowerCase().indexOf(filter) > -1) {
        found = true
        break
      }
    }

    row.style.display = found ? "" : "none"
  }
}

// Sistema de relatórios
function generateReport(type) {
  let reportContent = ""

  switch (type) {
    case "students":
      reportContent = `
        📊 RELATÓRIO DE ALUNOS
        
        Total de Alunos: ${appState.students.length}
        Alunos Ativos: ${appState.students.filter((s) => s.status_curso === "Ativo").length}
        Alunos Trancados: ${appState.students.filter((s) => s.status_curso === "Trancado").length}
      `
      break
    case "courses":
      reportContent = `
        📚 RELATÓRIO DE CURSOS
        
        Total de Cursos: ${appState.courses.length}
        Total de Matérias: ${appState.subjects.length}
        Carga Horária Total: ${appState.courses.reduce((sum, c) => sum + c.carga_horaria, 0)}h
      `
      break
    case "professors":
      reportContent = `
        👨‍🏫 RELATÓRIO DE PROFESSORES
        
        Total de Professores: ${appState.professors.length}
        Total de Ofertas: ${appState.offers.length}
      `
      break
    case "dashboard":
      reportContent = `
        📈 DASHBOARD GERAL
        
        Alunos: ${appState.students.length}
        Cursos: ${appState.courses.length}
        Professores: ${appState.professors.length}
        Matérias: ${appState.subjects.length}
        Ofertas: ${appState.offers.length}
        Matrículas: ${appState.enrollments.length}
      `
      break
  }

  alert(reportContent)
  showNotification("Relatório gerado com sucesso!", "success")
}

// Funções utilitárias
function formatDate(dateString) {
  if (!dateString) return "N/A"
  const date = new Date(dateString)
  return date.toLocaleDateString("pt-BR")
}

// Funcionalidades de Edição Inline
let editingRow = null;
let originalRowData = null;

function startInlineEdit(entityType, id, row) {
  // Se já existe uma linha sendo editada, cancelar a edição anterior
  if (editingRow) {
    cancelInlineEdit();
  }

  editingRow = row;
  originalRowData = {};
  
  // Salvar dados originais e converter células para inputs
  const cells = row.querySelectorAll('td:not(:last-child)');
  cells.forEach((cell, index) => {
    const originalValue = cell.textContent.trim();
    originalRowData[index] = originalValue;
    
    // Para subjects, o ID Matéria (index 0) não deve ser editável
    if (entityType === 'subject' && index === 0) {
      return; // Pular a edição do ID Matéria
    }
    
    // Determinar o tipo de input baseado no conteúdo e posição
    let inputType = 'text';
    let inputValue = originalValue;
    
    // Lógica específica para cada tipo de entidade
    if (entityType === 'student') {
      // Estrutura: Matrícula, CPF, Nome, Data Nasc, Telefone, Email, Período, Status, Ações
      if (index === 6) { // Período
        inputValue = originalValue.replace('º', '');
        inputType = 'number';
      } else if (index === 7) { // Status
        const select = document.createElement('select');
        select.innerHTML = `
          <option value="Ativo" ${originalValue === 'Ativo' ? 'selected' : ''}>Ativo</option>
          <option value="Inativo" ${originalValue === 'Inativo' ? 'selected' : ''}>Inativo</option>
          <option value="Trancado" ${originalValue === 'Trancado' ? 'selected' : ''}>Trancado</option>
          <option value="Formado" ${originalValue === 'Formado' ? 'selected' : ''}>Formado</option>
        `;
        cell.innerHTML = '';
        cell.appendChild(select);
        cell.classList.add('editable-cell');
        return;
      } else if (index === 5) { // Email
        inputType = 'email';
      } else if (index === 3) { // Data Nascimento
        inputType = 'date';
        inputValue = originalValue && originalValue !== 'N/A' ? formatDateForInput(originalValue) : '';
      }
    } else if (entityType === 'professor') {
      // Estrutura: ID, CPF, Nome, Data Nasc, Telefone, Email, Status, Ações
      if (index === 6) { // Status do professor
        const select = document.createElement('select');
        select.innerHTML = `
          <option value="Ativo" ${originalValue === 'Ativo' ? 'selected' : ''}>Ativo</option>
          <option value="Inativo" ${originalValue === 'Inativo' ? 'selected' : ''}>Inativo</option>
          <option value="Afastado" ${originalValue === 'Afastado' ? 'selected' : ''}>Afastado</option>
        `;
        cell.innerHTML = '';
        cell.appendChild(select);
        cell.classList.add('editable-cell');
        return;
      } else if (index === 5) { // Email
        inputType = 'email';
      } else if (index === 3) { // Data Nascimento
        inputType = 'date';
        inputValue = originalValue && originalValue !== 'N/A' ? formatDateForInput(originalValue) : '';
      }
    } else if (entityType === 'course') {
      // Estrutura: ID, Nome, Carga Horária, Ações
      if (index === 2) { // Carga Horária
        inputValue = originalValue.replace('h', '');
        inputType = 'number';
      }
    } else if (entityType === 'subject') {
      // Estrutura: ID Matéria, ID Curso, Período, Nome, Carga Horária, Ações
      if (index === 2) { // Período
        inputValue = originalValue.replace('º', '');
        inputType = 'number';
      } else if (index === 4) { // Carga Horária
        inputValue = originalValue.replace('h', '');
        inputType = 'number';
      } else if (index === 1) { // ID Curso
        inputType = 'number';
      }
    } else if (entityType === 'offer') {
      // Estrutura: ID, Ano, Semestre, Professor, Matéria, Ações
      if (index === 1) { // Ano
        inputType = 'number';
      } else if (index === 2) { // Semestre
        inputValue = originalValue.replace('º', '');
        const select = document.createElement('select');
        select.innerHTML = `
          <option value="1" ${inputValue === '1' ? 'selected' : ''}>1º</option>
          <option value="2" ${inputValue === '2' ? 'selected' : ''}>2º</option>
        `;
        cell.innerHTML = '';
        cell.appendChild(select);
        cell.classList.add('editable-cell');
        return;
      } else if (index === 3) { // Professor - editar ID do professor
        const professorId = cell.getAttribute('data-id');
        inputType = 'number';
        inputValue = professorId || '';
        
        const input = document.createElement('input');
        input.type = inputType;
        input.value = inputValue;
        input.placeholder = 'ID do Professor';
        
        cell.innerHTML = '';
        cell.appendChild(input);
        cell.classList.add('editable-cell');
        return;
      } else if (index === 4) { // Matéria - editar ID da matéria e curso
        const materiaId = cell.getAttribute('data-id');
        const cursoId = cell.getAttribute('data-curso-id');
        
        const container = document.createElement('div');
        container.style.display = 'flex';
        container.style.gap = '5px';
        
        const materiaInput = document.createElement('input');
        materiaInput.type = 'number';
        materiaInput.value = materiaId || '';
        materiaInput.placeholder = 'ID Matéria';
        materiaInput.style.flex = '1';
        
        const cursoInput = document.createElement('input');
        cursoInput.type = 'number';
        cursoInput.value = cursoId || '';
        cursoInput.placeholder = 'ID Curso';
        cursoInput.style.flex = '1';
        
        container.appendChild(materiaInput);
        container.appendChild(cursoInput);
        
        cell.innerHTML = '';
        cell.appendChild(container);
        cell.classList.add('editable-cell');
        return;
      }
    }
    
    // Criar input para campos editáveis (exceto primeiro campo que geralmente é ID)
    if (index > 0) {
      const input = document.createElement('input');
      input.type = inputType;
      input.value = inputValue;
      
      // Para inputs de data, adicionar configurações especiais
      if (inputType === 'date') {
        input.setAttribute('lang', 'pt-BR');
        input.setAttribute('data-date-format', 'DD/MM/YYYY');
        
        // Adicionar listeners para debug e correção
        input.addEventListener('focus', function() {
          console.log('Input date focado - valor original:', originalValue, 'valor input:', this.value);
        });
        
        input.addEventListener('change', function() {
          console.log('Input date alterado - novo valor:', this.value);
        });
      }
      
      cell.innerHTML = '';
      cell.appendChild(input);
      cell.classList.add('editable-cell');
    }
  });

  // Trocar botões de ação por botões de salvar/cancelar
  const actionsCell = row.querySelector('td:last-child');
  actionsCell.innerHTML = `
    <div class="edit-actions">
      <button class="save-btn" onclick="saveInlineEdit('${entityType}', '${id}')">Salvar</button>
      <button class="cancel-btn" onclick="cancelInlineEdit()">Cancelar</button>
    </div>
  `;
  
  row.classList.add('editing-row');
}

function cancelInlineEdit() {
  if (!editingRow || !originalRowData) return;

  const cells = editingRow.querySelectorAll('td:not(:last-child)');
  cells.forEach((cell, index) => {
    cell.innerHTML = originalRowData[index] || '';
    cell.classList.remove('editable-cell');
  });

  // Restaurar botões de ação originais
  const actionsCell = editingRow.querySelector('td:last-child');
  const entityType = getCurrentEntityType();
  const id = getEntityIdFromRow(editingRow);
  
  // Mapear os tipos de entidade para as funções de delete corretas
  const deleteFunction = {
    'student': 'deleteStudent',
    'professor': 'deleteProfessor',
    'course': 'deleteCourse',
    'subject': 'deleteSubject',
    'offer': 'deleteOffer'
  }[entityType] || `delete${capitalizeFirst(entityType)}`;

  actionsCell.innerHTML = `
    <div class="table-actions">
      <button class="icon-btn edit" onclick="startInlineEdit('${entityType}', ${id}, this.closest('tr'))" title="Editar">✏️</button>
      <button class="icon-btn delete" onclick="${deleteFunction}(${id})" title="Excluir">🗑️</button>
    </div>
  `;

  editingRow.classList.remove('editing-row');
  editingRow = null;
  originalRowData = null;
}

async function saveInlineEdit(entityType, id) {
  if (!editingRow) return;

  try {
    const cells = editingRow.querySelectorAll('td:not(:last-child)');
    const updatedData = {};

    // Extrair dados dos inputs baseado no tipo de entidade
    if (entityType === 'student') {
      const inputs = editingRow.querySelectorAll('input, select');
      console.log('Dados do student - inputs encontrados:', inputs.length); // Debug
      
      // Estrutura: ID(0), CPF(1), Nome(2), Data_Nasc(3), Telefone(4), Email(5), Período(6), Status(7), Ações(8)
      updatedData.cpf = inputs[0]?.value || '';   // 1ª input - CPF
      updatedData.nome = inputs[1]?.value || '';  // 2ª input - Nome
      updatedData.telefone = inputs[3]?.value || ''; // 4ª input - Telefone  
      updatedData.email = inputs[4]?.value || '';  // 5ª input - Email
      updatedData.periodo = inputs[5]?.value || ''; // 6ª input - Período
      updatedData.status_curso = inputs[6]?.value || ''; // 7ª input - Status (select)
      
      if (inputs[2]?.value) { // 3ª input - Data Nascimento se fornecida
        const dateValue = inputs[2].value;
        const formattedDate = convertDateToUserFormat(dateValue);
        updatedData.data_nasc = formattedDate;
        console.log('Data do student convertida:', formattedDate); // Debug
      }
      
      console.log('Dados finais do student:', updatedData); // Debug
      
    } else if (entityType === 'professor') {
      const inputs = editingRow.querySelectorAll('input, select');
      console.log('Dados do professor - inputs encontrados:', inputs.length); // Debug
      
      // Estrutura: ID(0), CPF(1), Nome(2), Data_Nasc(3), Telefone(4), Email(5), Status(6), Ações(7)
      updatedData.cpf = inputs[0]?.value || '';   // 1ª input - CPF
      updatedData.nome = inputs[1]?.value || '';  // 2ª input - Nome
      updatedData.telefone = inputs[3]?.value || ''; // 4ª input - Telefone
      updatedData.email = inputs[4]?.value || '';  // 5ª input - Email
      updatedData.status = inputs[5]?.value || ''; // 6ª input - Status (select)
      
      if (inputs[2]?.value) { // 3ª input - Data Nascimento se fornecida
        const dateValue = inputs[2].value;
        const formattedDate = convertDateToUserFormat(dateValue);
        updatedData.data_nasc = formattedDate;
        console.log('Data do professor convertida:', formattedDate); // Debug
      }
      
      console.log('Dados finais do professor:', updatedData); // Debug
    } else if (entityType === 'course') {
      const inputs = editingRow.querySelectorAll('input');
      updatedData.nome = inputs[0]?.value || '';  // 2ª célula - Nome
      updatedData.carga_horaria_total = inputs[1]?.value || ''; // 3ª célula - Carga Horária
    } else if (entityType === 'subject') {
      const inputs = editingRow.querySelectorAll('input');
      console.log('Dados do subject - inputs encontrados:', inputs.length); // Debug
      
      // Estrutura: ID Matéria (não editável), ID Curso, Período, Nome, Carga Horária
      // Como ID Matéria não é editável, temos 4 inputs para os outros campos
      updatedData.id_curso = inputs[0]?.value || '';  // 1º input - ID Curso
      updatedData.periodo = inputs[1]?.value || '';   // 2º input - Período  
      updatedData.nome = inputs[2]?.value || '';      // 3º input - Nome
      updatedData.carga_horaria = inputs[3]?.value || ''; // 4º input - Carga Horária
      
      console.log('Dados finais do subject:', updatedData); // Debug
    } else if (entityType === 'offer') {
      const inputs = editingRow.querySelectorAll('input, select');
      console.log('Dados da oferta - inputs encontrados:', inputs.length); // Debug
      
      // Estrutura: ID(0), Ano(1), Semestre(2), Professor ID(3), Matéria/Curso IDs(4), Ações(5)
      updatedData.ano = inputs[0]?.value || '';  // 1ª input - Ano
      updatedData.semestre = inputs[1]?.value || ''; // 2ª input/select - Semestre
      updatedData.id_professor = inputs[2]?.value || ''; // 3ª input - ID Professor
      updatedData.id_materia = inputs[3]?.value || ''; // 4ª input - ID Matéria
      updatedData.id_curso = inputs[4]?.value || ''; // 5ª input - ID Curso
      
      console.log('Dados finais da oferta:', updatedData); // Debug
    }

    // Chamar a função CRUD apropriada
    if (entityType === 'student') {
      await updateStudent(id, updatedData);
    } else if (entityType === 'professor') {
      await updateProfessor(id, updatedData);
    } else if (entityType === 'course') {
      await updateCourse(id, updatedData);
    } else if (entityType === 'subject') {
      await updateSubject(id, updatedData);
    } else if (entityType === 'offer') {
      await updateOffer(id, updatedData);
    }

    // Limpar estado de edição
    editingRow = null;
    originalRowData = null;
    
    showNotification(`${capitalizeFirst(entityType)} atualizado com sucesso!`, 'success');
    
  } catch (error) {
    console.error('Erro ao salvar edição inline:', error);
    showNotification(`Erro ao atualizar ${entityType}: ${error.message}`, 'error');
    cancelInlineEdit();
  }
}

function getCurrentEntityType() {
  const currentSection = appState.currentSection;
  if (currentSection === 'students') return 'student';
  if (currentSection === 'professors') return 'professor';
  if (currentSection === 'courses') return 'course';
  if (currentSection === 'subjects') return 'subject';
  if (currentSection === 'offers') return 'offer';
  return 'unknown';
}

function getEntityIdFromRow(row) {
  const firstCell = row.querySelector('td');
  return firstCell ? firstCell.textContent.trim() : null;
}

function capitalizeFirst(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function formatDateForInput(dateStr) {
  console.log('formatDateForInput input:', dateStr); // Debug
  
  if (!dateStr || dateStr === 'N/A' || dateStr.trim() === '') return '';
  
  // Se já está no formato YYYY-MM-DD, validar e retornar
  if (dateStr.match(/^\d{4}-\d{1,2}-\d{1,2}$/)) {
    const parts = dateStr.split('-');
    const [year, month, day] = parts;
    const dayNum = parseInt(day, 10);
    const monthNum = parseInt(month, 10);
    const yearNum = parseInt(year, 10);
    
    if (dayNum >= 1 && dayNum <= 31 && monthNum >= 1 && monthNum <= 12 && yearNum > 1900) {
      const result = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
      console.log('Data ISO válida, formatada:', result); // Debug
      return result;
    }
  }
  
  // Converter data no formato brasileiro/americano para ISO
  if (dateStr.includes('/')) {
    const parts = dateStr.split('/');
    if (parts.length === 3) {
      const [first, second, year] = parts;
      const firstNum = parseInt(first, 10);
      const secondNum = parseInt(second, 10);
      const yearNum = parseInt(year, 10);
      
      // Detectar se é DD/MM/YYYY ou MM/DD/YYYY baseado nos valores
      let day, month;
      
      if (firstNum > 12) {
        // Definitivamente DD/MM/YYYY
        day = firstNum;
        month = secondNum;
        console.log('Detectado formato DD/MM/YYYY'); // Debug
      } else if (secondNum > 12) {
        // Definitivamente MM/DD/YYYY (formato americano incorreto)
        day = secondNum;
        month = firstNum;
        console.log('Detectado formato MM/DD/YYYY (corrigindo)'); // Debug
      } else {
        // Ambíguo - assumir DD/MM/YYYY (formato brasileiro preferido)
        day = firstNum;
        month = secondNum;
        console.log('Formato ambíguo, assumindo DD/MM/YYYY'); // Debug
      }
      
      // Validar os valores
      if (day >= 1 && day <= 31 && month >= 1 && month <= 12 && yearNum > 1900) {
        const result = `${yearNum}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
        console.log('Data convertida para ISO:', result); // Debug
        return result;
      }
    }
  }
  
  console.log('Data não pôde ser convertida, retornando vazio'); // Debug
  return '';
}

function convertDateToUserFormat(dateStr) {
  console.log('convertDateToUserFormat input:', dateStr); // Debug
  
  if (!dateStr || dateStr === 'N/A' || dateStr.trim() === '') return '';
  
  // Se já está no formato DD/MM/YYYY, retornar como está
  if (dateStr.match(/^\d{1,2}\/\d{1,2}\/\d{4}$/)) {
    console.log('Data já em formato brasileiro:', dateStr); // Debug
    return dateStr;
  }
  
  // Converter data do formato ISO (YYYY-MM-DD) para formato brasileiro (DD/MM/YYYY)
  if (dateStr.includes('-')) {
    const parts = dateStr.split('-');
    if (parts.length === 3) {
      const [year, month, day] = parts;
      
      // Validar os componentes da data
      const yearNum = parseInt(year, 10);
      const monthNum = parseInt(month, 10);
      const dayNum = parseInt(day, 10);
      
      if (yearNum > 1900 && monthNum >= 1 && monthNum <= 12 && dayNum >= 1 && dayNum <= 31) {
        const result = `${dayNum.toString().padStart(2, '0')}/${monthNum.toString().padStart(2, '0')}/${yearNum}`;
        console.log('Data convertida de ISO para brasileiro:', result); // Debug
        return result;
      }
    }
  }
  
  console.log('Data não pôde ser convertida, retornando vazio'); // Debug
  return '';
}

// ===== FUNÇÕES DE LOADING =====
let loadingOverlay = null;

function showLoading(message = 'Carregando...') {
  // Remove loading anterior se existir
  hideLoading();
  
  // Criar overlay de loading
  loadingOverlay = document.createElement('div');
  loadingOverlay.id = 'loadingOverlay';
  loadingOverlay.innerHTML = `
    <div class="loading-backdrop">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <p class="loading-message">${message}</p>
      </div>
    </div>
  `;
  
  // Adicionar estilos inline para garantir que funcionem
  loadingOverlay.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 9999;
    pointer-events: none;
  `;
  
  const backdrop = loadingOverlay.querySelector('.loading-backdrop');
  if (backdrop) {
    backdrop.style.cssText = `
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 100%;
      background: rgba(255, 255, 255, 0.8);
      backdrop-filter: blur(2px);
    `;
  }
  
  const content = loadingOverlay.querySelector('.loading-content');
  if (content) {
    content.style.cssText = `
      text-align: center;
      padding: 2rem;
      background: white;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      border: 1px solid #e5e7eb;
    `;
  }
  
  const spinner = loadingOverlay.querySelector('.loading-spinner');
  if (spinner) {
    spinner.style.cssText = `
      width: 40px;
      height: 40px;
      border: 4px solid #f3f4f6;
      border-top: 4px solid #3b82f6;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 1rem;
    `;
  }
  
  const messageEl = loadingOverlay.querySelector('.loading-message');
  if (messageEl) {
    messageEl.style.cssText = `
      margin: 0;
      color: #374151;
      font-size: 14px;
      font-weight: 500;
    `;
  }
  
  // Adicionar animação CSS se não existir
  if (!document.querySelector('#loadingStyles')) {
    const styleSheet = document.createElement('style');
    styleSheet.id = 'loadingStyles';
    styleSheet.textContent = `
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    `;
    document.head.appendChild(styleSheet);
  }
  
  document.body.appendChild(loadingOverlay);
  
  console.log('🔄 Loading mostrado:', message);
}

function hideLoading() {
  if (loadingOverlay && loadingOverlay.parentNode) {
    loadingOverlay.parentNode.removeChild(loadingOverlay);
    loadingOverlay = null;
    console.log('✅ Loading ocultado');
  }
}
