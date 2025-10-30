"""
Script para popular o banco de dados com dados de exemplo
Execução: docker exec -it natacao_backend python -m app.init_db
"""
from datetime import date, time, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.aluno import Aluno
from app.models.pagamento import Pagamento
from app.models.horario import Horario
from app.models.turma import AlunoHorario


def limpar_banco():
    """Remove todos os dados das tabelas"""
    print("🗑️  Limpando banco de dados...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Banco de dados limpo e tabelas recriadas!")


def criar_alunos(db: Session):
    """Cria 5 alunos de exemplo"""
    print("\n👥 Criando alunos...")

    alunos_data = [
        {
            "nome_completo": "João Silva Santos",
            "responsavel": "Maria Silva",
            "tipo_aula": "natacao",
            "valor_mensalidade": Decimal("150.00"),
            "dia_vencimento": 10,
            "data_inicio_contrato": date(2025, 1, 15),
            "ativo": True,
            "telefone_whatsapp": "(11) 99999-1234",
            "observacoes": "Aluno iniciante, sem restrições médicas"
        },
        {
            "nome_completo": "Ana Paula Oliveira",
            "responsavel": None,  # Maior de idade
            "tipo_aula": "natacao",
            "valor_mensalidade": Decimal("180.00"),
            "dia_vencimento": 5,
            "data_inicio_contrato": date(2024, 6, 1),
            "ativo": True,
            "telefone_whatsapp": "(11) 98888-5678",
            "observacoes": "Nível intermediário, treina para competições"
        },
        {
            "nome_completo": "Carlos Eduardo Mendes",
            "responsavel": "Roberto Mendes",
            "tipo_aula": "natacao",
            "valor_mensalidade": Decimal("150.00"),
            "dia_vencimento": 15,
            "data_inicio_contrato": date(2025, 3, 10),
            "ativo": True,
            "telefone_whatsapp": "(11) 97777-9012",
            "observacoes": "8 anos, sabe nadar, quer aperfeiçoar técnica"
        },
        {
            "nome_completo": "Mariana Costa Lima",
            "responsavel": None,
            "tipo_aula": "hidroginastica",
            "valor_mensalidade": Decimal("120.00"),
            "dia_vencimento": 20,
            "data_inicio_contrato": date(2024, 11, 5),
            "ativo": True,
            "telefone_whatsapp": "(11) 96666-3456",
            "observacoes": "65 anos, recomendação médica para hidroginástica"
        },
        {
            "nome_completo": "Pedro Henrique Rocha",
            "responsavel": "Fernanda Rocha",
            "tipo_aula": "natacao",
            "valor_mensalidade": Decimal("160.00"),
            "dia_vencimento": 10,
            "data_inicio_contrato": date(2025, 2, 1),
            "ativo": True,
            "telefone_whatsapp": "(11) 95555-7890",
            "observacoes": "6 anos, primeira vez na piscina, aulas para iniciantes"
        }
    ]

    alunos = []
    for aluno_data in alunos_data:
        aluno = Aluno(**aluno_data)
        db.add(aluno)
        alunos.append(aluno)

    db.commit()

    for aluno in alunos:
        db.refresh(aluno)
        print(f"  ✅ Aluno criado: {aluno.nome_completo} (ID: {aluno.id})")

    return alunos


