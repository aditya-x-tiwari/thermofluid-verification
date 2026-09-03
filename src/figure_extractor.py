import fitz
from pathlib import Path


def render_pages(pdf_path: str, output_dir: str):

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    document = fitz.open(pdf_path)

    generated = []

    for page_number, page in enumerate(document, start=1):

        pix = page.get_pixmap(
            matrix=fitz.Matrix(2, 2),
            alpha=False
        )

        path = output / f"page_{page_number:03d}.png"

        pix.save(path)

        generated.append(path)

    document.close()

    return generated