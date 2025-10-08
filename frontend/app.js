const API_BASE_URL = "http://localhost:5000/api"

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

document.addEventListener("DOMContentLoaded", async () => {
  console.log("[v0] Initializing application...")

  await loadAllDataFromAPI()

  // Animate splash screen stats
  setTimeout(() => {
    animateSplashStats()
  }, 500)

  // Show main app after splash
  setTimeout(() => {
    document.getElementById("appContainer").classList.add("active")
  }, 4500)

  // Initialize navigation
  initNavigation()
})

async function loadAllDataFromAPI() {
  console.log("[v0] Loading data from API...")

  try {
    await Promise.all([
      fetchStudents(),
      fetchCourses(),
      fetchProfessors(),
      fetchSubjects(),
      fetchOffers(),
      fetchEvaluations(),
      fetchEnrollments(),
      fetchGrades(),
    ])

    updateDashboard()
    console.log("[v0] All data loaded successfully")
  } catch (error) {
    console.error("[v0] Error loading data:", error)
    showNotification("Erro ao carregar dados. Verifique se o backend está rodando.", "error")
  }
}

async function fetchStudents() {
  try {
    const response = await fetch(`${API_BASE_URL}/students`)
    if (response.ok) {
      appState.students = await response.json()
      loadStudentsTable()
    }
  } catch (error) {
    console.error("[v0] Error fetching students:", error)
    appState.students = []
  }
}

async function fetchCourses() {
  try {
    const response = await fetch(`${API_BASE_URL}/courses`)
    if (response.ok) {
      appState.courses = await response.json()
      loadCoursesTable()
    }
  } catch (error) {
    console.error("[v0] Error fetching courses:", error)
    appState.courses = []
  }
}

async function fetchProfessors() {
  try {
    const response = await fetch(`${API_BASE_URL}/professors`)
    if (response.ok) {
      appState.professors = await response.json()
      loadProfessorsTable()
    }
  } catch (error) {
    console.error("[v0] Error fetching professors:", error)
    appState.professors = []
  }
}

async function fetchSubjects() {
  try {
    const response = await fetch(`${API_BASE_URL}/subjects`)
    if (response.ok) {
      appState.subjects = await response.json()
      loadSubjectsTable()
    }
  } catch (error) {
    console.error("[v0] Error fetching subjects:", error)
    appState.subjects = []
  }
}

async function fetchOffers() {
  try {
    const response = await fetch(`${API_BASE_URL}/offers`)
    if (response.ok) {
      appState.offers = await response.json()
      loadOffersTable()
    }
  } catch (error) {
    console.error("[v0] Error fetching offers:", error)
    appState.offers = []
  }
}

async function fetchEvaluations() {
  try {
    const response = await fetch(`${API_BASE_URL}/evaluations`)
    if (response.ok) {
      appState.evaluations = await response.json()
      loadEvaluationsTable()
    }
  } catch (error) {
    console.error("[v0] Error fetching evaluations:", error)
    appState.evaluations = []
  }
}

async function fetchEnrollments() {
  try {
    const response = await fetch(`${API_BASE_URL}/enrollments`)
    if (response.ok) {
      appState.enrollments = await response.json()
      loadEnrollmentsTable()
    }
  } catch (error) {
    console.error("[v0] Error fetching enrollments:", error)
    appState.enrollments = []
  }
}

async function fetchGrades() {
  try {
    const response = await fetch(`${API_BASE_URL}/student-evaluations`)
    if (response.ok) {
      appState.grades = await response.json()
      loadGradesTable()
    }
  } catch (error) {
    console.error("[v0] Error fetching grades:", error)
    appState.grades = []
  }
}

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

// Navigation
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

