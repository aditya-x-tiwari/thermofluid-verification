import json
import os

from google import genai
from google.genai import types

from schemas import PaperSpec


SYSTEM_PROMPT = r"""
You are a scientific-computing assistant analyzing a research paper
for automated CFD/thermofluid validation.

Your task is NOT to reproduce the paper.

Your task is to identify every figure that could be relevant to
validation or reproduction using independently generated COMSOL data.

For every relevant figure determine:

1. Figure number.
2. Figure title/caption.
3. What quantity is plotted.
4. X-axis variable.
5. Y-axis variable.
6. Z-axis if applicable.
7. Plot type.
8. Linear/log axis.
9. Physical fields required to reproduce the figure.
10. Fixed simulation conditions.
11. Parameter values.
12. Reference curves/series.
13. Whether the reference data appears to come from:
    - a table
    - a plotted curve
    - digitization
    - unknown

Important rules:

- Never invent numerical values.
- If a value cannot be determined, use "unknown".
- Distinguish clearly between values explicitly stated in the paper
  and values inferred from context.
- Identify validation figures separately from ordinary result figures.
- For contour/field plots identify the underlying physical field.
- For heatlines identify all quantities likely required to reconstruct them.
- Preserve the paper's terminology but also provide standard variable
  names when obvious.
- Do not generate plotting code.
- Return structured JSON matching the supplied schema.
"""


def analyze_pdf(pdf_path: str) -> PaperSpec:

    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[
            types.Part.from_bytes(
                data=pdf_bytes,
                mime_type="application/pdf"
            ),
            SYSTEM_PROMPT,
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=PaperSpec,
            temperature=0.0,
        ),
    )

    data = json.loads(response.text)

    return PaperSpec.model_validate(data)