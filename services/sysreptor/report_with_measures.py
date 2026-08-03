import os
import json

from reptor import Reptor
from dotenv import load_dotenv

# load environment variables from the .env file
load_dotenv()

# create a connection to the SysReptor using the API token
reptor = Reptor(
    server=os.getenv("REPTOR_SERVER"),
    token=os.getenv("REPTOR_TOKEN"),
    project_id="265623af-a1a9-4b23-881a-aa3fac05a2f6",
)

# load report data from json file
with open("../../test_input_files/report_data.json", "r", encoding="utf-8") as f:
    report_data = json.load(f)

with open("../../test_input_files/style.json", "r", encoding="utf-8") as f:
    report_style = json.load(f)

# update the report section of the project
reptor.api.projects.update_section(
    section_id="report",
    data={"data": report_data}
)
reptor.api.projects.update_section(
    section_id="design",
    data={"data": report_style}
)

# render the project into a PDF document
pdf = reptor.api.projects.render()

# save the generated PDF
with open("../../exports/audit_report_with_measures.pdf", "wb") as f:
    f.write(pdf)
