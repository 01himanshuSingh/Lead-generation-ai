"""
Enterprise-grade Extraction Orchestrator.

Purpose:
- Coordinate extraction pipeline
- Dynamically load extractors
- Route extraction requests
- Merge extraction results
- Normalize structured outputs

Architecture:
Browser HTML
      ↓
Orchestrator
      ↓
Dynamic Extractor Routing
      ├── RegexExtractor
      ├── DOMParser
      └── AIExtractor
      ↓
Merge Results
      ↓
Structured Lead Data

Design Goals:
- Scalable
- Modular
- Plug-and-play
- Microservice-ready
- Extendable
"""

from __future__ import annotations

from typing import Dict, List, Any

from extractors.regex_extractor import (
    RegexExtractor,
)

from extractors.dom_parser import (
    DOMParser,
)

from utils.logger import (
    logger,
    log_json,
)

from services.extraction_service import (
    ExtractionService
)

from extractors.ai_extractor import (
    AIExtractor
)

# =========================================================
# Extraction Orchestrator
# =========================================================

class ExtractionOrchestrator:
    """
    Central extraction coordination layer.

    Responsibilities:
    - decide which extractor to run
    - manage extraction workflow
    - merge extraction results
    - normalize outputs
    """

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(self):

        logger.info(
            "Initializing ExtractionOrchestrator"
        )

        # -------------------------------------------------
        # Extraction Engines
        # -------------------------------------------------

        self.regex_extractor = (
            RegexExtractor()
        )

        self.dom_parser = (
            DOMParser()
        )
        
        self.extraction_service = (
            ExtractionService()
        )
        self.ai_extractor = (
    AIExtractor()
)
        # -------------------------------------------------
        # Dynamic Extraction Routing
        # -------------------------------------------------

        self.regex_supported = {

            "email",
            "phone",
            "linkedin",
            "website",
            "instagram",
        }

        self.dom_supported = {

            "title",
            "meta",
            "open_graph",
            "schema",
            "visible_text",
        }
        self.ai_supported = {

    "company_name",

    "industry",

    "description",

    "ceo_name",

    "founder_name",

    "address",
}
        logger.info(
            "ExtractionOrchestrator ready"
        )

    # =====================================================
    # Main Extraction Pipeline
    # =====================================================

    async def extract(
        self,
        url: str,
        html: str,
        fields: List[str],
    ) -> Dict[str, Any]:
        """
        Main extraction entrypoint.

        Example:
            fields = [
                "email",
                "phone",
                "meta",
            ]

        Workflow:
            route extraction
            ↓
            run extractors
            ↓
            merge results
            ↓
            return structured output
        """

        logger.info(
            f"Starting extraction pipeline "
            f"-> {fields}"
        )

        results = {}

        try:

            # =================================================
            # REGEX EXTRACTION
            # =================================================

            regex_fields = [

                field
                for field in fields

                if field in self.regex_supported
            ]

            if regex_fields:

                logger.info(
                    f"Running regex extraction "
                    f"-> {regex_fields}"
                )

                regex_results = (
                    self.regex_extractor
                    .extract(
                        text=html,
                        fields=regex_fields,
                    )
                )

                results.update(
                    regex_results
                )

            # =================================================
            # DOM PARSING
            # =================================================

            dom_fields = [

                field
                for field in fields

                if field in self.dom_supported
            ]

            if dom_fields:

                logger.info(
                    f"Running DOM parsing "
                    f"-> {dom_fields}"
                )

                dom_result = (
                    self.dom_parser
                    .parse(html)
                )

                # ---------------------------------------------
                # Dynamic DOM Field Mapping
                # ---------------------------------------------

                if "title" in dom_fields:

                    results["title"] = (
                        dom_result.title
                    )

                if "meta" in dom_fields:

                    results["meta"] = (
                        dom_result.meta
                    )

                if "open_graph" in dom_fields:

                    results["open_graph"] = (
                        dom_result.open_graph
                    )

                if "schema" in dom_fields:

                    results["schema"] = (
                        dom_result.schema_data
                    )

                if "visible_text" in dom_fields:

                    results["visible_text"] = (
                        dom_result.visible_text
                    )
            # =================================================
            # AI EXTRACTION
            # =================================================

            ai_fields = [

                field

                for field in fields

                if field in self.ai_supported
            ]

            if ai_fields:

                logger.info(
                    f"Running AI extraction "
                    f"-> {ai_fields}"
                )

                ai_result = await (
                    self.ai_extractor.extract(

                        url=url,

                        dom_data={

                            "title":
                                results.get(
                                    "title"
                                ),

                            "meta":
                                results.get(
                                    "meta"
                                ),

                            "schema":
                                results.get(
                                    "schema"
                                ),

                            "open_graph":
                                results.get(
                                    "open_graph"
                                ),

                            "visible_text":
                                results.get(
                                    "visible_text"
                                ),
                        },

                        requested_fields=
                            ai_fields,
                    )
                )

                results.update(
                    ai_result.to_dict()
                )
            # =================================================
            # FINAL PIPELINE COMPLETE
            # =================================================

            logger.info(
                "Extraction pipeline completed"
            )

            log_json(
                level="INFO",
                message=(
                    "Extraction success"
                ),
                extra={
                    "fields":
                        list(results.keys())
                },
            )

            # return results
            clean_results = (
                self.extraction_service.process(
                    results
                )
            )

            return clean_results


        except Exception as e:

            logger.error(
                f"Extraction pipeline failed "
                f"-> {e}"
            )

            raise