def criar_horarios(db: Session):
    """Cria 8 horários de exemplo"""
    print("\n📅 Criando horários...")

    horarios_data = [
        # Segunda-feira
        {
            "dia_semana": "segunda",
            "horario": time(8, 0, 0),
            "capacidade_maxima": 20,
            "tipo_aula": "natacao"
        },
        {
            "dia_semana": "segunda",
            "horario": time(18, 0, 0),
            "capacidade_maxima": 25,
            "tipo_aula": "natacao"
        },
        # Terça-feira
        {
            "dia_semana": "terca",
            "horario": time(9, 0, 0),
            "capacidade_maxima": 15,
            "tipo_aula": "hidroginastica"
        },
        {
            "dia_semana": "terca",
            "horario": time(19, 0, 0),
            "capacidade_maxima": 20,
            "tipo_aula": "natacao"
        },
        # Quarta-feira
        {
            "dia_semana": "quarta",
            "horario": time(8, 0, 0),
            "capacidade_maxima": 20,
            "tipo_aula": "natacao"
        },
        {
            "dia_semana": "quarta",
            "horario": time(18, 30, 0),
            "capacidade_maxima": 25,
            "tipo_aula": "natacao"
        },
        # Quinta-feira
        {
            "dia_semana": "quinta",
            "horario": time(9, 0, 0),
            "capacidade_maxima": 15,
            "tipo_aula": "hidroginastica"
        },
        # Sexta-feira
        {
            "dia_semana": "sexta",
            "horario": time(17, 0, 0),
            "capacidade_maxima": 18,
            "tipo_aula": "natacao"
        }
    ]

    horarios = []
    for horario_data in horarios_data:
        horario = Horario(**horario_data)
        db.add(horario)
        horarios.append(horario)

    db.commit()

    for horario in horarios:
        db.refresh(horario)
        print(f"  ✅ Horário criado: {horario.dia_semana} {horario.horario} - {horario.tipo_aula} (ID: {horario.id})")

    return horarios


def matricular_alunos(db: Session, alunos: list, horarios: list):
    """Matricula alunos em horários"""
    print("\n🎓 Matriculando alunos nos horários...")

    # Definir matrículas (aluno_id, horario_id)
    matriculas = [
        (alunos[0].id, horarios[0].id),  # João - Segunda 08:00 Natação
        (alunos[0].id, horarios[4].id),  # João - Quarta 08:00 Natação
        (alunos[1].id, horarios[1].id),  # Ana - Segunda 18:00 Natação
        (alunos[1].id, horarios[5].id),  # Ana - Quarta 18:30 Natação
        (alunos[2].id, horarios[0].id),  # Carlos - Segunda 08:00 Natação
        (alunos[2].id, horarios[3].id),  # Carlos - Terça 19:00 Natação
        (alunos[3].id, horarios[2].id),  # Mariana - Terça 09:00 Hidroginástica
        (alunos[3].id, horarios[6].id),  # Mariana - Quinta 09:00 Hidroginástica
        (alunos[4].id, horarios[7].id),  # Pedro - Sexta 17:00 Natação
    ]

    for aluno_id, horario_id in matriculas:
        matricula = AlunoHorario(aluno_id=aluno_id, horario_id=horario_id)
        db.add(matricula)

        # Buscar nomes para log
        aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
        horario = db.query(Horario).filter(Horario.id == horario_id).first()
        print(f"  ✅ {aluno.nome_completo} matriculado em {horario.dia_semana} {horario.horario}")

    db.commit()


