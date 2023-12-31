import json
import os
import tempfile

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry

load_dotenv()
openai_client = OpenAI()

text = """["@!) ecoinvent Trust in Transparency\n\necoinvent 3.8 Dataset Documentation 'chromite ore concentrate production - KZ - chromite ore concentrate'", 'Source\n\n<table><tr><td>Additional author(s)</td><td>Ruhrberg M., Mistry M.</td></tr><tr><td>Title</td><td>Flacheninanspruchnahme des Kupfererzberbaus</td></tr><tr><td>Year</td><td>2002</td></tr><tr><td>Journal</td><td>Erzmetall</td></tr><tr><td>Issue number</td><td>55</td></tr><tr><td>First author</td><td>NPI</td></tr><tr><td>Title</td><td>Emission Estimation Technique Manual for Mining</td></tr><tr><td>Year</td><td>2001</td></tr><tr><td>Volume number</td><td>1</td></tr><tr><td>First author</td><td>Zimmermann P.</td></tr><tr><td>Additional author(s)</td><td>Doka G., Huber F., Labhardt A. and Ménard M.</td></tr><tr><td>Title</td><td>Okoinventare fiir Entsorgungsprozesse; Grundlagen zur Integration der Entsorgung in Okobilanzen.</td></tr><tr><td>Year</td><td>1996</td></tr><tr><td>Volume number</td><td>1</td></tr><tr><td>Issue number</td><td>1</td></tr><tr><td>First author</td><td>Adelhardt W.</td></tr><tr><td>Additional author(s)</td><td>Antrekowitsch H.</td></tr><tr><td>Title</td><td>Stoffmengenfllsse und Energiebedarf bei der Gewinnung ausgewahlter mineralischer Rohstoffe; Teilstudie Chrom.</td></tr><tr><td>Year</td><td>1998</td></tr><tr><td>Volume number</td><td>3</td></tr><tr><td>First author</td><td>Weidema B. P.</td></tr><tr><td>Additional author(s)</td><td>Et al.</td></tr><tr><td>Title</td><td>Overview and methodology. Data quality guideline for the ecoinvent database version 3</td></tr><tr><td>Year</td><td>2011</td></tr><tr><td>First author</td><td>IPPC</td></tr></table>', 'Title\n\nDraft Reference Document on Best Available Techniques for Management of Tailings and Waste-Rock in Mining Activities', 'Year\n\n2002', 'Volume number\n\n1', 'First author', 'Althaus H. - J.\n\nAdditional author(s) Blaser S., Classen M., Jungbluth N.\n\nTitle Life Cycle Inventories of Metals', 'Year\n\n2000', 'Volume number\n\n10']"""

result_list = [
    {
        "title": "Source",
        "body": "<table><tr><td>Additional author(s)</td><td>Ruhrberg M., Mistry M.</td></tr><tr><td>Title</td><td>Flacheninanspruchnahme des Kupfererzberbaus</td></tr><tr><td>Year</td><td>2002</td></tr><tr><td>Journal</td><td>Erzmetall</td></tr><tr><td>Issue number</td><td>55</td></tr><tr><td>First author</td><td>NPI</td></tr><tr><td>Title</td><td>Emission Estimation Technique Manual for Mining</td></tr><tr><td>Year</td><td>2001</td></tr><tr><td>Volume number</td><td>1</td></tr><tr><td>First author</td><td>Zimmermann P.</td></tr><tr><td>Additional author(s)</td><td>Doka G., Huber F., Labhardt A. and Ménard M.</td></tr><tr><td>Title</td><td>Okoinventare fiir Entsorgungsprozesse; Grundlagen zur Integration der Entsorgung in Okobilanzen.</td></tr><tr><td>Year</td><td>1996</td></tr><tr><td>Volume number</td><td>1</td></tr><tr><td>Issue number</td><td>1</td></tr><tr><td>First author</td><td>Adelhardt W.</td></tr><tr><td>Additional author(s)</td><td>Antrekowitsch H.</td></tr><tr><td>Title</td><td>Stoffmengenfllsse und Energiebedarf bei der Gewinnung ausgewahlter mineralischer Rohstoffe; Teilstudie Chrom.</td></tr><tr><td>Year</td><td>1998</td></tr><tr><td>Volume number</td><td>3</td></tr><tr><td>First author</td><td>Weidema B. P.</td></tr><tr><td>Additional author(s)</td><td>Et al.</td></tr><tr><td>Title</td><td>Overview and methodology. Data quality guideline for the ecoinvent database version 3</td></tr><tr><td>Year</td><td>2011</td></tr><tr><td>First author</td><td>IPPC</td></tr></table>",
    },
    {
        "title": "Title",
        "body": "Draft Reference Document on Best Available Techniques for Management of Tailings and Waste-Rock in Mining Activities",
    },
    {"title": "Year", "body": "2002"},
    {"title": "Volume number", "body": "1"},
    {
        "title": "Althaus H. - J.",
        "body": "Additional author(s) Blaser S., Classen M., Jungbluth N.\n\nTitle Life Cycle Inventories of Metals",
    },
    {"title": "Year", "body": "2000"},
    {"title": "Volume number", "body": "10"},
]



@retry(stop_max_attempt_number=3)
def create_completion(**kwargs):
    return openai_client.chat.completions.create(**kwargs)

response = create_completion(
    model="gpt-4-1106-preview",
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant designed to output JSON with the key name of CSV_Content.",
        },
        {
            "role": "user",
            "content": f"""从下面信息中仔细分辨并提取信息: First Author, Additional Author(s), Title, Year, Volume Number, Issue Number, Journal，输出为csv格式：\n\n{text}""",
        },
    ],
)


result = response.choices[0].message.content
dict_data = json.loads(result)

with open("test.csv", "a+") as f:
    f.write(dict_data["CSV_Content"])
