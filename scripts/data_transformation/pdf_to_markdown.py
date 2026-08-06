import pymupdf4llm
import pathlib

md_text = pymupdf4llm.to_markdown(
    "input/IT_Grundschutz_Kompendium_Edition2023.pdf",
    header=False,
    footer=False
)

pathlib.Path(
    "output/IT_Grundschutz_Kompendium_Edition2023.md"
).write_bytes(
    md_text.encode()
)