// Update dashboard statistics
function updateDashboard() {
  document.getElementById("dashStudents").textContent = appState.students.length
  document.getElementById("dashCourses").textContent = appState.courses.length
  document.getElementById("dashProfessors").textContent = appState.professors.length
  document.getElementById("dashSubjects").textContent = appState.subjects.length
  document.getElementById("dashOffers").textContent = appState.offers.length
  document.getElementById("dashEvaluations").textContent = appState.evaluations.length
  document.getElementById("dashEnrollments").textContent = appState.enrollments.length
  document.getElementById("dashGrades").textContent = appState.grades.length
}

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
      <td>${student.id || student.id_aluno}</td>
      <td>${student.matricula || "N/A"}</td>
      <td>${student.nome}</td>
      <td>${student.cpf || "N/A"}</td>
      <td>${student.email || "N/A"}</td>
      <td>${student.periodo || "N/A"}</td>
      <td><span class="status-badge ${student.status_curso || "Ativo"}">${student.status_curso || "Ativo"}</span></td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="editStudent(${student.id || student.id_aluno})" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteStudent(${student.id || student.id_aluno})" title="Excluir">🗑️</button>
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
      <td>${course.id || course.id_curso}</td>
      <td>${course.nome || course.name}</td>
      <td>${course.codigo || course.code || "N/A"}</td>
      <td>${course.carga_horaria || course.workload || "N/A"}h</td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="editCourse(${course.id || course.id_curso})" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteCourse(${course.id || course.id_curso})" title="Excluir">🗑️</button>
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
      '<tr><td colspan="6" style="text-align: center; padding: 3rem;">Nenhum professor cadastrado</td></tr>'
    return
  }

  appState.professors.forEach((professor) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${professor.id || professor.id_professor}</td>
      <td>${professor.nome}</td>
      <td>${professor.cpf || "N/A"}</td>
      <td>${professor.email || "N/A"}</td>
      <td>${professor.telefone || "N/A"}</td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="editProfessor(${professor.id || professor.id_professor})" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteProfessor(${professor.id || professor.id_professor})" title="Excluir">🗑️</button>
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
      <td>${subject.carga_horaria || "N/A"}h</td>
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

  if (appState.offers.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="6" style="text-align: center; padding: 3rem;">Nenhuma oferta cadastrada</td></tr>'
    return
  }

  appState.offers.forEach((offer) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${offer.id || offer.id_oferta}</td>
      <td>${offer.ano}</td>
      <td>${offer.semestre}</td>
      <td>${offer.professor_nome || "N/A"}</td>
      <td>${offer.materia_nome || "N/A"}</td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="editOffer(${offer.id || offer.id_oferta})" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteOffer(${offer.id || offer.id_oferta})" title="Excluir">🗑️</button>
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
      <td>${evaluation.id || evaluation.id_avaliacao}</td>
      <td>${evaluation.id_oferta}</td>
      <td>${evaluation.tipo || "N/A"}</td>
      <td>${evaluation.peso || "N/A"}</td>
      <td>${evaluation.data_avaliacao ? formatDate(evaluation.data_avaliacao) : "N/A"}</td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="editEvaluation(${evaluation.id || evaluation.id_avaliacao})" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteEvaluation(${evaluation.id || evaluation.id_avaliacao})" title="Excluir">🗑️</button>
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
      <td>${enrollment.aluno_nome || enrollment.id_aluno}</td>
      <td>${enrollment.oferta_info || enrollment.id_oferta}</td>
      <td><span class="status-badge ${enrollment.status || "Ativo"}">${enrollment.status || "Ativo"}</span></td>
      <td>${enrollment.media_final || "N/A"}</td>
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
      <td>${grade.id_avaliacao}</td>
      <td>${grade.aluno_nome || grade.id_aluno}</td>
      <td>${grade.nota || "N/A"}</td>
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

async function deleteStudent(id) {
  if (!confirm("Tem certeza que deseja excluir este aluno?")) return

  try {
    const response = await fetch(`${API_BASE_URL}/students/${id}`, {
      method: "DELETE",
    })

    if (response.ok) {
      showNotification("Aluno excluído com sucesso!", "success")
      await fetchStudents()
      updateDashboard()
    } else {
      const error = await response.json()
      showNotification(error.error || "Erro ao excluir aluno", "error")
    }
  } catch (error) {
    console.error("[v0] Error deleting student:", error)
    showNotification("Erro ao excluir aluno", "error")
  }
}

async function deleteCourse(id) {
  if (!confirm("Tem certeza que deseja excluir este curso?")) return

  try {
    const response = await fetch(`${API_BASE_URL}/courses/${id}`, {
      method: "DELETE",
    })

    if (response.ok) {
      showNotification("Curso excluído com sucesso!", "success")
      await fetchCourses()
      updateDashboard()
    } else {
      const error = await response.json()
      showNotification(error.error || "Erro ao excluir curso", "error")
    }
  } catch (error) {
    console.error("[v0] Error deleting course:", error)
    showNotification("Erro ao excluir curso", "error")
  }
}

async function deleteProfessor(id) {
  if (!confirm("Tem certeza que deseja excluir este professor?")) return

  try {
    const response = await fetch(`${API_BASE_URL}/professors/${id}`, {
      method: "DELETE",
    })

    if (response.ok) {
      showNotification("Professor excluído com sucesso!", "success")
      await fetchProfessors()
      updateDashboard()
    } else {
      const error = await response.json()
      showNotification(error.error || "Erro ao excluir professor", "error")
    }
  } catch (error) {
    console.error("[v0] Error deleting professor:", error)
    showNotification("Erro ao excluir professor", "error")
  }
}

async function deleteSubject(idMateria, idCurso) {
  if (!confirm("Tem certeza que deseja excluir esta matéria?")) return

  try {
    const response = await fetch(`${API_BASE_URL}/subjects/${idMateria}/${idCurso}`, {
      method: "DELETE",
    })

    if (response.ok) {
      showNotification("Matéria excluída com sucesso!", "success")
      await fetchSubjects()
      updateDashboard()
    } else {
      const error = await response.json()
      showNotification(error.error || "Erro ao excluir matéria", "error")
    }
  } catch (error) {
    console.error("[v0] Error deleting subject:", error)
    showNotification("Erro ao excluir matéria", "error")
  }
}

async function deleteOffer(id) {
  if (!confirm("Tem certeza que deseja excluir esta oferta?")) return

  try {
    const response = await fetch(`${API_BASE_URL}/offers/${id}`, {
      method: "DELETE",
    })

    if (response.ok) {
      showNotification("Oferta excluída com sucesso!", "success")
      await fetchOffers()
      updateDashboard()
    } else {
      const error = await response.json()
      showNotification(error.error || "Erro ao excluir oferta", "error")
    }
  } catch (error) {
    console.error("[v0] Error deleting offer:", error)
    showNotification("Erro ao excluir oferta", "error")
  }
}

async function deleteEvaluation(id) {
  if (!confirm("Tem certeza que deseja excluir esta avaliação?")) return

  try {
    const response = await fetch(`${API_BASE_URL}/evaluations/${id}`, {
      method: "DELETE",
    })

    if (response.ok) {
      showNotification("Avaliação excluída com sucesso!", "success")
      await fetchEvaluations()
      updateDashboard()
    } else {
      const error = await response.json()
      showNotification(error.error || "Erro ao excluir avaliação", "error")
    }
  } catch (error) {
    console.error("[v0] Error deleting evaluation:", error)
    showNotification("Erro ao excluir avaliação", "error")
  }
}

async function deleteEnrollment(idAluno, idOferta) {
  if (!confirm("Tem certeza que deseja excluir esta matrícula?")) return

  try {
    const response = await fetch(`${API_BASE_URL}/enrollments/${idAluno}/${idOferta}`, {
      method: "DELETE",
    })

    if (response.ok) {
      showNotification("Matrícula excluída com sucesso!", "success")
      await fetchEnrollments()
      updateDashboard()
    } else {
      const error = await response.json()
      showNotification(error.error || "Erro ao excluir matrícula", "error")
    }
  } catch (error) {
    console.error("[v0] Error deleting enrollment:", error)
    showNotification("Erro ao excluir matrícula", "error")
  }
}

async function deleteGrade(idAvaliacao, idAluno) {
  if (!confirm("Tem certeza que deseja excluir esta nota?")) return

  try {
    const response = await fetch(`${API_BASE_URL}/student-evaluations/${idAvaliacao}/${idAluno}`, {
      method: "DELETE",
    })

    if (response.ok) {
      showNotification("Nota excluída com sucesso!", "success")
      await fetchGrades()
      updateDashboard()
    } else {
      const error = await response.json()
      showNotification(error.error || "Erro ao excluir nota", "error")
    }
  } catch (error) {
    console.error("[v0] Error deleting grade:", error)
    showNotification("Erro ao excluir nota", "error")
  }
}

// Edit functions (placeholder - would open modal with pre-filled data)
function editStudent(id) {
  showNotification("Função de edição em desenvolvimento", "info")
}

function editCourse(id) {
  showNotification("Função de edição em desenvolvimento", "info")
}

function editProfessor(id) {
  showNotification("Função de edição em desenvolvimento", "info")
}

function editSubject(idMateria, idCurso) {
  showNotification("Função de edição em desenvolvimento", "info")
}

function editOffer(id) {
  showNotification("Função de edição em desenvolvimento", "info")
}

function editEvaluation(id) {
  showNotification("Função de edição em desenvolvimento", "info")
}

function editEnrollment(idAluno, idOferta) {
  showNotification("Função de edição em desenvolvimento", "info")
}

function editGrade(idAvaliacao, idAluno) {
  showNotification("Função de edição em desenvolvimento", "info")
}

// Add modal functions (placeholder)
function openAddModal(type) {
  showNotification(`Função de adicionar ${type} em desenvolvimento`, "info")
}

// Search/Filter function
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

// Reports functions
async function generateReport(type) {
  showNotification("Gerando relatório...", "info")

  try {
    let reportData = ""

    switch (type) {
      case "students":
        reportData = `Relatório de Alunos\n\nTotal: ${appState.students.length}`
        break
      case "courses":
        reportData = `Relatório de Cursos\n\nTotal: ${appState.courses.length}`
        break
      case "professors":
        reportData = `Relatório de Professores\n\nTotal: ${appState.professors.length}`
        break
      case "dashboard":
        const response = await fetch(`${API_BASE_URL}/reports/dashboard`)
        if (response.ok) {
          const data = await response.json()
          reportData = `Dashboard Geral\n\n${JSON.stringify(data, null, 2)}`
        }
        break
    }

    alert(reportData)
    showNotification("Relatório gerado com sucesso!", "success")
  } catch (error) {
    console.error("[v0] Error generating report:", error)
    showNotification("Erro ao gerar relatório", "error")
  }
}

// Refresh all data
async function refreshAllData() {
  showNotification("Atualizando dados...", "info")
  await loadAllDataFromAPI()
  showNotification("Dados atualizados com sucesso!", "success")
}

// Utility functions
function formatDate(dateString) {
  if (!dateString) return "N/A"
  const date = new Date(dateString)
  return date.toLocaleDateString("pt-BR")
}

function showNotification(message, type) {
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
  `
  notification.textContent = message
  document.body.appendChild(notification)

  setTimeout(() => {
    notification.style.animation = "slideOut 0.3s ease"
    setTimeout(() => notification.remove(), 300)
  }, 3000)
}
