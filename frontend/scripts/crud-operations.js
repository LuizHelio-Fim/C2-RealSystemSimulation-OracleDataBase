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
      console.log('Dados do formulário recebidos:', formData); // Debug
      
      try {
        // Fazer a requisição para o backend
        const response = await apiService.createStudent(formData);
        console.log('Resposta da API:', response); // Debug
        
        // Recarregar dados e atualizar interface
        await dataManager.loadStudents();
        loadStudentsTable();
        updateDashboard();
        showNotification("Aluno criado com sucesso!", "success");
      } catch (error) {
        // Se der erro no backend, mostrar dados coletados para debug
        console.warn('Backend indisponível, dados coletados:', formData);
        showNotification("Backend indisponível, mas formulário funcionando: " + JSON.stringify(formData), "info");
      }
    } else {
      console.log('Nenhum dado recebido do formulário'); // Debug
      showNotification('Nenhum dado foi recebido do formulário!', 'error');
    }
  } catch (error) {
    console.error('Erro ao criar aluno:', error);
    showNotification(`Erro ao criar aluno: ${error.message}`, "error");
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
    // Garantir que os dados estão carregados
    if (!dataManager.state.offers || dataManager.state.offers.length === 0) {
      await dataManager.loadOffers();
    }
    
    const offer = dataManager.state.offers.find(o => o.id === id);
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

// ===== ENROLLMENTS - READ ONLY (AUTO-POPULATED) =====
// Note: CRUD operations removed since Grade_Aluno is now auto-populated
// Status comes from Student table and Media_Final is automatically calculated

async function refreshEnrollments() {
  try {
    showNotification("Atualizando dados das matrículas...", "info");
    
    // Call the backend refresh endpoint
    const response = await fetch(`${apiService.baseURL}/enrollments/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error('Falha ao atualizar dados');
    }
    
    // Reload the data
    await dataManager.loadEnrollments();
    loadEnrollmentsTable();
    updateDashboard();
    showNotification("Dados das matrículas atualizados com sucesso!", "success");
    
  } catch (error) {
    console.error('Erro ao atualizar matrículas:', error);
    showNotification("Erro ao atualizar dados das matrículas!", "error");
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
    // Criar modal dinâmico
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.display = 'block';
    
    let formFields = '';
    fields.forEach(field => {
      if (field.type === 'select') {
        let options = field.options.map(opt => 
          `<option value="${opt}" ${field.value === opt ? 'selected' : ''}>${opt}</option>`
        ).join('');
        formFields += `
          <div class="form-group">
            <label for="${field.name}">${field.label}${field.required ? ' *' : ''}:</label>
            <select id="${field.name}" name="${field.name}" ${field.required ? 'required' : ''}>
              ${options}
            </select>
          </div>
        `;
      } else {
        formFields += `
          <div class="form-group">
            <label for="${field.name}">${field.label}${field.required ? ' *' : ''}:</label>
            <input type="${field.type}" 
                   id="${field.name}" 
                   name="${field.name}" 
                   value="${field.value || ''}"
                   ${field.required ? 'required' : ''}
                   ${field.type === 'email' ? 'pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,}$"' : ''}
                   ${field.type === 'number' ? 'min="1"' : ''}
                   ${field.name === 'cpf' ? 'pattern="[0-9]{3}\\.[0-9]{3}\\.[0-9]{3}-[0-9]{2}|[0-9]{11}" title="CPF deve ter formato: 123.456.789-01 ou 12345678901"' : ''}
                   ${field.name === 'periodo' ? 'min="1" max="12"' : ''}
                   ${field.name === 'carga_horaria_total' || field.name === 'carga_horaria' ? 'min="1" max="9999"' : ''}>
          </div>
        `;
      }
    });
    
    modal.innerHTML = `
      <div class="modal-content">
        <div class="modal-header">
          <h2>${title}</h2>
          <span class="close" onclick="cancelModal();">&times;</span>
        </div>
        <div class="modal-body">
          <form id="editForm" novalidate>
            ${formFields}
            <div class="form-validation-info">
              <small>* Campos obrigatórios</small>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" onclick="cancelModal()">Cancelar</button>
          <button type="button" class="btn btn-primary" onclick="submitModalForm()">Salvar</button>
        </div>
      </div>
    `;
    
    // Adicionar ao container de modais
    const modalContainer = document.getElementById('modalContainer') || document.body;
    modalContainer.appendChild(modal);
    
    // Funções globais para gerenciar o modal
    window.currentModal = modal;
    window.currentModalResolve = resolve;
    
    window.cancelModal = function() {
      if (window.currentModal) {
        window.currentModal.remove();
        window.currentModalResolve(null);
        window.currentModal = null;
        window.currentModalResolve = null;
      }
    };
    
    window.submitModalForm = function() {
      submitForm();
    };
    
    // Função para validar e submeter formulário
    function submitForm() {
      console.log('submitForm chamada'); // Debug
      const form = document.getElementById('editForm');
      const formData = new FormData(form);
      const result = {};
      let isValid = true;
      let errors = [];
      
      console.log('Form encontrado:', form); // Debug
      console.log('FormData:', formData); // Debug
      
      // Validação customizada
      fields.forEach(field => {
        const value = formData.get(field.name);
        result[field.name] = value;
        
        // Validação de campos obrigatórios
        if (field.required && (!value || value.trim() === '')) {
          isValid = false;
          errors.push(`Campo "${field.label}" é obrigatório`);
          return;
        }
        
        // Validações específicas por tipo de campo
        if (value && value.trim()) {
          switch (field.name) {
            case 'email':
              const emailRegex = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i;
              if (!emailRegex.test(value)) {
                isValid = false;
                errors.push('Email deve ter um formato válido');
              }
              break;
            case 'cpf':
              const cpfClean = value.replace(/[^\d]/g, '');
              if (cpfClean.length !== 11) {
                isValid = false;
                errors.push('CPF deve ter 11 dígitos');
              }
              break;
            case 'periodo':
              const periodo = parseInt(value);
              if (periodo < 1 || periodo > 12) {
                isValid = false;
                errors.push('Período deve ser entre 1 e 12');
              }
              break;
            case 'carga_horaria_total':
            case 'carga_horaria':
              const carga = parseInt(value);
              if (carga < 1 || carga > 9999) {
                isValid = false;
                errors.push('Carga horária deve ser entre 1 e 9999 horas');
              }
              break;
          }
        }
      });
      
      console.log('Validação concluída. isValid:', isValid, 'result:', result); // Debug
      
      if (isValid) {
        console.log('Dados válidos, chamando resolve'); // Debug
        window.currentModal.remove();
        window.currentModalResolve(result);
        window.currentModal = null;
        window.currentModalResolve = null;
      } else {
        console.log('Dados inválidos, erros:', errors); // Debug
        // Mostrar erros de validação
        let existingAlert = modal.querySelector('.validation-alert');
        if (existingAlert) existingAlert.remove();
        
        const alertDiv = document.createElement('div');
        alertDiv.className = 'validation-alert alert alert-danger';
        alertDiv.innerHTML = `
          <strong>Erro de validação:</strong>
          <ul>
            ${errors.map(error => `<li>${error}</li>`).join('')}
          </ul>
        `;
        window.currentModal.querySelector('.modal-body').insertBefore(alertDiv, window.currentModal.querySelector('form'));
      }
    }
    
    // Focar no primeiro campo
    setTimeout(() => {
      const firstInput = modal.querySelector('input, select');
      if (firstInput) firstInput.focus();
    }, 100);
    

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

async function updateSubject(id, subjectData) {
  try {
    // Subjects têm chave composta, o id vem como 'id_materia,id_curso'
    const [id_materia, id_curso] = id.split(',');
    await apiService.updateSubject(id_materia, id_curso, subjectData);
    await dataManager.loadSubjects();
    loadSubjectsTable();
    updateDashboard();
  } catch (error) {
    console.error('Erro ao atualizar matéria:', error);
    throw error;
  }
}