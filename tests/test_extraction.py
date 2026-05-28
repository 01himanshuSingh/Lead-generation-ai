import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from extractors.orchestrator import (
    ExtractionOrchestrator
)

html = """
<html>

<head>

<title>AI Company</title>

<meta
name="description"
content="Best AI company"
/>

</head>

<body>

Contact:
info@company.com

Phone:
+91 9876543210

LinkedIn:
https://linkedin.com/company/test

</body>

</html>
"""

fields = [
    "email",
    "phone",
    "linkedin",
    "title",
    "meta",
    "visible_text",
]

orchestrator = (
    ExtractionOrchestrator()
)

results = orchestrator.extract(
    html=html,
    fields=fields,
)

print(results)