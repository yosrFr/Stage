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
    project_id="c9600fcb-1ec2-411a-8364-26a2b3cef8f6",
)

# load report data from json file
with open("input/data/audit_plan_data.json", "r", encoding="utf-8") as f:
    report_data = json.load(f)

# update the report section of the project
reptor.api.projects.update_section(
    section_id="report",
    data={"data": report_data}
)

# render the project into a PDF document
pdf = reptor.api.projects.render()

# save the generated PDF
with open("output/audit_plan_de.pdf", "wb") as f:
    f.write(pdf)
