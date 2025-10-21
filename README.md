# 🎓 Sistema de Gestão de Estudantes

Sistema de gerenciamento acadêmico desenvolvido para fins educacionais na disciplina de Banco de Dados (Prof. Howard).

O sistema permite realizar operações CRUD completas para alunos, cursos, professores, matérias, ofertas e matrículas, além de gerar relatórios dinâmicos e dashboards de desempenho.

---

## 🧭 Visão Geral

O projeto é dividido em duas camadas principais:

- **Backend:** Desenvolvido em Python (Flask) com banco de dados Oracle
- **Frontend:** Desenvolvido em HTML, CSS e JavaScript, com painéis dinâmicos e modais interativos

---

## 📁 Estrutura do Projeto

```
C2-RealSystemSimulation-OracleDataBase/
├── backend/
│   ├── controllers/          # Controladores para cada entidade
│   ├── db/                    # Configuração e conexão com Oracle
│   ├── app.py                 # Aplicação Flask principal
│   ├── requirements.txt       # Dependências Python
│   └── .env.example          # Exemplo de configuração
├── frontend/
│   ├── index.html            # Interface principal
│   ├── scripts/              # JavaScript (API, CRUD, relatórios)
│   └── styles/               # CSS global
├── DataBase/
│   └── Create_Table.sql      # Script de criação do banco
└── README.md
```

---

## ⚙️ Instalação e Configuração

### 1. 🧩 Requisitos

- **Python 3.x**
- **Oracle Database XE 21c**
- **pip (gerenciador de pacotes Python)**

### 2. 📦 Instalar Dependências

No diretório do backend, execute:
```bash
cd backend
pip install -r requirements.txt
```

### 3. 🔐 Configurar Variáveis de Ambiente

Crie o arquivo `.env` com base no `.env.example` e configure suas credenciais Oracle:

```ini
ORACLE_USER=labdatabase
ORACLE_PASS=lab@Database2025
ORACLE_DSN=localhost:1521/XEPDB1
POOL_MIN=1
POOL_MAX=5
```

### 4. 🗃️ Criar o Banco de Dados

Execute o script SQL localizado em:
```sql
DataBase/Create_Table.sql
```

no seu ambiente Oracle (SQL Developer, SQL*Plus ou similar) para criar todas as tabelas e relações.

### 5. 🚀 Executar o Backend

Dentro da pasta `backend/`, execute:
```bash
python app.py
```

A aplicação iniciará em:
```
http://localhost:5000
```

#### Exemplos de endpoints:

```bash
# Listar todos os alunos
GET http://localhost:5000/api/students

# Criar novo aluno
POST http://localhost:5000/api/students

# Obter relatório de estatísticas
GET http://localhost:5000/api/reports/course-statistics
```

Para ver todos os endpoints e exemplos de requisições, consulte o arquivo `API_DOCUMENTATION.md`.

### 6. 🌐 Acessar o Frontend

Após iniciar o backend, abra o arquivo:

```
frontend/index.html
```

no seu navegador preferido. O frontend se conectará automaticamente ao backend em `http://localhost:5000`.

**Funcionalidades disponíveis:**
- 📋 Gerenciamento completo de todas as entidades via interface web
- 🔄 Edição inline de dados
- 📊 Visualização de relatórios dinâmicos
- 🎯 Dashboard com estatísticas em tempo real

---

## 🧱 Funcionalidades Principais

### 🧍‍♂️ Alunos
- CRUD completo (criar, listar, editar, deletar)
- Validação de dados e integridade referencial
- Suporte a múltiplos formatos de data (YYYY-MM-DD e DD/MM/YYYY)

### 🎓 Cursos
- Cadastro e manutenção de cursos
- Associação com matérias e alunos
- Controle de carga horária total

### 👩‍🏫 Professores
- Registro e gerenciamento de professores
- Consultas por oferta e carga horária
- Status ativo/inativo

