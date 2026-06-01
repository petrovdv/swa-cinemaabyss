import random

from flask import Flask, jsonify, request, Response
import requests
import os
app = Flask(__name__)

MONOLITH_URL = os.getenv("MONOLITH_URL", "http://monolith:8080")
MOVIES_SERVICE_URL = os.getenv("MOVIES_SERVICE_URL", "http://movies-service:8081")
EVENTS_SERVICE_URL = os.getenv("EVENTS_SERVICE_URL", "http://events-service:8082")
GRADUAL_MIGRATION = os.getenv("GRADUAL_MIGRATION", "true").lower() == "true"
MOVIES_MIGRATION_PERCENT = int(os.getenv("MOVIES_MIGRATION_PERCENT", "50"))

@app.route('/health')
def health():
    return jsonify({"status": True})

def forward_request(service, path):
    query = request.query_string.decode()
    url = f"{service}{path}"
    if query:
        url += f"?{query}"

    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for key, value in request.headers if key.lower() != "host"},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
    )

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = {name: value for name, value in resp.raw.headers.items() if name.lower() not in excluded_headers}
    return Response(resp.content, resp.status_code, headers)

@app.route(
    '/api/<string:service>/<path:unused>',
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
@app.route(
    '/api/<string:service>',
    defaults={'unused': ''},
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
def proxy_redirect(service, unused):
    redirect_to_service = MONOLITH_URL
    if GRADUAL_MIGRATION:
        match service:
            case "movies":
                if random.random() < MOVIES_MIGRATION_PERCENT / 100:
                    redirect_to_service = MOVIES_SERVICE_URL
            case "events":
                redirect_to_service = EVENTS_SERVICE_URL

    return forward_request(redirect_to_service, request.path)

