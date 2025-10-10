// Função showNotification (deve estar no escopo global)
function showNotification(message, type = 'info') {
  const notification = document.createElement("div")
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 1rem 1.5rem;
    background: ${type === "success" ? "var(--color-success)" : type === "error" ? "var(--color-error)" : "var(--color-primary)"};
    color: white;
    border-radius: var(--radius-md);
    z-index: 10000;
    animation: slideIn 0.3s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    max-width: 400px;
  `
  notification.textContent = message
  document.body.appendChild(notification)

  setTimeout(() => {
    notification.style.animation = "slideOut 0.3s ease"
    setTimeout(() => notification.remove(), 300)
  }, 3000)
}

// Estado da aplicação
const appState = {
  students: [],
  courses: [],
  professors: [],
  subjects: [],
  offers: [],
  evaluations: [],
  enrollments: [],
  grades: [],
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
      appState.evaluations = dataManager.state.evaluations;
      appState.enrollments = dataManager.state.enrollments;
      appState.grades = dataManager.state.studentEvaluations;
      
      // Carregar todas as tabelas
      loadStudentsTable();
      loadCoursesTable();
      loadProfessorsTable();
      loadSubjectsTable();
      loadOffersTable();
      loadEvaluationsTable();
      loadEnrollmentsTable();
      loadGradesTable();
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



// Animação dos números da splash screen
function animateSplashStats() {
  animateNumber("totalStudents", appState.students.length)
  animateNumber("totalCourses", appState.courses.length)
  animateNumber("totalProfessors", appState.professors.length)
  animateNumber("totalSubjects", appState.subjects.length)
  animateNumber("totalOffers", appState.offers.length)
  animateNumber("totalEvaluations", appState.evaluations.length)
  animateNumber("totalEnrollments", appState.enrollments.length)
  animateNumber("totalGrades", appState.grades.length)
}

function animateNumber(elementId, target) {
  const element = document.getElementById(elementId)
  let current = 0
  const increment = target / 50
  const timer = setInterval(() => {
    current += increment
    if (current >= target) {
      element.textContent = target
      clearInterval(timer)
    } else {
      element.textContent = Math.floor(current)
    }
  }, 30)
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
  }
}

// Atualizar estatísticas do dashboard
function updateDashboard() {
  document.getElementById("dashStudents").textContent = dataManager.students.length
  document.getElementById("dashCourses").textContent = dataManager.courses.length
  document.getElementById("dashProfessors").textContent = dataManager.professors.length
  document.getElementById("dashSubjects").textContent = dataManager.subjects.length
  document.getElementById("dashOffers").textContent = dataManager.offers.length
  document.getElementById("dashEvaluations").textContent = dataManager.evaluations.length
  document.getElementById("dashEnrollments").textContent = dataManager.enrollments.length
  document.getElementById("dashGrades").textContent = dataManager.grades.length
}

// Funções de carregamento de tabelas
function loadStudentsTable() {
  const tbody = document.getElementById("studentsTableBody")
  tbody.innerHTML = ""

  if (appState.students.length === 0) {
    tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 3rem;">Nenhum aluno cadastrado</td></tr>'
    return
  }

  appState.students.forEach((student) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${student.id}</td>
      <td>${student.matricula}</td>
      <td>${student.nome}</td>
      <td>${student.cpf}</td>
      <td>${student.email}</td>
      <td>${student.periodo}º</td>
      <td><span class="status-badge ${student.status_curso}">${student.status_curso}</span></td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="editStudent(${student.id})" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteStudent(${student.id})" title="Excluir">🗑️</button>
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
    tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 3rem;">Nenhum curso cadastrado</td></tr>'
    return
  }

  appState.courses.forEach((course) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${course.id}</td>
      <td>${course.nome}</td>
      <td>${course.codigo}</td>
      <td>${course.carga_horaria}h</td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="editCourse(${course.id})" title="Editar">✏️</button>
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

  if (dataManager.professors.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="8" style="text-align: center; padding: 3rem;">Nenhum professor cadastrado</td></tr>'
    return
  }

  dataManager.professors.forEach((professor) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${professor.id_professor}</td>
      <td>${professor.cpf}</td>
      <td>${professor.nome}</td>
      <td>${professor.data_nasc ? new Date(professor.data_nasc).toLocaleDateString('pt-BR') : '-'}</td>
      <td>${professor.telefone || '-'}</td>
      <td>${professor.email}</td>
      <td><span class="status-badge ${professor.status?.toLowerCase()}">${professor.status}</span></td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="editProfessor(${professor.id_professor})" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteProfessor(${professor.id_professor})" title="Excluir">🗑️</button>
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
      '<tr><td colspan="5" style="text-align: center; padding: 3rem;">Nenhuma matéria cadastrada</td></tr>'
    return
  }

  appState.subjects.forEach((subject) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${subject.id_materia}</td>
      <td>${subject.id_curso}</td>
      <td>${subject.nome}</td>
      <td>${subject.carga_horaria}h</td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="editSubject(${subject.id_materia}, ${subject.id_curso})" title="Editar">✏️</button>
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

  if (dataManager.offers.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="6" style="text-align: center; padding: 3rem;">Nenhuma oferta cadastrada</td></tr>'
    return
  }

  dataManager.offers.forEach((offer) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${offer.id}</td>
      <td>${offer.ano}</td>
      <td>${offer.semestre}º</td>
      <td>${offer.professor_nome || '-'}</td>
      <td>${offer.materia_nome || '-'}</td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="editOffer(${offer.id})" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteOffer(${offer.id})" title="Excluir">🗑️</button>
        </div>
      </td>
    `
    tbody.appendChild(row)
  })
}