### 📚 Matérias e Ofertas
- Associação de matérias a cursos
- Ofertas por semestre e professor
- Controle de períodos letivos

### 📝 Matrículas (Grade de Alunos)
- Gerenciamento de matrículas em ofertas
- Controle de status (cursando, aprovado, reprovado)
- Validações de integridade referencial

### 📊 Relatórios
- **Estatísticas por Curso:** Relatório com COUNT() e SUM() mostrando dados agregados
- **Relatório de Ofertas Completas:** Consulta com múltiplos JOINs exibindo informações detalhadas
- **Dashboard Geral:** Visão consolidada do sistema com estatísticas em tempo real

---

## 🧰 Tecnologias Utilizadas

**Backend**
- Python 3.x
- Flask 2.3.2 
- Oracle Database XE 
- oracledb 1.6.0 (driver de conexão Python-Oracle)
- Flask-CORS 4.0.0 (Cross-Origin Resource Sharing)
- python-dotenv 1.0.0 (gerenciamento de variáveis de ambiente)

**Frontend**
- HTML5 
- CSS3 
- JavaScript Vanilla 
- Fetch API (requisições HTTP)

**Banco de Dados**
- Oracle Database XE 21c
- 6 Tabelas relacionais com constraints
- Índices para otimização de queries

---

## 🧩 Características Técnicas

- ✅ Arquitetura MVC modularizada
- ✅ Endpoints RESTful padronizados
- ✅ Validação de dados e erros com mensagens JSON
- ✅ Gerenciamento de pool de conexões Oracle
- ✅ Respostas HTTP apropriadas (200, 201, 400, 404, 500)
- ✅ Relatórios com consultas relacionais complexas (JOINs, agregações)
- ✅ Tratamento robusto de erros e logging detalhado
- ✅ Funções SQL: COUNT, SUM, COALESCE para tratamento de NULL
- ✅ Interface responsiva com edição inline

---

## 🔧 Troubleshooting

### Erro: "DPY-4027: connection pool is closed"
- Reinicie o backend com `python app.py`

### Erro: "ORA-00942: table or view does not exist"
- Verifique se executou o script `Create_Table.sql`
- Confirme que os nomes das tabelas estão pluralizados

### Frontend não conecta ao backend
- Verifique se o backend está rodando em `http://localhost:5000`
- Limpe o cache do navegador (Ctrl+Shift+R)
- Verifique o console do navegador (F12) para erros

### Porta 5000 já está em uso
- No Windows: `netstat -an | findstr :5000`
- Termine o processo ou altere a porta em `app.py`

---

## ⚠️ Observações Importantes

1. **🔒 Segurança:** O sistema foi desenvolvido com foco educacional e **NÃO deve ser usado em produção**.
   
2. **🎓 Propósito Educacional:** Criado para demonstrar conceitos de:
   - Modelagem de banco de dados relacional
   - Operações CRUD com Oracle
   - Consultas SQL complexas (JOINs, agregações)
   - Integração backend-frontend
   - Arquitetura REST API

3. **📝 SQL Queries:** O sistema utiliza consultas com:
   - Múltiplos JOINs entre tabelas
   - Funções de agregação (COUNT, SUM, COALESCE)
   - Tratamento de valores NULL
   - Integridade referencial

---

## 👥 Equipe de Desenvolvimento

- Bernardo Lodi
- João Guilherme 
- Luanna Moreira
- Luiz Hélio
- Pedro Sousa
- Thomas Veiga

---

## 📘 Licença

Este projeto foi desenvolvido para fins educacionais e é de uso livre sob a licença MIT.

## 🧩 Referências

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python-oracledb](https://python-oracledb.readthedocs.io/)
- [Oracle Database Documentation](https://docs.oracle.com/en/database/)

---

**© 2025 — Sistema de Gestão de Estudantes** 

Desenvolvido como parte do projeto acadêmico da disciplina de Banco de Dados.

