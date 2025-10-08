// api-service.js - Serviço de integração com o backend

// Configuração da API
const API_BASE_URL = 'http://localhost:5000/api';

// Classe principal para gerenciar requisições à API
class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  // Método genérico para fazer requisições à API
  async request(endpoint, options = {}) {
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const config = { ...defaultOptions, ...options };
    
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, config);
      
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

  // ===== STUDENTS API =====
  async getStudents() {
    return await this.request('/students');
  }

  async createStudent(studentData) {
    return await this.request('/students', {
      method: 'POST',
      body: JSON.stringify(studentData)
    });
  }

  async updateStudent(id, studentData) {
    return await this.request(`/students/${id}`, {
      method: 'PUT',
      body: JSON.stringify(studentData)
    });
  }

  async deleteStudent(id) {
    return await this.request(`/students/${id}`, {
      method: 'DELETE'
    });
  }

  // ===== COURSES API =====
  async getCourses() {
    return await this.request('/courses');
  }

  async createCourse(courseData) {
    return await this.request('/courses', {
      method: 'POST',
      body: JSON.stringify(courseData)
    });
  }

  async updateCourse(id, courseData) {
    return await this.request(`/courses/${id}`, {
      method: 'PUT',
      body: JSON.stringify(courseData)
    });
  }

  async deleteCourse(id) {
    return await this.request(`/courses/${id}`, {
      method: 'DELETE'
    });
  }

  // ===== PROFESSORS API =====
  async getProfessors() {
    return await this.request('/professors');
  }

  async createProfessor(professorData) {
    return await this.request('/professors', {
      method: 'POST',
      body: JSON.stringify(professorData)
    });
  }

  async updateProfessor(id, professorData) {
    return await this.request(`/professors/${id}`, {
      method: 'PUT',
      body: JSON.stringify(professorData)
    });
  }

  async deleteProfessor(id) {
    return await this.request(`/professors/${id}`, {
      method: 'DELETE'
    });
  }

  // ===== SUBJECTS API =====
  async getSubjects() {
    return await this.request('/subjects');
  }

  async createSubject(subjectData) {
    return await this.request('/subjects', {
      method: 'POST',
      body: JSON.stringify(subjectData)
    });
  }

  async updateSubject(idMateria, idCurso, subjectData) {
    return await this.request(`/subjects/${idMateria}/${idCurso}`, {
      method: 'PUT',
      body: JSON.stringify(subjectData)
    });
  }

  async deleteSubject(idMateria, idCurso) {
    return await this.request(`/subjects/${idMateria}/${idCurso}`, {
      method: 'DELETE'
    });
  }

  // ===== OFFERS API =====
  async getOffers() {
    return await this.request('/offers');
  }

  async createOffer(offerData) {
    return await this.request('/offers', {
      method: 'POST',
      body: JSON.stringify(offerData)
    });
  }

  async updateOffer(id, offerData) {
    return await this.request(`/offers/${id}`, {
      method: 'PUT',
      body: JSON.stringify(offerData)
    });
  }

  async deleteOffer(id) {
    return await this.request(`/offers/${id}`, {
      method: 'DELETE'
    });
  }

  // ===== EVALUATIONS API =====
  async getEvaluations() {
    return await this.request('/evaluations');
  }

  async createEvaluation(evaluationData) {
    return await this.request('/evaluations', {
      method: 'POST',
      body: JSON.stringify(evaluationData)
    });
  }

  async updateEvaluation(id, evaluationData) {
    return await this.request(`/evaluations/${id}`, {
      method: 'PUT',
      body: JSON.stringify(evaluationData)
    });
  }

  async deleteEvaluation(id) {
    return await this.request(`/evaluations/${id}`, {
      method: 'DELETE'
    });
  }

  // ===== ENROLLMENTS API =====
  async getEnrollments() {
    return await this.request('/enrollments');
  }

  async createEnrollment(enrollmentData) {
    return await this.request('/enrollments', {
      method: 'POST',
      body: JSON.stringify(enrollmentData)
    });
  }

  async updateEnrollment(idAluno, idOferta, enrollmentData) {
    return await this.request(`/enrollments/${idAluno}/${idOferta}`, {
      method: 'PUT',
      body: JSON.stringify(enrollmentData)
    });
  }

  async deleteEnrollment(idAluno, idOferta) {
    return await this.request(`/enrollments/${idAluno}/${idOferta}`, {
      method: 'DELETE'
    });
  }

  // ===== GRADES API =====
  async getGrades() {
    return await this.request('/grades');
  }

  async createGrade(gradeData) {
    return await this.request('/grades', {
      method: 'POST',
      body: JSON.stringify(gradeData)
    });
  }

  async updateGrade(idAvaliacao, idAluno, gradeData) {
    return await this.request(`/grades/${idAvaliacao}/${idAluno}`, {
      method: 'PUT',
      body: JSON.stringify(gradeData)
    });
  }

  async deleteGrade(idAvaliacao, idAluno) {
    return await this.request(`/grades/${idAvaliacao}/${idAluno}`, {
      method: 'DELETE'
    });
  }
}

