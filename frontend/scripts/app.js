// Configuração da API
const API_BASE_URL = 'http://localhost:5000/api';

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

// Funções utilitárias para API
async function apiRequest(endpoint, options = {}) {
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const config = { ...defaultOptions, ...options };
  
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    showNotification(`Erro na API: ${error.message}`, 'error');
    throw error;
  }
}

// Inicialização da aplicação
document.addEventListener("DOMContentLoaded", () => {
  loadAllData()

  // Animar estatísticas da splash screen
  setTimeout(() => {
    animateSplashStats()
  }, 500)

  // Mostrar aplicação principal após splash
  setTimeout(() => {
    document.getElementById("appContainer").classList.add("active")
  }, 4500)

  // Inicializar navegação
  initNavigation()
})

// Funções de carregamento de dados da API
async function loadAllData() {
  try {
    showNotification('Carregando dados...', 'info');
    
    // Carregar todos os dados em paralelo
    await Promise.all([
      loadStudentsFromAPI(),
      loadCoursesFromAPI(),
      loadProfessorsFromAPI(),
      loadSubjectsFromAPI(),
      loadOffersFromAPI(),
      loadEvaluationsFromAPI(),
      loadEnrollmentsFromAPI(),
      loadGradesFromAPI()
    ]);

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
    showNotification('Dados carregados com sucesso!', 'success');
  } catch (error) {
    console.error('Erro ao carregar dados:', error);
    showNotification('Erro ao carregar dados da API', 'error');
  }
}

async function loadStudentsFromAPI() {
  try {
    const data = await apiRequest('/students');
    appState.students = data || [];
  } catch (error) {
    console.error('Erro ao carregar alunos:', error);
    appState.students = [];
  }
}

async function loadCoursesFromAPI() {
  try {
    const data = await apiRequest('/courses');
    appState.courses = data || [];
  } catch (error) {
    console.error('Erro ao carregar cursos:', error);
    appState.courses = [];
  }
}

async function loadProfessorsFromAPI() {
  try {
    const data = await apiRequest('/professors');
    appState.professors = data || [];
  } catch (error) {
    console.error('Erro ao carregar professores:', error);
    appState.professors = [];
  }
}

async function loadSubjectsFromAPI() {
  try {
    const data = await apiRequest('/subjects');
    appState.subjects = data || [];
  } catch (error) {
    console.error('Erro ao carregar matérias:', error);
    appState.subjects = [];
  }
}

async function loadOffersFromAPI() {
  try {
    const data = await apiRequest('/offers');
    appState.offers = data || [];
  } catch (error) {
    console.error('Erro ao carregar ofertas:', error);
    appState.offers = [];
  }
}

async function loadEvaluationsFromAPI() {
  try {
    const data = await apiRequest('/evaluations');
    appState.evaluations = data || [];
  } catch (error) {
    console.error('Erro ao carregar avaliações:', error);
    appState.evaluations = [];
  }
}

async function loadEnrollmentsFromAPI() {
  try {
    const data = await apiRequest('/enrollments');
    appState.enrollments = data || [];
  } catch (error) {
    console.error('Erro ao carregar matrículas:', error);
    appState.enrollments = [];
  }
}

