"""
Módulo de models do sistema
"""
from app.models.aluno import Aluno
from app.models.pagamento import Pagamento
from app.models.horario import Horario
from app.models.turma import AlunoHorario
from app.models.user import User
from app.models.plano import Plano
from app.models.professor import Professor

__all__ = ["Aluno", "Pagamento", "Horario", "AlunoHorario", "User", "Plano", "Professor"]