def criar_pagamentos(db: Session, alunos: list):
    """Cria pagamentos de exemplo para os últimos 6 meses"""
    print("\n💰 Criando pagamentos...")

    hoje = date.today()

    # Pagamentos para João Silva (aluno 0) - últimos 6 meses em dia
    for i in range(6):
        mes_ref = hoje - timedelta(days=30*i)
        pagamento = Pagamento(
            aluno_id=alunos[0].id,
            valor=alunos[0].valor_mensalidade,
            data_pagamento=date(mes_ref.year, mes_ref.month, 10),  # Dia 10
            mes_referencia=mes_ref.strftime("%Y-%m"),
            forma_pagamento="pix",
            observacoes="Pagamento via PIX" if i == 0 else None
        )
        db.add(pagamento)

    # Pagamentos para Ana Paula (aluno 1) - últimos 5 meses em dia
    for i in range(5):
        mes_ref = hoje - timedelta(days=30*i)
        pagamento = Pagamento(
            aluno_id=alunos[1].id,
            valor=alunos[1].valor_mensalidade,
            data_pagamento=date(mes_ref.year, mes_ref.month, 5),  # Dia 5
            mes_referencia=mes_ref.strftime("%Y-%m"),
            forma_pagamento="cartao",
            observacoes="Débito automático" if i == 0 else None
        )
        db.add(pagamento)

    # Pagamentos para Carlos Eduardo (aluno 2) - últimos 4 meses
    for i in range(4):
        mes_ref = hoje - timedelta(days=30*i)
        pagamento = Pagamento(
            aluno_id=alunos[2].id,
            valor=alunos[2].valor_mensalidade,
            data_pagamento=date(mes_ref.year, mes_ref.month, 15),  # Dia 15
            mes_referencia=mes_ref.strftime("%Y-%m"),
            forma_pagamento="transferencia"
        )
        db.add(pagamento)

    # Pagamentos para Mariana (aluno 3) - últimos 6 meses
    for i in range(6):
        mes_ref = hoje - timedelta(days=30*i)
        pagamento = Pagamento(
            aluno_id=alunos[3].id,
            valor=alunos[3].valor_mensalidade,
            data_pagamento=date(mes_ref.year, mes_ref.month, 20),  # Dia 20
            mes_referencia=mes_ref.strftime("%Y-%m"),
            forma_pagamento="dinheiro"
        )
        db.add(pagamento)

    # Pagamentos para Pedro (aluno 4) - últimos 3 meses (tem atraso de 2 meses)
    for i in range(2, 5):  # Começa do mês -2, ou seja, deixa 2 meses sem pagar
        mes_ref = hoje - timedelta(days=30*i)
        pagamento = Pagamento(
            aluno_id=alunos[4].id,
            valor=alunos[4].valor_mensalidade,
            data_pagamento=date(mes_ref.year, mes_ref.month, 10),  # Dia 10
            mes_referencia=mes_ref.strftime("%Y-%m"),
            forma_pagamento="pix"
        )
        db.add(pagamento)

    db.commit()

    # Contar total de pagamentos
    total = db.query(Pagamento).count()
    print(f"  ✅ Total de {total} pagamentos criados")

    # Mostrar resumo por aluno
    for aluno in alunos:
        count = db.query(Pagamento).filter(Pagamento.aluno_id == aluno.id).count()
        print(f"    - {aluno.nome_completo}: {count} pagamentos")


def main():
    """Função principal"""
    print("=" * 60)
    print("🏊 INICIALIZAÇÃO DO BANCO DE DADOS - NATAÇÃO MANAGER")
    print("=" * 60)

    # Confirmar antes de limpar
    print("\n⚠️  ATENÇÃO: Este script irá APAGAR todos os dados existentes!")
    resposta = input("Deseja continuar? (s/n): ")

    if resposta.lower() not in ['s', 'sim', 'y', 'yes']:
        print("❌ Operação cancelada.")
        return

    # Criar sessão do banco
    db = SessionLocal()

    try:
        # 1. Limpar banco
        limpar_banco()

        # 2. Criar alunos
        alunos = criar_alunos(db)

        # 3. Criar horários
        horarios = criar_horarios(db)

        # 4. Matricular alunos
        matricular_alunos(db, alunos, horarios)

        # 5. Criar pagamentos
        criar_pagamentos(db, alunos)

        print("\n" + "=" * 60)
        print("✅ BANCO DE DADOS INICIALIZADO COM SUCESSO!")
        print("=" * 60)
        print("\n📊 Resumo:")
        print(f"  - {len(alunos)} alunos cadastrados")
        print(f"  - {len(horarios)} horários criados")
        print(f"  - 9 matrículas realizadas")
        print(f"  - {db.query(Pagamento).count()} pagamentos registrados")
        print("\n🌐 Acesse o sistema:")
        print("  - Frontend: http://localhost:9001")
        print("  - Backend API: http://localhost:9000")
        print("  - Documentação: http://localhost:9000/docs")
        print("\n💡 Dicas:")
        print("  - Pedro Henrique tem 2 meses de atraso (inadimplente)")
        print("  - Os demais alunos estão com pagamentos em dia")
        print("  - Horário de Segunda 08:00 tem 2 alunos matriculados")
        print("  - Mariana está nos horários de Hidroginástica")

    except Exception as e:
        print(f"\n❌ Erro ao inicializar banco: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