async function loadGradesFromAPI() {
  try {
    const data = await apiRequest('/grades');
    appState.grades = data || [];
  } catch (error) {
    console.error('Erro ao carregar notas:', error);
    appState.grades = [];
  }
}

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
  document.getElementById("dashStudents").textContent = appState.students.length
  document.getElementById("dashCourses").textContent = appState.courses.length
  document.getElementById("dashProfessors").textContent = appState.professors.length
  document.getElementById("dashSubjects").textContent = appState.subjects.length
  document.getElementById("dashOffers").textContent = appState.offers.length
  document.getElementById("dashEvaluations").textContent = appState.evaluations.length
  document.getElementById("dashEnrollments").textContent = appState.enrollments.length
  document.getElementById("dashGrades").textContent = appState.grades.length
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

  if (appState.professors.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="6" style="text-align: center; padding: 3rem;">Nenhum professor cadastrado</td></tr>'
    return
  }

  appState.professors.forEach((professor) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${professor.id}</td>
      <td>${professor.nome}</td>
      <td>${professor.cpf}</td>
      <td>${professor.email}</td>
      <td>${professor.telefone}</td>
      <td>
        <div class="table-actions">
          <button class="icon-btn edit" onclick="editProfessor(${professor.id})" title="Editar">✏️</button>
          <button class="icon-btn delete" onclick="deleteProfessor(${professor.id})" title="Excluir">🗑️</button>
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

  if (appState.offers.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="6" style="text-align: center; padding: 3rem;">Nenhuma oferta cadastrada</td></tr>'
    return
  }

  appState.offers.forEach((offer) => {
    const row = document.createElement("tr")
    row.innerHTML = `
      <td>${offer.id}</td>
      <td>${offer.ano}</td>
      <td>${offer.semestre}º</td>
      <td>${offer.professor_nome}</td>
      <td>${offer.materia_nome}</td>
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

// Funções de exclusão com API
async function deleteStudent(id) {
  if (!confirm("Tem certeza que deseja excluir este aluno?")) return

  try {
    await apiRequest(`/students/${id}`, { method: 'DELETE' });
    await loadStudentsFromAPI();
    loadStudentsTable();
    updateDashboard();
    showNotification("Aluno excluído com sucesso!", "success");
  } catch (error) {
    console.error('Erro ao excluir aluno:', error);
  }
}

async function deleteCourse(id) {
  if (!confirm("Tem certeza que deseja excluir este curso?")) return

  try {
    await apiRequest(`/courses/${id}`, { method: 'DELETE' });
    await loadCoursesFromAPI();
    loadCoursesTable();
    updateDashboard();
    showNotification("Curso excluído com sucesso!", "success");
  } catch (error) {
    console.error('Erro ao excluir curso:', error);
  }
}

async function deleteProfessor(id) {
  if (!confirm("Tem certeza que deseja excluir este professor?")) return

  try {
    await apiRequest(`/professors/${id}`, { method: 'DELETE' });
    await loadProfessorsFromAPI();
    loadProfessorsTable();
    updateDashboard();
    showNotification("Professor excluído com sucesso!", "success");
  } catch (error) {
    console.error('Erro ao excluir professor:', error);
  }
}

async function deleteSubject(idMateria, idCurso) {
  if (!confirm("Tem certeza que deseja excluir esta matéria?")) return

  try {
    await apiRequest(`/subjects/${idMateria}/${idCurso}`, { method: 'DELETE' });
    await loadSubjectsFromAPI();
    loadSubjectsTable();
    updateDashboard();
    showNotification("Matéria excluída com sucesso!", "success");
  } catch (error) {
    console.error('Erro ao excluir matéria:', error);
  }
}

async function deleteOffer(id) {
  if (!confirm("Tem certeza que deseja excluir esta oferta?")) return

  try {
    await apiRequest(`/offers/${id}`, { method: 'DELETE' });
    await loadOffersFromAPI();
    loadOffersTable();
    updateDashboard();
    showNotification("Oferta excluída com sucesso!", "success");
  } catch (error) {
    console.error('Erro ao excluir oferta:', error);
  }
}

async function deleteEvaluation(id) {
  if (!confirm("Tem certeza que deseja excluir esta avaliação?")) return

  try {
    await apiRequest(`/evaluations/${id}`, { method: 'DELETE' });
    await loadEvaluationsFromAPI();
    loadEvaluationsTable();
    updateDashboard();
    showNotification("Avaliação excluída com sucesso!", "success");
  } catch (error) {
    console.error('Erro ao excluir avaliação:', error);
  }
}

async function deleteEnrollment(idAluno, idOferta) {
  if (!confirm("Tem certeza que deseja excluir esta matrícula?")) return

  try {
    await apiRequest(`/enrollments/${idAluno}/${idOferta}`, { method: 'DELETE' });
    await loadEnrollmentsFromAPI();
    loadEnrollmentsTable();
    updateDashboard();
    showNotification("Matrícula excluída com sucesso!", "success");
  } catch (error) {
    console.error('Erro ao excluir matrícula:', error);
  }
}

async function deleteGrade(idAvaliacao, idAluno) {
  if (!confirm("Tem certeza que deseja excluir esta nota?")) return

  try {
    await apiRequest(`/grades/${idAvaliacao}/${idAluno}`, { method: 'DELETE' });
    await loadGradesFromAPI();
    loadGradesTable();
    updateDashboard();
    showNotification("Nota excluída com sucesso!", "success");
  } catch (error) {
    console.error('Erro ao excluir nota:', error);
  }
}

// Funções de edição com API
async function editStudent(id) {
  try {
    const student = appState.students.find(s => s.id === id || s.matricula === id);
    if (!student) {
      showNotification("Aluno não encontrado!", "error");
      return;
    }

    const formData = await showEditForm('Editar Aluno', [
      { name: 'matricula', label: 'Matrícula', type: 'text', value: student.matricula, required: true },
      { name: 'nome', label: 'Nome', type: 'text', value: student.nome, required: true },
      { name: 'cpf', label: 'CPF', type: 'text', value: student.cpf },
      { name: 'email', label: 'Email', type: 'email', value: student.email, required: true },
      { name: 'telefone', label: 'Telefone', type: 'text', value: student.telefone },
      { name: 'data_nasc', label: 'Data Nascimento', type: 'date', value: student.data_nasc },
      { name: 'periodo', label: 'Período', type: 'number', value: student.periodo, required: true },
      { name: 'course_id', label: 'ID do Curso', type: 'number', value: student.course_id, required: true },
      { name: 'status_curso', label: 'Status', type: 'select', value: student.status_curso, options: ['Ativo', 'Trancado', 'Formado'] }
    ]);

    if (formData) {
      await apiRequest(`/students/${id}`, {
        method: 'PUT',
        body: JSON.stringify(formData)
      });
      
      await loadStudentsFromAPI();
      loadStudentsTable();
      updateDashboard();
      showNotification("Aluno atualizado com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao editar aluno:', error);
  }
}

async function editCourse(id) {
  try {
    const course = appState.courses.find(c => c.id === id);
    if (!course) {
      showNotification("Curso não encontrado!", "error");
      return;
    }

    const formData = await showEditForm('Editar Curso', [
      { name: 'nome', label: 'Nome', type: 'text', value: course.nome, required: true },
      { name: 'codigo', label: 'Código', type: 'text', value: course.codigo, required: true },
      { name: 'carga_horaria', label: 'Carga Horária', type: 'number', value: course.carga_horaria, required: true }
    ]);

    if (formData) {
      await apiRequest(`/courses/${id}`, {
        method: 'PUT',
        body: JSON.stringify(formData)
      });
      
      await loadCoursesFromAPI();
      loadCoursesTable();
      updateDashboard();
      showNotification("Curso atualizado com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao editar curso:', error);
  }
}

async function editProfessor(id) {
  try {
    const professor = appState.professors.find(p => p.id === id);
    if (!professor) {
      showNotification("Professor não encontrado!", "error");
      return;
    }

    const formData = await showEditForm('Editar Professor', [
      { name: 'nome', label: 'Nome', type: 'text', value: professor.nome, required: true },
      { name: 'cpf', label: 'CPF', type: 'text', value: professor.cpf, required: true },
      { name: 'email', label: 'Email', type: 'email', value: professor.email, required: true },
      { name: 'telefone', label: 'Telefone', type: 'text', value: professor.telefone }
    ]);

    if (formData) {
      await apiRequest(`/professors/${id}`, {
        method: 'PUT',
        body: JSON.stringify(formData)
      });
      
      await loadProfessorsFromAPI();
      loadProfessorsTable();
      updateDashboard();
      showNotification("Professor atualizado com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao editar professor:', error);
  }
}

async function editSubject(idMateria, idCurso) {
  try {
    const subject = appState.subjects.find(s => s.id_materia === idMateria && s.id_curso === idCurso);
    if (!subject) {
      showNotification("Matéria não encontrada!", "error");
      return;
    }

    const formData = await showEditForm('Editar Matéria', [
      { name: 'nome', label: 'Nome', type: 'text', value: subject.nome, required: true },
      { name: 'carga_horaria', label: 'Carga Horária', type: 'number', value: subject.carga_horaria, required: true }
    ]);

    if (formData) {
      await apiRequest(`/subjects/${idMateria}/${idCurso}`, {
        method: 'PUT',
        body: JSON.stringify(formData)
      });
      
      await loadSubjectsFromAPI();
      loadSubjectsTable();
      updateDashboard();
      showNotification("Matéria atualizada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao editar matéria:', error);
  }
}

async function editOffer(id) {
  try {
    const offer = appState.offers.find(o => o.id === id);
    if (!offer) {
      showNotification("Oferta não encontrada!", "error");
      return;
    }

    const formData = await showEditForm('Editar Oferta', [
      { name: 'ano', label: 'Ano', type: 'number', value: offer.ano, required: true },
      { name: 'semestre', label: 'Semestre', type: 'number', value: offer.semestre, required: true },
      { name: 'id_professor', label: 'ID Professor', type: 'number', value: offer.id_professor, required: true },
      { name: 'id_materia', label: 'ID Matéria', type: 'number', value: offer.id_materia, required: true },
      { name: 'id_curso', label: 'ID Curso', type: 'number', value: offer.id_curso, required: true }
    ]);

    if (formData) {
      await apiRequest(`/offers/${id}`, {
        method: 'PUT',
        body: JSON.stringify(formData)
      });
      
      await loadOffersFromAPI();
      loadOffersTable();
      updateDashboard();
      showNotification("Oferta atualizada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao editar oferta:', error);
  }
}

async function editEvaluation(id) {
  try {
    const evaluation = appState.evaluations.find(e => e.id === id);
    if (!evaluation) {
      showNotification("Avaliação não encontrada!", "error");
      return;
    }

    const formData = await showEditForm('Editar Avaliação', [
      { name: 'id_oferta', label: 'ID Oferta', type: 'number', value: evaluation.id_oferta, required: true },
      { name: 'tipo', label: 'Tipo', type: 'select', value: evaluation.tipo, options: ['Prova', 'Trabalho', 'Seminário', 'Projeto'], required: true },
      { name: 'peso', label: 'Peso (0-1)', type: 'number', step: '0.1', value: evaluation.peso, required: true },
      { name: 'data_avaliacao', label: 'Data da Avaliação', type: 'date', value: evaluation.data_avaliacao }
    ]);

    if (formData) {
      await apiRequest(`/evaluations/${id}`, {
        method: 'PUT',
        body: JSON.stringify(formData)
      });
      
      await loadEvaluationsFromAPI();
      loadEvaluationsTable();
      updateDashboard();
      showNotification("Avaliação atualizada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao editar avaliação:', error);
  }
}

async function editEnrollment(idAluno, idOferta) {
  try {
    const enrollment = appState.enrollments.find(e => e.id_aluno === idAluno && e.id_oferta === idOferta);
    if (!enrollment) {
      showNotification("Matrícula não encontrada!", "error");
      return;
    }

    const formData = await showEditForm('Editar Matrícula', [
      { name: 'status', label: 'Status', type: 'select', value: enrollment.status, options: ['Matriculado', 'Aprovado', 'Reprovado', 'Trancado'], required: true },
      { name: 'media_final', label: 'Média Final', type: 'number', step: '0.1', value: enrollment.media_final }
    ]);

    if (formData) {
      await apiRequest(`/enrollments/${idAluno}/${idOferta}`, {
        method: 'PUT',
        body: JSON.stringify(formData)
      });
      
      await loadEnrollmentsFromAPI();
      loadEnrollmentsTable();
      updateDashboard();
      showNotification("Matrícula atualizada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao editar matrícula:', error);
  }
}

async function editGrade(idAvaliacao, idAluno) {
  try {
    const grade = appState.grades.find(g => g.id_avaliacao === idAvaliacao && g.id_aluno === idAluno);
    if (!grade) {
      showNotification("Nota não encontrada!", "error");
      return;
    }

    const formData = await showEditForm('Editar Nota', [
      { name: 'nota', label: 'Nota (0-10)', type: 'number', step: '0.1', min: '0', max: '10', value: grade.nota, required: true }
    ]);

    if (formData) {
      await apiRequest(`/grades/${idAvaliacao}/${idAluno}`, {
        method: 'PUT',
        body: JSON.stringify(formData)
      });
      
      await loadGradesFromAPI();
      loadGradesTable();
      updateDashboard();
      showNotification("Nota atualizada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao editar nota:', error);
  }
}

// Funções de criação (add) com API
async function addStudent() {
  try {
    const formData = await showEditForm('Adicionar Aluno', [
      { name: 'matricula', label: 'Matrícula', type: 'text', required: true },
      { name: 'nome', label: 'Nome', type: 'text', required: true },
      { name: 'cpf', label: 'CPF', type: 'text' },
      { name: 'email', label: 'Email', type: 'email', required: true },
      { name: 'telefone', label: 'Telefone', type: 'text' },
      { name: 'data_nasc', label: 'Data Nascimento', type: 'date' },
      { name: 'periodo', label: 'Período', type: 'number', required: true },
      { name: 'course_id', label: 'ID do Curso', type: 'number', required: true },
      { name: 'status_curso', label: 'Status', type: 'select', options: ['Ativo', 'Trancado', 'Formado'], value: 'Ativo' }
    ]);

    if (formData) {
      await apiRequest('/students', {
        method: 'POST',
        body: JSON.stringify(formData)
      });
      
      await loadStudentsFromAPI();
      loadStudentsTable();
      updateDashboard();
      showNotification("Aluno criado com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao criar aluno:', error);
  }
}

async function addCourse() {
  try {
    const formData = await showEditForm('Adicionar Curso', [
      { name: 'nome', label: 'Nome', type: 'text', required: true },
      { name: 'codigo', label: 'Código', type: 'text', required: true },
      { name: 'carga_horaria', label: 'Carga Horária', type: 'number', required: true }
    ]);

    if (formData) {
      await apiRequest('/courses', {
        method: 'POST',
        body: JSON.stringify(formData)
      });
      
      await loadCoursesFromAPI();
      loadCoursesTable();
      updateDashboard();
      showNotification("Curso criado com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao criar curso:', error);
  }
}

async function addProfessor() {
  try {
    const formData = await showEditForm('Adicionar Professor', [
      { name: 'nome', label: 'Nome', type: 'text', required: true },
      { name: 'cpf', label: 'CPF', type: 'text', required: true },
      { name: 'email', label: 'Email', type: 'email', required: true },
      { name: 'telefone', label: 'Telefone', type: 'text' }
    ]);

    if (formData) {
      await apiRequest('/professors', {
        method: 'POST',
        body: JSON.stringify(formData)
      });
      
      await loadProfessorsFromAPI();
      loadProfessorsTable();
      updateDashboard();
      showNotification("Professor criado com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao criar professor:', error);
  }
}

async function addSubject() {
  try {
    const formData = await showEditForm('Adicionar Matéria', [
      { name: 'id_materia', label: 'ID da Matéria', type: 'number', required: true },
      { name: 'id_curso', label: 'ID do Curso', type: 'number', required: true },
      { name: 'nome', label: 'Nome', type: 'text', required: true },
      { name: 'carga_horaria', label: 'Carga Horária', type: 'number', required: true }
    ]);

    if (formData) {
      await apiRequest('/subjects', {
        method: 'POST',
        body: JSON.stringify(formData)
      });
      
      await loadSubjectsFromAPI();
      loadSubjectsTable();
      updateDashboard();
      showNotification("Matéria criada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao criar matéria:', error);
  }
}

async function addOffer() {
  try {
    const formData = await showEditForm('Adicionar Oferta', [
      { name: 'ano', label: 'Ano', type: 'number', required: true },
      { name: 'semestre', label: 'Semestre', type: 'number', required: true },
      { name: 'id_professor', label: 'ID Professor', type: 'number', required: true },
      { name: 'id_materia', label: 'ID Matéria', type: 'number', required: true },
      { name: 'id_curso', label: 'ID Curso', type: 'number', required: true }
    ]);

    if (formData) {
      await apiRequest('/offers', {
        method: 'POST',
        body: JSON.stringify(formData)
      });
      
      await loadOffersFromAPI();
      loadOffersTable();
      updateDashboard();
      showNotification("Oferta criada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao criar oferta:', error);
  }
}

async function addEvaluation() {
  try {
    const formData = await showEditForm('Adicionar Avaliação', [
      { name: 'id_oferta', label: 'ID Oferta', type: 'number', required: true },
      { name: 'tipo', label: 'Tipo', type: 'select', options: ['Prova', 'Trabalho', 'Seminário', 'Projeto'], required: true },
      { name: 'peso', label: 'Peso (0-1)', type: 'number', step: '0.1', required: true },
      { name: 'data_avaliacao', label: 'Data da Avaliação', type: 'date' }
    ]);

    if (formData) {
      await apiRequest('/evaluations', {
        method: 'POST',
        body: JSON.stringify(formData)
      });
      
      await loadEvaluationsFromAPI();
      loadEvaluationsTable();
      updateDashboard();
      showNotification("Avaliação criada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao criar avaliação:', error);
  }
}

async function addEnrollment() {
  try {
    const formData = await showEditForm('Adicionar Matrícula', [
      { name: 'id_aluno', label: 'ID/Matrícula do Aluno', type: 'text', required: true },
      { name: 'id_oferta', label: 'ID da Oferta', type: 'number', required: true },
      { name: 'status', label: 'Status', type: 'select', options: ['Matriculado', 'Aprovado', 'Reprovado', 'Trancado'], value: 'Matriculado' },
      { name: 'media_final', label: 'Média Final', type: 'number', step: '0.1' }
    ]);

    if (formData) {
      await apiRequest('/enrollments', {
        method: 'POST',
        body: JSON.stringify(formData)
      });
      
      await loadEnrollmentsFromAPI();
      loadEnrollmentsTable();
      updateDashboard();
      showNotification("Matrícula criada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao criar matrícula:', error);
  }
}

async function addGrade() {
  try {
    const formData = await showEditForm('Adicionar Nota', [
      { name: 'id_avaliacao', label: 'ID da Avaliação', type: 'number', required: true },
      { name: 'id_aluno', label: 'ID/Matrícula do Aluno', type: 'text', required: true },
      { name: 'nota', label: 'Nota (0-10)', type: 'number', step: '0.1', min: '0', max: '10', required: true }
    ]);

    if (formData) {
      await apiRequest('/grades', {
        method: 'POST',
        body: JSON.stringify(formData)
      });
      
      await loadGradesFromAPI();
      loadGradesTable();
      updateDashboard();
      showNotification("Nota adicionada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao adicionar nota:', error);
  }
}

// Função auxiliar para mostrar formulários de edição/criação
function showEditForm(title, fields) {
  return new Promise((resolve) => {
    // Esta função será implementada junto com o sistema de modais
    // Por enquanto, vamos usar um prompt simples como fallback
    const result = {};
    let valid = true;
    
    for (const field of fields) {
      if (field.type === 'select') {
        const options = field.options.map((opt, idx) => `${idx + 1}: ${opt}`).join('\n');
        const input = prompt(`${title}\n${field.label}:\nOpções:\n${options}\nEscolha um número:`, field.value || '');
        if (input === null) {
          valid = false;
          break;
        }
        const optionIndex = parseInt(input) - 1;
        if (optionIndex >= 0 && optionIndex < field.options.length) {
          result[field.name] = field.options[optionIndex];
        } else {
          result[field.name] = input;
        }
      } else {
        const input = prompt(`${title}\n${field.label}:`, field.value || '');
        if (input === null) {
          valid = false;
          break;
        }
        if (field.required && !input.trim()) {
          alert(`Campo ${field.label} é obrigatório!`);
          valid = false;
          break;
        }
        result[field.name] = input;
      }
    }
    
    resolve(valid ? result : null);
  });
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

// Atualizar todos os dados
async function refreshAllData() {
  showNotification("Atualizando dados...", "info");
  await loadAllData();
  showNotification("Dados atualizados com sucesso!", "success");
}

// Funções utilitárias
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
    max-width: 400px;
  `
  notification.textContent = message
  document.body.appendChild(notification)

  setTimeout(() => {
    notification.style.animation = "slideOut 0.3s ease"
    setTimeout(() => notification.remove(), 300)
  }, 3000)
}
