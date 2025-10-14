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
        const errorText = await response.text();
        let errorData;
        try {
          errorData = JSON.parse(errorText);
        } catch {
          errorData = { message: errorText };
        }
        throw new Error(errorData.message || errorData.error || `HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      // O backend retorna {success: true, data: [...]} ou {success: false, message: "...">
      if (result.success === false) {
        throw new Error(result.message || 'Erro na operação');
      }
      
      // Retorna os dados ou a resposta completa
      return result.data || result;
    } catch (error) {
      console.error('API request failed:', error);
      
      // Melhor diagnóstico de erro de rede
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        const networkError = 'Erro de rede: Não foi possível conectar ao servidor. Verifique se o backend está rodando em http://localhost:5000';
        console.error(networkError);
        showNotification(networkError, 'error');
        throw new Error(networkError);
      } else {
        showNotification(`Erro na API: ${error.message}`, 'error');
        throw error;
      }
    }
  }

  // ===== STUDENTS API =====
  async getStudents() {
    return await this.request('/students');
  }

  async getStudent(id) {
    return await this.request(`/students/${id}`);
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

  async getCourse(id) {
    return await this.request(`/courses/${id}`);
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

  async getProfessor(id) {
    return await this.request(`/professors/${id}`);
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

  async getSubject(idMateria, idCurso) {
    return await this.request(`/subjects/${idMateria}/${idCurso}`);
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

  async getOffer(id) {
    return await this.request(`/offers/${id}`);
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

  // ===== ENROLLMENTS API (Grade Student) =====
  async getEnrollments() {
    return await this.request('/enrollments');
  }

  async getEnrollment(idAluno, idOferta) {
    return await this.request(`/enrollments/${idAluno}/${idOferta}`);
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

  // ===== REPORTS API =====
  async getDashboard() {
    return await this.request('/reports/dashboard');
  }

  async getCourseStatistics() {
    return await this.request('/reports/course-statistics');
  }

  async getOffersCompleteReport() {
    return await this.request('/reports/offers-complete');
  }

  // ===== MÉTODOS DE TESTE E DIAGNÓSTICO =====
  async testConnection() {
    try {
      const response = await fetch(`${this.baseUrl}/`);
      const data = await response.json();
      console.log('✅ Teste de conexão bem-sucedido:', data);
      return data;
    } catch (error) {
      console.error('❌ Teste de conexão falhou:', error);
      throw error;
    }
  }

  async testReportsEndpoint() {
    try {
      const response = await fetch(`${this.baseUrl}/reports/dashboard`);
      const data = await response.json();
      console.log('✅ Teste de endpoint de reports bem-sucedido:', data);
      return data;
    } catch (error) {
      console.error('❌ Teste de endpoint de reports falhou:', error);
      throw error;
    }
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
      enrollments: []
    };
  }

  // Carregar todos os dados da API
  async loadAllData() {
    try {
      showNotification('Carregando dados...', 'info');
      
      // Carregar todos os dados em paralelo
      const [students, courses, professors, subjects, offers, enrollments] = await Promise.all([
        this.loadStudents(),
        this.loadCourses(),
        this.loadProfessors(),
        this.loadSubjects(),
        this.loadOffers(),
        this.loadEnrollments()
      ]);

      // Atualizar estado global
      appState.students = students;
      appState.courses = courses;
      appState.professors = professors;
      appState.subjects = subjects;
      appState.offers = offers;
      appState.enrollments = enrollments;

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
      // Normalizar os dados para incluir 'id' baseado na matrícula
      const students = Array.isArray(data) ? data.map(student => ({
        ...student,
        id: student.matricula // Usar matrícula como ID
      })) : [];
      this.state.students = students;
      return students;
    } catch (error) {
      console.error('Erro ao carregar alunos:', error);
      this.state.students = [];
      return [];
    }
  }

  async loadCourses() {
    try {
      const data = await this.apiService.getCourses();
      this.state.courses = Array.isArray(data) ? data : [];
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
      // Normalizar os dados para incluir 'id' baseado no id_professor
      const professors = Array.isArray(data) ? data.map(professor => ({
        ...professor,
        id: professor.id_professor // Usar id_professor como ID
      })) : [];
      this.state.professors = professors;
      return professors;
    } catch (error) {
      console.error('Erro ao carregar professores:', error);
      this.state.professors = [];
      return [];
    }
  }

  async loadSubjects() {
    try {
      const data = await this.apiService.getSubjects();
      this.state.subjects = Array.isArray(data) ? data : [];
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
      this.state.offers = Array.isArray(data) ? data : [];
      return this.state.offers;
    } catch (error) {
      console.error('Erro ao carregar ofertas:', error);
      this.state.offers = [];
      return [];
    }
  }

  async loadEnrollments() {
    try {
      const data = await this.apiService.getEnrollments();
      this.state.enrollments = Array.isArray(data) ? data : [];
      return this.state.enrollments;
    } catch (error) {
      console.error('Erro ao carregar matrículas:', error);
      this.state.enrollments = [];
      return [];
    }
  }

  // Método para recarregar todos os dados
  async refreshAllData() {
    return await this.loadAllData();
  }
}

// Instâncias globais
const apiService = new ApiService();
const dataManager = new DataManager();