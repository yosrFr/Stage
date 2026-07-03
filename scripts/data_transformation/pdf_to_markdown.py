import pymupdf4llm
import pathlib

md_text = pymupdf4llm.to_markdown(
    "C:/Users/LOQ/Desktop/Stage/test_input_files/IT_Grundschutz_Kompendium_Edition2023.pdf",
    header=False,
    footer=False
)

pathlib.Path(
    "C:/Users/LOQ/Desktop/Stage/exports/IT_Grundschutz_Kompendium_Edition2023.md"
).write_bytes(
    md_text.encode()
)