// Classe para gerenciar dados e estado da aplicação
class DataManager {
  constructor() {
    this.apiService = new ApiService();
    this.state = {
      students: [],
      courses: [],
      professors: [],
      subjects: [],
      offers: [],
      evaluations: [],
      enrollments: [],
      grades: []
    };
  }

  // Carregar todos os dados da API
  async loadAllData() {
    try {
      showNotification('Carregando dados...', 'info');
      
      // Carregar todos os dados em paralelo
      const [students, courses, professors, subjects, offers, evaluations, enrollments, grades] = await Promise.all([
        this.loadStudents(),
        this.loadCourses(),
        this.loadProfessors(),
        this.loadSubjects(),
        this.loadOffers(),
        this.loadEvaluations(),
        this.loadEnrollments(),
        this.loadGrades()
      ]);

      // Atualizar estado global
      appState.students = students;
      appState.courses = courses;
      appState.professors = professors;
      appState.subjects = subjects;
      appState.offers = offers;
      appState.evaluations = evaluations;
      appState.enrollments = enrollments;
      appState.grades = grades;

      showNotification('Dados carregados com sucesso!', 'success');
      return true;
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      showNotification('Erro ao carregar dados da API', 'error');
      return false;
    }
  }

  // Métodos individuais de carregamento
  async loadStudents() {
    try {
      const data = await this.apiService.getStudents();
      this.state.students = data || [];
      return this.state.students;
    } catch (error) {
      console.error('Erro ao carregar alunos:', error);
      this.state.students = [];
      return [];
    }
  }

  async loadCourses() {
    try {
      const data = await this.apiService.getCourses();
      this.state.courses = data || [];
      return this.state.courses;
    } catch (error) {
      console.error('Erro ao carregar cursos:', error);
      this.state.courses = [];
      return [];
    }
  }

  async loadProfessors() {
    try {
      const data = await this.apiService.getProfessors();
      this.state.professors = data || [];
      return this.state.professors;
    } catch (error) {
      console.error('Erro ao carregar professores:', error);
      this.state.professors = [];
      return [];
    }
  }

  async loadSubjects() {
    try {
      const data = await this.apiService.getSubjects();
      this.state.subjects = data || [];
      return this.state.subjects;
    } catch (error) {
      console.error('Erro ao carregar matérias:', error);
      this.state.subjects = [];
      return [];
    }
  }

  async loadOffers() {
    try {
      const data = await this.apiService.getOffers();
      this.state.offers = data || [];
      return this.state.offers;
    } catch (error) {
      console.error('Erro ao carregar ofertas:', error);
      this.state.offers = [];
      return [];
    }
  }

  async loadEvaluations() {
    try {
      const data = await this.apiService.getEvaluations();
      this.state.evaluations = data || [];
      return this.state.evaluations;
    } catch (error) {
      console.error('Erro ao carregar avaliações:', error);
      this.state.evaluations = [];
      return [];
    }
  }

  async loadEnrollments() {
    try {
      const data = await this.apiService.getEnrollments();
      this.state.enrollments = data || [];
      return this.state.enrollments;
    } catch (error) {
      console.error('Erro ao carregar matrículas:', error);
      this.state.enrollments = [];
      return [];
    }
  }

  async loadGrades() {
    try {
      const data = await this.apiService.getGrades();
      this.state.grades = data || [];
      return this.state.grades;
    } catch (error) {
      console.error('Erro ao carregar notas:', error);
      this.state.grades = [];
      return [];
    }
  }
}

// Instâncias globais
const apiService = new ApiService();
const dataManager = new DataManager();