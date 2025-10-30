"""
Serviço de notificações automáticas com APScheduler
"""
import logging
from datetime import datetime, date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from app.models.aluno import Aluno
from app.models.pagamento import Pagamento
from app.services.whatsapp_service import EvolutionWhatsAppService
from app.database import SessionLocal

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NotificacaoService:
    """Serviço para gerenciar notificações automáticas de pagamentos"""

    def __init__(self):
        """Inicializa o serviço de notificações"""
        self.scheduler = BackgroundScheduler(timezone='America/Sao_Paulo')
        self.whatsapp_service = EvolutionWhatsAppService()
        logger.info("NotificacaoService inicializado")

    def verificar_vencimentos(self):
        """
        Verifica alunos com vencimento próximo (3 dias antes) e envia avisos
        Executado diariamente às 9h
        """
        logger.info("Iniciando verificação de vencimentos...")

        db: Session = SessionLocal()
        try:
            hoje = date.today()
            dia_aviso = hoje + timedelta(days=3)  # 3 dias antes do vencimento

            # Buscar alunos ativos com vencimento próximo
            alunos = db.query(Aluno).filter(
                Aluno.ativo == True,
                Aluno.dia_vencimento == dia_aviso.day
            ).all()

            logger.info(f"Encontrados {len(alunos)} alunos com vencimento em {dia_aviso.day}/{dia_aviso.month}")

            # Enviar avisos
            enviados = 0
            falhas = 0

            for aluno in alunos:
                # Verificar se já existe pagamento para o mês atual
                mes_referencia = f"{hoje.year}-{hoje.month:02d}"
                pagamento_existente = db.query(Pagamento).filter(
                    Pagamento.aluno_id == aluno.id,
                    Pagamento.mes_referencia == mes_referencia,
                    Pagamento.pago == True
                ).first()

                # Se já pagou, não enviar aviso
                if pagamento_existente:
                    logger.info(f"Aluno {aluno.nome_completo} já efetuou o pagamento de {mes_referencia}")
                    continue

                # Enviar aviso de vencimento
                try:
                    sucesso = self.whatsapp_service.send_aviso_vencimento(aluno, dias_antes=3)
                    if sucesso:
                        enviados += 1
                        logger.info(f"Aviso de vencimento enviado para {aluno.nome_completo}")
                    else:
                        falhas += 1
                        logger.warning(f"Falha ao enviar aviso para {aluno.nome_completo}")
                except Exception as e:
                    falhas += 1
                    logger.error(f"Erro ao enviar aviso para {aluno.nome_completo}: {str(e)}")

            logger.info(f"Verificação de vencimentos concluída. Enviados: {enviados}, Falhas: {falhas}")

        except Exception as e:
            logger.error(f"Erro na verificação de vencimentos: {str(e)}")
        finally:
            db.close()

    def verificar_inadimplentes(self):
        """
        Verifica alunos inadimplentes (5 dias após vencimento) e envia avisos
        Executado diariamente às 9h
        """
        logger.info("Iniciando verificação de inadimplentes...")

        db: Session = SessionLocal()
        try:
            hoje = date.today()

            # Buscar alunos ativos
            alunos = db.query(Aluno).filter(Aluno.ativo == True).all()

            logger.info(f"Verificando inadimplência de {len(alunos)} alunos ativos")

            # Verificar inadimplência
            enviados = 0
            falhas = 0

            for aluno in alunos:
                # Calcular data de vencimento do mês atual
                try:
                    data_vencimento = date(hoje.year, hoje.month, aluno.dia_vencimento)
                except ValueError:
                    # Caso o dia não exista no mês (ex: 31 de fevereiro)
                    import calendar
                    ultimo_dia = calendar.monthrange(hoje.year, hoje.month)[1]
                    data_vencimento = date(hoje.year, hoje.month, min(aluno.dia_vencimento, ultimo_dia))

                # Calcular dias de atraso
                dias_atraso = (hoje - data_vencimento).days

                # Se passou 5 dias do vencimento, enviar aviso
                if dias_atraso == 5:
                    # Verificar se já existe pagamento
                    mes_referencia = f"{hoje.year}-{hoje.month:02d}"
                    pagamento_existente = db.query(Pagamento).filter(
                        Pagamento.aluno_id == aluno.id,
                        Pagamento.mes_referencia == mes_referencia,
                        Pagamento.pago == True
                    ).first()

                    # Se já pagou, não enviar aviso
                    if pagamento_existente:
                        logger.info(f"Aluno {aluno.nome_completo} já efetuou o pagamento")
                        continue

                    # Enviar aviso de atraso
                    try:
                        sucesso = self.whatsapp_service.send_aviso_atraso(aluno, dias_atraso=dias_atraso)
                        if sucesso:
                            enviados += 1
                            logger.info(f"Aviso de inadimplência enviado para {aluno.nome_completo} ({dias_atraso} dias)")
                        else:
                            falhas += 1
                            logger.warning(f"Falha ao enviar aviso de inadimplência para {aluno.nome_completo}")
                    except Exception as e:
                        falhas += 1
                        logger.error(f"Erro ao enviar aviso de inadimplência para {aluno.nome_completo}: {str(e)}")

            logger.info(f"Verificação de inadimplentes concluída. Enviados: {enviados}, Falhas: {falhas}")

        except Exception as e:
            logger.error(f"Erro na verificação de inadimplentes: {str(e)}")
        finally:
            db.close()

    def iniciar_agendador(self):
        """
        Inicia o agendador de tarefas
        - verificar_vencimentos: diariamente às 9h
        - verificar_inadimplentes: diariamente às 9h
        - timezone: America/Sao_Paulo
        """
        try:
            # Agendar verificação de vencimentos (diariamente às 9h)
            self.scheduler.add_job(
                self.verificar_vencimentos,
                trigger=CronTrigger(hour=9, minute=0, timezone='America/Sao_Paulo'),
                id='verificar_vencimentos',
                name='Verificar vencimentos próximos',
                replace_existing=True
            )
            logger.info("Job 'verificar_vencimentos' agendado para 9h diariamente")

            # Agendar verificação de inadimplentes (diariamente às 9h)
            self.scheduler.add_job(
                self.verificar_inadimplentes,
                trigger=CronTrigger(hour=9, minute=0, timezone='America/Sao_Paulo'),
                id='verificar_inadimplentes',
                name='Verificar inadimplentes',
                replace_existing=True
            )
            logger.info("Job 'verificar_inadimplentes' agendado para 9h diariamente")

            # Iniciar scheduler
            self.scheduler.start()
            logger.info("Agendador iniciado com sucesso (timezone: America/Sao_Paulo)")

            # Listar jobs agendados
            jobs = self.scheduler.get_jobs()
            logger.info(f"Jobs ativos: {len(jobs)}")
            for job in jobs:
                logger.info(f"  - {job.name} (ID: {job.id})")

        except Exception as e:
            logger.error(f"Erro ao iniciar agendador: {str(e)}")
            raise

    def parar_agendador(self):
        """Para o agendador de tarefas"""
        try:
            if self.scheduler.running:
                self.scheduler.shutdown(wait=False)
                logger.info("Agendador parado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao parar agendador: {str(e)}")

    def executar_verificacao_manual(self):
        """
        Executa verificações manualmente (útil para testes)
        """
        logger.info("Executando verificações manuais...")
        self.verificar_vencimentos()
        self.verificar_inadimplentes()
        logger.info("Verificações manuais concluídas")


# Instância global do serviço de notificações
notificacao_service = NotificacaoService()