function loadEvaluationsTable() {
  const tbody = document.getElementById("evaluationsTableBody")
  tbody.innerHTML = ""

  if (appState.evaluations.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="6" style="text-align: center; padding: 3rem;">Nenhuma avaliação cadastrada</td></tr>'
    return
  }

  appState.evaluations.forEach((evaluation) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${evaluation.id}</td>
      <td>Oferta #${evaluation.id_oferta}</td>
      <td>${evaluation.tipo}</td>
      <td>${(evaluation.peso * 100).toFixed(0)}%</td>
      <td>${formatDate(evaluation.data_avaliacao)}</td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="editEvaluation(${evaluation.id})" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteEvaluation(${evaluation.id})" title="Excluir">🗑️</button>
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
      '<tr><td colspan="5" style="text-align: center; padding: 3rem;">Nenhuma matrícula cadastrada</td></tr>'
    return
  }

  appState.enrollments.forEach((enrollment) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${enrollment.aluno_nome}</td>
      <td>${enrollment.oferta_info}</td>
      <td><span class="status-badge ${enrollment.status}">${enrollment.status}</span></td>
      <td>${enrollment.media_final ? enrollment.media_final.toFixed(1) : "N/A"}</td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="editEnrollment(${enrollment.id_aluno}, ${enrollment.id_oferta})" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteEnrollment(${enrollment.id_aluno}, ${enrollment.id_oferta})" title="Excluir">🗑️</button>
        </div>
      </td>
    `
    tbody.appendChild(row)
  })
}

function loadGradesTable() {
  const tbody = document.getElementById("gradesTableBody")
  tbody.innerHTML = ""

  if (appState.grades.length === 0) {
    tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 3rem;">Nenhuma nota cadastrada</td></tr>'
    return
  }

  appState.grades.forEach((grade) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>Avaliação #${grade.id_avaliacao}</td>
      <td>${grade.aluno_nome}</td>
      <td><strong>${grade.nota.toFixed(1)}</strong></td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="editGrade(${grade.id_avaliacao}, ${grade.id_aluno})" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteGrade(${grade.id_avaliacao}, ${grade.id_aluno})" title="Excluir">🗑️</button>
        </div>
      </td>
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
        Avaliações: ${appState.evaluations.length}
        Matrículas: ${appState.enrollments.length}
        Notas: ${appState.grades.length}
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
