-- Script para remover o sistema de avaliações e notas
-- Executar após fazer backup da base de dados

-- 1. Remover a coluna MEDIA_FINAL da tabela GRADE_ALUNO
ALTER TABLE GRADE_ALUNO DROP COLUMN MEDIA_FINAL;

-- 2. Dropar a tabela AVALIACAO_ALUNO (tabela de associação)
DROP TABLE AVALIACAO_ALUNO;

-- 3. Dropar a tabela AVALIACAO
DROP TABLE AVALIACAO;

-- Comentários:
-- Este script simplifica o sistema acadêmico removendo:
-- - Sistema completo de avaliações (AVALIACAO)
-- - Sistema de notas dos alunos (AVALIACAO_ALUNO)  
-- - Campo de média final das matrículas (MEDIA_FINAL)
-- O sistema passa a ser apenas de matrícula de alunos em cursos/ofertas.