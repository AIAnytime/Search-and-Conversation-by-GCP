from fastapi import FastAPI, Form
from starlette.responses import HTMLResponse
import requests
import subprocess

app = FastAPI()

def get_access_token():
    # Obtain access token from gcloud
    command = "gcloud auth print-access-token"
    token = subprocess.check_output(command, shell=True).decode("utf-8").strip()
    return token

def converse(query):
    url = "https://discoveryengine.googleapis.com/v1alpha/projects/477054480627/locations/global/collections/default_collection/dataStores/genai-anytime_1698398847402/conversations/-:converse"

    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }

    data = {
        "query": {"input": query},
        "summarySpec": {
            "summaryResultCount": 5,
            "ignoreAdversarialQuery": True,
            "includeCitations": True
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <html>
        <body>
            <form action="/query/" method="post">
                Enter your query: <input type="text" name="q" value="what is this document all about?">
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/query/")
def get_query_response(q: str = Form(...)):
    response = converse(q)
    return response

