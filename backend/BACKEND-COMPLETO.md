# Sistema de Gestão de Estudantes - Backend Completo

## 📋 Visão Geral

Este é um sistema CRUD completo com foco no banco de dados Oracle para gestão de estudantes, desenvolvido com Flask (Python).

**⚠️ IMPORTANTE:** Este sistema foi intencionalmente desenvolvido com vulnerabilidades de SQL Injection. Todas as queries utilizam concatenação de strings.

## 🏗️ Arquitetura do Sistema

### Estrutura de Diretórios
```
backend/
├── app.py                       # Aplicação principal Flask
├── requirements.txt             # Dependências Python
├── .env.example                 # Exemplo de configuração
├── API_DOCUMENTATION.md         # Documentação da API
├── db/
│   └── db_conn.py               # Conexão com Oracle
├── models/                      # Modelos de dados
│   ├── student.py
│   ├── course.py
│   ├── professor.py
│   ├── subject.py
│   ├── offer.py
│   ├── evaluation.py
│   ├── grade_student.py
│   └── student_evaluation.py
└── controllers/                 # Controladores REST
    ├── student_controller.py
    ├── course_controller.py
    ├── professor_controller.py
    ├── subject_controller.py
    ├── offer_controller.py
    ├── evaluation_controller.py
    ├── grade_student_controller.py
    ├── student_evaluation_controller.py
    └── reports_controller.py
```

## 🎯 Funcionalidades

### ✅ **CRUD Completo para todas as entidades:**

1. **CURSO (Course)**
   - ✅ Criar, Listar, Buscar, Atualizar, Deletar cursos
   - ✅ Validações de integridade (não permite deletar curso com alunos/matérias)

2. **ALUNO (Student)**
   - ✅ Gestão completa de estudantes
   - ✅ Suporte a formatos de data flexíveis
   - ✅ Validações de campos obrigatórios

3. **PROFESSOR (Professor)**
   - ✅ CRUD completo de professores
   - ✅ Validações de integridade referencial

4. **MATERIA (Subject)**
   - ✅ Gestão de matérias por curso
   - ✅ Chave composta (ID_MATERIA, ID_CURSO)
   - ✅ Endpoints específicos por curso

5. **OFERTA (Offer)**
   - ✅ Gestão de ofertas semestrais
   - ✅ Relacionamentos com Professor, Matéria e Curso
   - ✅ Consultas por semestre

6. **AVALIACAO (Evaluation)**
   - ✅ Gestão de avaliações por oferta
   - ✅ Suporte a tipos, pesos e datas

7. **GRADE_ALUNO (Student Enrollment)**
   - ✅ Sistema de matrícula completo
   - ✅ Gestão de status e médias finais
   - ✅ Consultas por aluno e por oferta

8. **AVALIACAO_ALUNO (Student Evaluation)**
   - ✅ Lançamento de notas individuais
   - ✅ Validações de matrícula
   - ✅ Consultas detalhadas

9. **RELATÓRIOS (Reports)**
   - ✅ Relatório de notas por aluno
   - ✅ Carga de trabalho de professores
   - ✅ Dashboard geral do sistema
   - ✅ Estatísticas de avaliações

## 🔗 **Endpoints da API**

### Base URL: `http://localhost:5000/api`

#### **Estudantes**
- `GET /students` - Listar todos os estudantes
- `GET /students/{id}` - Buscar estudante por ID
- `POST /students` - Criar novo estudante
- `PUT /students/{id}` - Atualizar estudante
- `DELETE /students/{id}` - Deletar estudante

#### **Cursos**
- `GET /courses` - Listar todos os cursos
- `GET /courses/{id}` - Buscar curso por ID
- `POST /courses` - Criar novo curso
- `PUT /courses/{id}` - Atualizar curso
- `DELETE /courses/{id}` - Deletar curso

#### **Professores**
- `GET /professors` - Listar todos os professores
- `GET /professors/{id}` - Buscar professor por ID
- `POST /professors` - Criar novo professor
- `PUT /professors/{id}` - Atualizar professor
- `DELETE /professors/{id}` - Deletar professor

#### **Matérias**
- `GET /subjects` - Listar todas as matérias
- `GET /subjects/{id_materia}/{id_curso}` - Buscar matéria específica
- `POST /subjects` - Criar nova matéria
- `PUT /subjects/{id_materia}/{id_curso}` - Atualizar matéria
- `DELETE /subjects/{id_materia}/{id_curso}` - Deletar matéria
- `GET /courses/{id}/subjects` - Matérias de um curso específico

#### **Ofertas**
- `GET /offers` - Listar todas as ofertas
- `GET /offers/{id}` - Buscar oferta por ID
- `POST /offers` - Criar nova oferta
- `PUT /offers/{id}` - Atualizar oferta
- `DELETE /offers/{id}` - Deletar oferta
- `GET /offers/semester/{year}/{semester}` - Ofertas por semestre

#### **Avaliações**
- `GET /evaluations` - Listar todas as avaliações
- `GET /evaluations/{id}` - Buscar avaliação por ID
- `POST /evaluations` - Criar nova avaliação
- `PUT /evaluations/{id}` - Atualizar avaliação
- `DELETE /evaluations/{id}` - Deletar avaliação
- `GET /offers/{id}/evaluations` - Avaliações de uma oferta

