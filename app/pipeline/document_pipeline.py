from __future__ import annotations

from app.core.logger import logger
from app.models.job import JobStatus

from app.pipeline.consistency_validator import ConsistencyValidator
from app.pipeline.document_aggregator import DocumentAggregator
from app.pipeline.employee_consolidator import EmployeeConsolidator
from app.pipeline.employee_report_builder import EmployeeReportBuilder
from app.pipeline.employee_timeline import EmployeeTimeline
from app.pipeline.page_merger import PageMerger
from app.pipeline.page_processor import PageProcessor
from app.pipeline.response_parser import ResponseParser
from app.pipeline.summary_builder import SummaryBuilder

from app.services.job_service import JobService
from app.services.pdf_service import PDFService

from app.websocket.sender import sender


class DocumentPipeline:
    """
    Pipeline principal do RDO Check.

    Responsável por coordenar todas as etapas do processamento.
    """

    def __init__(self):

        self.job_service = JobService()

        self.pdf_service = PDFService()

        self.processor = PageProcessor()

        self.merger = PageMerger()

        self.parser = ResponseParser()

        self.aggregator = DocumentAggregator()

        self.timeline = EmployeeTimeline()

        self.summary = SummaryBuilder()

        self.consolidator = EmployeeConsolidator()

        self.report = EmployeeReportBuilder()

        self.validator = ConsistencyValidator()

    async def execute(self, job):

        logger.info(
            "Pipeline iniciada: %s",
            job.job_id,
        )

        try:

            await self.job_service.set_status(
                job,
                JobStatus.UPLOADED,
            )

            await sender.job_started(job)

            pages_dir = self.pdf_service.get_pages_directory(
                job.job_id
            )

            output_dir = self.pdf_service.get_output_directory(
                job.job_id
            )

            pdf_path = (
                self.job_service.get_upload_directory(job.job_id)
                / job.filename
            )

            # =====================================================
            # Conversão
            # =====================================================

            await self.job_service.set_step(
                job,
                "Convertendo PDF",
            )

            await sender.log(
                job,
                "INFO",
                "Convertendo PDF...",
            )

            total_pages = self.pdf_service.convert_pdf(
                pdf_path=pdf_path,
                output_dir=pages_dir,
            )

            await self.job_service.set_status(
                job,
                JobStatus.CONVERTED,
            )

            await sender.log(
                job,
                "INFO",
                f"{total_pages} páginas encontradas.",
            )

            # =====================================================
            # Extração
            # =====================================================

            await self.job_service.set_status(
                job,
                JobStatus.EXTRACTING,
            )

            await self.job_service.set_step(
                job,
                "Processando páginas",
            )

            for page in range(1, total_pages + 1):

                try:
                
                    await self.job_service.set_page(
                        job,
                        page,
                        total_pages,
                    )

                    await self.processor.process(
                        job=job,
                        image_path=pages_dir / f"page_{page:03}.png",
                        output_dir=output_dir,
                        page=page,
                    )
                    
                    await sender.progress(
                        job,
                        page,
                        total_pages,
                    )  
                
                except Exception as exc:

                    logger.exception(exc)

                    await sender.log(

                        job,

                        "ERROR",

                        f"Erro na página {page}: {exc}"

                    )

                    continue

            # =====================================================
            # Merge
            # =====================================================

            await self.job_service.set_status(
                job,
                JobStatus.MERGING,
            )

            await self.job_service.set_step(
                job,
                "Consolidando",
            )

            await sender.log(
                job,
                "INFO",
                "Agregando informações..."
            )           
            
            merged = self.merger.merge(
                output_dir
            )

            # =====================================================
            # Parser
            # =====================================================

            
            
            await self.job_service.set_status(
                job,
                JobStatus.PARSING,
            )
            
            await sender.log(
                job,
                "INFO",
                "Interpretando resultados..."
            )
            
            self.parser.parse(
                merged
            )

            # =====================================================
            # Agregação
            # =====================================================

            await self.job_service.set_status(
                job,
                JobStatus.AGGREGATING,
            )

            await self.job_service.set_step(
                job,
                "Agregando",
            )
            
            await sender.log(
                job,
                "INFO",
                "Consolidando páginas..."
            )

            summary_doc = self.aggregator.aggregate(
                merged
            )

            # =====================================================
            # Timeline
            # =====================================================

            await sender.log(
                job,
                "INFO",
                "Construindo timeline..."
            )

            timeline = self.timeline.build(
                summary_doc
            )

            # =====================================================
            # Resumo
            # =====================================================

            await self.job_service.set_status(
                job,
                JobStatus.SUMMARIZING,
            )

            await sender.log(
                job,
                "INFO",
                "Gerando resumo..."
            )

            self.summary.build(
                timeline
            )

            # =====================================================
            # Consolidação
            # =====================================================

            await sender.log(
                job,
                "INFO",
                "Consolidando colaboradores..."
            )

            consolidated = self.consolidator.consolidate(
                merged
            )

            # =====================================================
            # Relatório
            # =====================================================

            await sender.log(
                job,
                "INFO",
                "Gerando relatório..."
            )

            report = self.report.build(
                consolidated
            )

            # =====================================================
            # Validação
            # =====================================================

            await sender.log(
                job,
                "INFO",
                "Validando consistência..."
            )           

            self.validator.validate(
                report
            )

            await sender.progress(
                job,
                total_pages,
                total_pages,
            )
            
            await self.job_service.finish(
                job
            )

            await sender.log(
                job,
                "SUCCESS",
                "Pipeline finalizada.",
            )

            await sender.job_finished(
                job
            )

            logger.info(
                "Pipeline concluída: %s",
                job.job_id,
            )

            return merged

        except Exception as exc:

            await self.job_service.fail(
                job,
                exc,
            )

            await sender.job_failed(
                job,
                str(exc),
            )

            logger.exception(exc)

            raise