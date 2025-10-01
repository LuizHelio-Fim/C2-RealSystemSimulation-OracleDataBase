# API de Estudantes - Documentação

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### 1. Listar todos os estudantes
**GET** `/students`

**Resposta de sucesso (200):**
```json
[
  {
    "id": 1,
    "matricula": "2023001",
    "cpf": "123.456.789-00",
    "nome": "João Silva",
    "data_nasc": "2000-01-15",
    "telefone": "(11) 99999-9999",
    "email": "joao@email.com",
    "periodo": 3,
    "course_id": 1,
    "status_curso": "Ativo"
  }
]
```

### 2. Buscar estudante por ID
**GET** `/students/{id}`

**Resposta de sucesso (200):**
```json
{
  "id": 1,
  "matricula": "2023001",
  "cpf": "123.456.789-00",
  "nome": "João Silva",
  "data_nasc": "2000-01-15",
  "telefone": "(11) 99999-9999",
  "email": "joao@email.com",
  "periodo": 3,
  "course_id": 1,
  "status_curso": "Ativo"
}
```

**Resposta de erro (404):**
```json
{
  "error": "Estudante não encontrado"
}
```

### 3. Criar novo estudante
**POST** `/students`

**Body (JSON):**
```json
{
  "matricula": "2023002",
  "cpf": "987.654.321-00",
  "nome": "Maria Santos",
  "data_nasc": "1999-05-20",
  "telefone": "(11) 88888-8888",
  "email": "maria@email.com",
  "periodo": 1,
  "course_id": 1,
  "status_curso": "Ativo"
}
```

**Campos obrigatórios:** matricula, nome, email, periodo, course_id

**Resposta de sucesso (201):**
```json
{
  "id": 2,
  "message": "Estudante criado com sucesso"
}
```

### 4. Atualizar estudante
**PUT** `/students/{id}`

**Body (JSON):** (Todos os campos são opcionais)
```json
{
  "nome": "Maria Santos Silva",
  "telefone": "(11) 77777-7777",
  "periodo": 2
}
```

**Resposta de sucesso (200):**
```json
{
  "message": "Estudante atualizado com sucesso"
}
```

### 5. Deletar estudante
**DELETE** `/students/{id}`

**Resposta de sucesso (200):**
```json
{
  "message": "Student deleted successfully"
}
```

**Resposta de erro (400):**
```json
{
  "error": "Aluno possui notas matricula e não pode ser excluído, remova-as antes."
}
```

## Formatos de Data
- Aceita formatos: `YYYY-MM-DD` ou `DD/MM/YYYY`
- Retorna sempre no formato: `YYYY-MM-DD`

## Códigos de Status HTTP
- **200**: Sucesso
- **201**: Criado com sucesso
- **400**: Dados inválidos ou erro de validação
- **404**: Recurso não encontrado
- **500**: Erro interno do servidor

## Configuração do Banco de Dados
Certifique-se de ter um arquivo `.env` na pasta backend com:
```
ORACLE_USER=seu_usuario
ORACLE_PASS=sua_senha
ORACLE_DSN=localhost:1521/XEPDB1
POOL_MIN=1
POOL_MAX=5
```