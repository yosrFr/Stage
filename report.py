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
    project_id="8b4072d3-2e3e-4c71-9812-6bc81d0cd1b5",
)

# load report data from json file
with open("report_data.json", "r", encoding="utf-8") as f:
    fields = json.load(f)

# update the report section of the project
reptor.api.projects.update_section(
    section_id="report",
    data={"data": fields}
)

# render the project into a PDF document
pdf = reptor.api.projects.render()

# save the generated PDF
with open("report.pdf", "wb") as f:
    f.write(pdf)
