# Sistema de Gestão de Estudantes - SGE

Sistema CRUD completo para gestão acadêmica com frontend em JavaScript e backend Flask + Oracle Database.

## 🚀 Como executar

### 1. Backend (API Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

O backend será executado em: `http://localhost:5000`

### 2. Frontend (Interface Web)

```bash
cd frontend
python -m http.server 8080
```

O frontend será executado em: `http://localhost:8080`

## 🔧 Funcionalidades Implementadas

### ✅ CRUD Completo
- **Alunos**: Criar, ler, atualizar, excluir
- **Cursos**: Criar, ler, atualizar, excluir  
- **Professores**: Criar, ler, atualizar, excluir
- **Matérias**: Criar, ler, atualizar, excluir
- **Ofertas**: Criar, ler, atualizar, excluir
- **Avaliações**: Criar, ler, atualizar, excluir
- **Matrículas**: Criar, ler, atualizar, excluir
- **Notas**: Criar, ler, atualizar, excluir

### 🌐 API Endpoints

| Entidade | Endpoint | Métodos Suportados |
|----------|----------|-------------------|
| Alunos | `/api/students` | GET, POST |
| Alunos | `/api/students/{id}` | GET, PUT, DELETE |
| Cursos | `/api/courses` | GET, POST |
| Cursos | `/api/courses/{id}` | GET, PUT, DELETE |
| Professores | `/api/professors` | GET, POST |
| Professores | `/api/professors/{id}` | GET, PUT, DELETE |
| Matérias | `/api/subjects` | GET, POST |
| Matérias | `/api/subjects/{idMateria}/{idCurso}` | GET, PUT, DELETE |
| Ofertas | `/api/offers` | GET, POST |
| Ofertas | `/api/offers/{id}` | GET, PUT, DELETE |
| Avaliações | `/api/evaluations` | GET, POST |
| Avaliações | `/api/evaluations/{id}` | GET, PUT, DELETE |
| Matrículas | `/api/enrollments` | GET, POST |
| Matrículas | `/api/enrollments/{idAluno}/{idOferta}` | GET, PUT, DELETE |
| Notas | `/api/grades` | GET, POST |
| Notas | `/api/grades/{idAvaliacao}/{idAluno}` | GET, PUT, DELETE |

### 💡 Recursos do Frontend

- Interface responsiva e intuitiva
- Formulários dinâmicos para criação/edição
- Confirmações de segurança para exclusões
- Notificações de sucesso/erro
- Busca e filtros em todas as tabelas
- Dashboard com estatísticas em tempo real
- Sistema de navegação fluido

### 🏗️ Arquitetura

- **Frontend**: JavaScript vanilla com módulos ES6
- **Backend**: Flask REST API com padrão MVC
- **Banco**: Oracle Database com cx-Oracle
- **Comunicação**: CORS habilitado, JSON API

## 🛠️ Configurações

### Banco de Dados
Configure a conexão Oracle no arquivo `backend/db/db_conn.py`

### CORS
O CORS está habilitado para desenvolvimento. Para produção, configure domínios específicos.

## ✨ Melhorias Implementadas

1. **Integração completa com API**: Todas as operações CRUD conectadas
2. **Tratamento de erros**: Mensagens claras para o usuário
3. **Interface aprimorada**: Formulários dinâmicos e responsivos  
4. **Validações**: Campos obrigatórios e tipos corretos
5. **Feedback visual**: Notificações e estados de carregamento

---
*Repositório para versionamento de códigos referentes ao trabalho do professor Howard Roatti*