#### **Matrículas**
- `GET /enrollments` - Listar todas as matrículas
- `GET /enrollments/{student_id}/{offer_id}` - Buscar matrícula específica
- `POST /enrollments` - Matricular aluno
- `PUT /enrollments/{student_id}/{offer_id}` - Atualizar matrícula
- `DELETE /enrollments/{student_id}/{offer_id}` - Cancelar matrícula
- `GET /students/{id}/enrollments` - Matrículas de um aluno
- `GET /offers/{id}/enrollments` - Matrículas de uma oferta

#### **Notas de Avaliações**
- `GET /student-evaluations` - Listar todas as notas
- `GET /student-evaluations/{eval_id}/{student_id}` - Buscar nota específica
- `POST /student-evaluations` - Lançar nova nota
- `PUT /student-evaluations/{eval_id}/{student_id}` - Atualizar nota
- `DELETE /student-evaluations/{eval_id}/{student_id}` - Deletar nota
- `GET /students/{id}/evaluations` - Notas de um aluno
- `GET /evaluations/{id}/students` - Notas de uma avaliação

#### **Relatórios**
- `GET /reports/student-grades/{id}` - Relatório de notas do aluno
- `GET /reports/professor-workload/{id}` - Carga de trabalho do professor
- `GET /reports/dashboard` - Dashboard geral do sistema

## 🛠️ **Tecnologias Utilizadas**

- **Python 3.x** - Linguagem principal
- **Flask** - Framework web
- **Oracle Database** - Banco de dados
- **oracledb** - Driver Python para Oracle
- **Flask-CORS** - Suporte a CORS
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## ⚙️ **Configuração e Instalação**

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Banco de Dados
```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar configurações no .env
ORACLE_USER=labdatabase
ORACLE_PASS=lab@Database2025
ORACLE_DSN=localhost:1521/XEPDB1
POOL_MIN=1
POOL_MAX=5
```

### 3. Executar Scripts de Criação das Tabelas
Execute o arquivo `DataBase/Create_Table` no Oracle para criar as tabelas.

### 4. Executar a Aplicação
```bash
python app.py
```

A aplicação estará disponível em: `http://localhost:5000`

## 🔧 **Características Técnicas**

### **Tratamento de Erros**
- ✅ Validação de campos obrigatórios
- ✅ Tratamento de exceções de banco de dados
- ✅ Respostas JSON padronizadas
- ✅ Códigos HTTP apropriados

### **Integridade Referencial**
- ✅ Validações antes de inserções
- ✅ Verificações antes de deleções
- ✅ Mensagens de erro específicas

### **Flexibilidade de Dados**
- ✅ Suporte a múltiplos formatos de data
- ✅ Campos opcionais tratados adequadamente
- ✅ Validações de tipos de dados

### **Pool de Conexões**
- ✅ Gerenciamento eficiente de conexões Oracle
- ✅ Configuração de pool mín/máx
- ✅ Liberação automática de recursos

## 📝 **Observações Importantes**

### **SISTEMA EDUCACIONAL**

- **NÃO utilizar em produção** - Sistema intencionalmente vulnerável
- **Ambiente controlado** necessário para testes de segurança

### **Funcionalidades Implementadas:**
- ✅ **CRUD Completo** para todas as entidades
- ✅ **API REST** com endpoints padronizados
- ✅ **Código modular e extensível**
- ✅ **Validações básicas** de integridade de dados
- ✅ **Documentação completa** da API

---

## 📊 **Estrutura do Banco de Dados Oracle**

### **Tabelas Principais:**
```sql
-- Principais entidades do sistema
CURSO           -- Cursos oferecidos
ALUNO           -- Estudantes matriculados  
PROFESSOR       -- Professores do sistema
MATERIA         -- Matérias dos cursos (chave composta)
OFERTA          -- Ofertas semestrais
AVALIACAO       -- Avaliações das ofertas
GRADE_ALUNO     -- Matrículas de alunos
AVALIACAO_ALUNO -- Notas individuais
```

### **Relacionamentos Implementados:**
- **1:N** - Curso → Matérias
- **1:N** - Professor → Ofertas  
- **1:N** - Oferta → Avaliações
- **N:M** - Aluno ↔ Oferta (Grade_Aluno)
- **N:M** - Aluno ↔ Avaliação (Avaliacao_Aluno)

### **Arquivos de Referência:**
- `DataBase/Create_Table` - Scripts de criação das tabelas
- `diagrams/` - Diagramas ER e relacionais
- `backend/models/` - Modelos Python correspondentes

---

## 🎓 **Objetivos Educacionais Atendidos**

✅ **API REST completa** com vulnerabilidades  
✅ **Arquitetura MVC** com Flask e Oracle  
✅ **Sistema CRUD** funcional para gestão acadêmica  
✅ **Documentação completa** 

**BACKEND COMPLETO DESENVOLVIDO PARA MATÉRIA DE BANCO DE DADOS DO PROFESSOR HOWARD** 🎯