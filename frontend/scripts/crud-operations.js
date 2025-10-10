// crud-operations.js - Operações CRUD para todas as entidades

// ===== STUDENTS CRUD =====
async function addStudent() {
  try {
    const formData = await showEditForm('Adicionar Aluno', [
      { name: 'nome', label: 'Nome', type: 'text', required: true },
      { name: 'cpf', label: 'CPF', type: 'text', required: true },
      { name: 'email', label: 'Email', type: 'email', required: true },
      { name: 'telefone', label: 'Telefone', type: 'text' },
      { name: 'data_nasc', label: 'Data Nascimento', type: 'date' },
      { name: 'periodo', label: 'Período', type: 'number', required: true },
      { name: 'id_curso', label: 'ID do Curso', type: 'number', required: true },
      { name: 'status_curso', label: 'Status', type: 'select', options: ['Ativo', 'Trancado', 'Formado'], value: 'Ativo', required: true }
    ]);

    if (formData) {
      await apiService.createStudent(formData);
      await dataManager.loadStudents();
      loadStudentsTable();
      updateDashboard();
      showNotification("Aluno criado com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao criar aluno:', error);
  }
}

async function editStudent(matricula) {
  try {
    const student = appState.students.find(s => s.matricula === matricula);
    if (!student) {
      showNotification("Aluno não encontrado!", "error");
      return;
    }

    const formData = await showEditForm('Editar Aluno', [
      { name: 'matricula', label: 'Matrícula', type: 'text', value: student.matricula, required: true },
      { name: 'nome', label: 'Nome', type: 'text', value: student.nome, required: true },
      { name: 'cpf', label: 'CPF', type: 'text', value: student.cpf, required: true },
      { name: 'email', label: 'Email', type: 'email', value: student.email, required: true },
      { name: 'telefone', label: 'Telefone', type: 'text', value: student.telefone },
      { name: 'data_nasc', label: 'Data Nascimento', type: 'date', value: student.data_nasc },
      { name: 'periodo', label: 'Período', type: 'number', value: student.periodo, required: true },
      { name: 'id_curso', label: 'ID do Curso', type: 'number', value: student.id_curso, required: true },
      { name: 'status_curso', label: 'Status', type: 'select', value: student.status_curso, options: ['Ativo', 'Trancado', 'Formado'], required: true }
    ]);

    if (formData) {
      await apiService.updateStudent(matricula, formData);
      await dataManager.loadStudents();
      loadStudentsTable();
      updateDashboard();
      showNotification("Aluno atualizado com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao editar aluno:', error);
  }
}

async function deleteStudent(matricula) {
  if (!confirm("Tem certeza que deseja excluir este aluno?")) return;

  try {
    await apiService.deleteStudent(matricula);
    await dataManager.loadStudents();
    loadStudentsTable();
    updateDashboard();
    showNotification("Aluno excluído com sucesso!", "success");
  } catch (error) {
    console.error('Erro ao excluir aluno:', error);
  }
}

// ===== COURSES CRUD =====
async function addCourse() {
  try {
    const formData = await showEditForm('Adicionar Curso', [
      { name: 'nome', label: 'Nome', type: 'text', required: true },
      { name: 'carga_horaria_total', label: 'Carga Horária Total', type: 'number', required: true }
    ]);

    if (formData) {
      await apiService.createCourse(formData);
      await dataManager.loadCourses();
      loadCoursesTable();
      updateDashboard();
      showNotification("Curso criado com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao criar curso:', error);
    showNotification(`Erro ao criar curso: ${error.message}`, "error");
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
      { name: 'carga_horaria_total', label: 'Carga Horária Total', type: 'number', value: course.carga_horaria_total, required: true }
    ]);

    if (formData) {
      await apiService.updateCourse(id, formData);
      await dataManager.loadCourses();
      loadCoursesTable();
      updateDashboard();
      showNotification("Curso atualizado com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao editar curso:', error);
    showNotification(`Erro ao editar curso: ${error.message}`, "error");
  }
}

async function deleteCourse(id) {
  if (!confirm("Tem certeza que deseja excluir este curso?")) return;

  try {
    await apiService.deleteCourse(id);
    await dataManager.loadCourses();
    loadCoursesTable();
    updateDashboard();
    showNotification("Curso excluído com sucesso!", "success");
  } catch (error) {
    console.error('Erro ao excluir curso:', error);
    showNotification(`Erro ao excluir curso: ${error.message}`, "error");
  }
}

// ===== PROFESSORS CRUD =====
async function addProfessor() {
  try {
    const formData = await showEditForm('Adicionar Professor', [
      { name: 'nome', label: 'Nome', type: 'text', required: true },
      { name: 'cpf', label: 'CPF', type: 'text', required: true },
      { name: 'email', label: 'Email', type: 'email', required: true },
      { name: 'status', label: 'Status', type: 'select', options: ['Ativo', 'Inativo', 'Afastado'], value: 'Ativo', required: true },
      { name: 'data_nasc', label: 'Data Nascimento', type: 'date' },
      { name: 'telefone', label: 'Telefone', type: 'text' }
    ]);

    if (formData) {
      await apiService.createProfessor(formData);
      await dataManager.loadProfessors();
      loadProfessorsTable();
      updateDashboard();
      showNotification("Professor criado com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao criar professor:', error);
    showNotification(`Erro ao criar professor: ${error.message}`, "error");
  }
}

async function editProfessor(id) {
  try {
    const professor = appState.professors.find(p => p.id_professor == id);
    if (!professor) {
      showNotification("Professor não encontrado!", "error");
      return;
    }

    const formData = await showEditForm('Editar Professor', [
      { name: 'nome', label: 'Nome', type: 'text', value: professor.nome, required: true },
      { name: 'cpf', label: 'CPF', type: 'text', value: professor.cpf, required: true },
      { name: 'email', label: 'Email', type: 'email', value: professor.email, required: true },
      { name: 'status', label: 'Status', type: 'select', options: ['Ativo', 'Inativo', 'Afastado'], value: professor.status, required: true },
      { name: 'data_nasc', label: 'Data Nascimento', type: 'date', value: professor.data_nasc ? professor.data_nasc.split('T')[0] : '' },
      { name: 'telefone', label: 'Telefone', type: 'text', value: professor.telefone }
    ]);

    if (formData) {
      await apiService.updateProfessor(id, formData);
      await dataManager.loadProfessors();
      loadProfessorsTable();
      updateDashboard();
      showNotification("Professor atualizado com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao editar professor:', error);
    showNotification(`Erro ao editar professor: ${error.message}`, "error");
  }
}

async function deleteProfessor(id) {
  if (!confirm("Tem certeza que deseja excluir este professor?")) return;

  try {
    await apiService.deleteProfessor(id);
    await dataManager.loadProfessors();
    loadProfessorsTable();
    updateDashboard();
    showNotification("Professor excluído com sucesso!", "success");
  } catch (error) {
    console.error('Erro ao excluir professor:', error);
    showNotification(`Erro ao excluir professor: ${error.message}`, "error");
  }
}

// ===== SUBJECTS CRUD =====
async function addSubject() {
  try {
    const formData = await showEditForm('Adicionar Matéria', [
      { name: 'id_curso', label: 'ID do Curso', type: 'number', required: true },
      { name: 'periodo', label: 'Período', type: 'number', required: true },
      { name: 'nome', label: 'Nome', type: 'text', required: true },
      { name: 'carga_horaria', label: 'Carga Horária', type: 'number', required: true }
    ]);

    if (formData) {
      await apiService.createSubject(formData);
      await dataManager.loadSubjects();
      loadSubjectsTable();
      updateDashboard();
      showNotification("Matéria criada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao criar matéria:', error);
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
      await apiService.updateSubject(idMateria, idCurso, formData);
      await dataManager.loadSubjects();
      loadSubjectsTable();
      updateDashboard();
      showNotification("Matéria atualizada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao editar matéria:', error);
  }
}

async function deleteSubject(idMateria, idCurso) {
  if (!confirm("Tem certeza que deseja excluir esta matéria?")) return;

  try {
    await apiService.deleteSubject(idMateria, idCurso);
    await dataManager.loadSubjects();
    loadSubjectsTable();
    updateDashboard();
    showNotification("Matéria excluída com sucesso!", "success");
  } catch (error) {
    console.error('Erro ao excluir matéria:', error);
  }
}

// ===== OFFERS CRUD =====
async function addOffer() {
  try {
    const formData = await showEditForm('Adicionar Oferta', [
      { name: 'ano', label: 'Ano', type: 'number', required: true },
      { name: 'semestre', label: 'Semestre', type: 'select', options: [1, 2], required: true },
      { name: 'id_professor', label: 'ID Professor', type: 'number', required: true },
      { name: 'id_materia', label: 'ID Matéria', type: 'number', required: true },
      { name: 'id_curso', label: 'ID Curso', type: 'number', required: true }
    ]);

    if (formData) {
      await apiService.createOffer(formData);
      await dataManager.loadOffers();
      loadOffersTable();
      updateDashboard();
      showNotification("Oferta criada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao criar oferta:', error);
    showNotification(`Erro ao criar oferta: ${error.message}`, "error");
  }
}

async function editOffer(id) {
  try {
    const offer = dataManager.offers.find(o => o.id === id);
    if (!offer) {
      showNotification("Oferta não encontrada!", "error");
      return;
    }

    const formData = await showEditForm('Editar Oferta', [
      { name: 'ano', label: 'Ano', type: 'number', value: offer.ano, required: true },
      { name: 'semestre', label: 'Semestre', type: 'select', options: [1, 2], value: offer.semestre, required: true },
      { name: 'id_professor', label: 'ID Professor', type: 'number', value: offer.id_professor, required: true },
      { name: 'id_materia', label: 'ID Matéria', type: 'number', value: offer.id_materia, required: true },
      { name: 'id_curso', label: 'ID Curso', type: 'number', value: offer.id_curso, required: true }
    ]);

    if (formData) {
      await apiService.updateOffer(id, formData);
      await dataManager.loadOffers();
      loadOffersTable();
      updateDashboard();
      showNotification("Oferta atualizada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao editar oferta:', error);
    showNotification(`Erro ao editar oferta: ${error.message}`, "error");
  }
}

async function deleteOffer(id) {
  if (!confirm("Tem certeza que deseja excluir esta oferta?")) return;

  try {
    await apiService.deleteOffer(id);
    await dataManager.loadOffers();
    loadOffersTable();
    updateDashboard();
    showNotification("Oferta excluída com sucesso!", "success");
  } catch (error) {
    console.error('Erro ao excluir oferta:', error);
    showNotification(`Erro ao excluir oferta: ${error.message}`, "error");
  }
}

// ===== EVALUATIONS CRUD =====
async function addEvaluation() {
  try {
    const formData = await showEditForm('Adicionar Avaliação', [
      { name: 'id_oferta', label: 'ID Oferta', type: 'number', required: true },
      { name: 'tipo', label: 'Tipo', type: 'select', options: ['Prova', 'Trabalho', 'Seminário', 'Projeto'], required: true },
      { name: 'peso', label: 'Peso (0-1)', type: 'number', step: '0.1', required: true },
      { name: 'data_avaliacao', label: 'Data da Avaliação', type: 'date' }
    ]);

    if (formData) {
      await apiService.createEvaluation(formData);
      await dataManager.loadEvaluations();
      loadEvaluationsTable();
      updateDashboard();
      showNotification("Avaliação criada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao criar avaliação:', error);
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
      await apiService.updateEvaluation(id, formData);
      await dataManager.loadEvaluations();
      loadEvaluationsTable();
      updateDashboard();
      showNotification("Avaliação atualizada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao editar avaliação:', error);
  }
}

async function deleteEvaluation(id) {
  if (!confirm("Tem certeza que deseja excluir esta avaliação?")) return;

  try {
    await apiService.deleteEvaluation(id);
    await dataManager.loadEvaluations();
    loadEvaluationsTable();
    updateDashboard();
    showNotification("Avaliação excluída com sucesso!", "success");
  } catch (error) {
    console.error('Erro ao excluir avaliação:', error);
  }
}

// ===== ENROLLMENTS CRUD =====
async function addEnrollment() {
  try {
    const formData = await showEditForm('Adicionar Matrícula', [
      { name: 'id_aluno', label: 'ID/Matrícula do Aluno', type: 'text', required: true },
      { name: 'id_oferta', label: 'ID da Oferta', type: 'number', required: true },
      { name: 'status', label: 'Status', type: 'select', options: ['Matriculado', 'Aprovado', 'Reprovado', 'Trancado'], value: 'Matriculado' },
      { name: 'media_final', label: 'Média Final', type: 'number', step: '0.1' }
    ]);

    if (formData) {
      await apiService.createEnrollment(formData);
      await dataManager.loadEnrollments();
      loadEnrollmentsTable();
      updateDashboard();
      showNotification("Matrícula criada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao criar matrícula:', error);
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
      await apiService.updateEnrollment(idAluno, idOferta, formData);
      await dataManager.loadEnrollments();
      loadEnrollmentsTable();
      updateDashboard();
      showNotification("Matrícula atualizada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao editar matrícula:', error);
  }
}

async function deleteEnrollment(idAluno, idOferta) {
  if (!confirm("Tem certeza que deseja excluir esta matrícula?")) return;

  try {
    await apiService.deleteEnrollment(idAluno, idOferta);
    await dataManager.loadEnrollments();
    loadEnrollmentsTable();
    updateDashboard();
    showNotification("Matrícula excluída com sucesso!", "success");
  } catch (error) {
    console.error('Erro ao excluir matrícula:', error);
  }
}

// ===== GRADES CRUD =====
async function addGrade() {
  try {
    const formData = await showEditForm('Adicionar Nota', [
      { name: 'id_avaliacao', label: 'ID da Avaliação', type: 'number', required: true },
      { name: 'id_aluno', label: 'ID/Matrícula do Aluno', type: 'text', required: true },
      { name: 'nota', label: 'Nota (0-10)', type: 'number', step: '0.1', min: '0', max: '10', required: true }
    ]);

    if (formData) {
      await apiService.createGrade(formData);
      await dataManager.loadGrades();
      loadGradesTable();
      updateDashboard();
      showNotification("Nota adicionada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao adicionar nota:', error);
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
      await apiService.updateGrade(idAvaliacao, idAluno, formData);
      await dataManager.loadGrades();
      loadGradesTable();
      updateDashboard();
      showNotification("Nota atualizada com sucesso!", "success");
    }
  } catch (error) {
    console.error('Erro ao editar nota:', error);
  }
}

async function deleteGrade(idAvaliacao, idAluno) {
  if (!confirm("Tem certeza que deseja excluir esta nota?")) return;

  try {
    await apiService.deleteGrade(idAvaliacao, idAluno);
    await dataManager.loadGrades();
    loadGradesTable();
    updateDashboard();
    showNotification("Nota excluída com sucesso!", "success");
  } catch (error) {
    console.error('Erro ao excluir nota:', error);
  }
}

// ===== UTILITY FUNCTIONS =====
async function refreshAllData() {
  showNotification("Atualizando dados...", "info");
  const success = await dataManager.loadAllData();
  if (success) {
    // Recarregar todas as tabelas
    loadStudentsTable();
    loadCoursesTable();
    loadProfessorsTable();
    loadSubjectsTable();
    loadOffersTable();
    loadEvaluationsTable();
    loadEnrollmentsTable();
    loadGradesTable();
    updateDashboard();
    showNotification("Dados atualizados com sucesso!", "success");
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

// Funções auxiliares para edição inline
async function updateStudent(id, studentData) {
  try {
    await apiService.updateStudent(id, studentData);
    await dataManager.loadStudents();
    loadStudentsTable();
    updateDashboard();
  } catch (error) {
    console.error('Erro ao atualizar aluno:', error);
    throw error;
  }
}

async function updateProfessor(id, professorData) {
  try {
    await apiService.updateProfessor(id, professorData);
    await dataManager.loadProfessors();
    loadProfessorsTable();
    updateDashboard();
  } catch (error) {
    console.error('Erro ao atualizar professor:', error);
    throw error;
  }
}

async function updateCourse(id, courseData) {
  try {
    await apiService.updateCourse(id, courseData);
    await dataManager.loadCourses();
    loadCoursesTable();
    updateDashboard();
  } catch (error) {
    console.error('Erro ao atualizar curso:', error);
    throw error;
  }
}