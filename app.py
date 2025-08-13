import os, requests
from flask import Flask, Response

app = Flask(__name__)

MI_REGION = os.environ["MI_REGION"]
MI_USER_ID = os.environ["MI_USER_ID"]
MI_SERVICE_TOKEN = os.environ["MI_SERVICE_TOKEN"]
MI_DEVICE_DID = os.environ["MI_DEVICE_DID"]

S = requests.Session()
S.headers.update({"User-Agent": "MiHome/6.0.0"})
cookie_domain = f"{MI_REGION}.api.io.mi.com"
S.cookies.set("userId", MI_USER_ID, domain=cookie_domain)
S.cookies.set("serviceToken", MI_SERVICE_TOKEN, domain=cookie_domain)

def is_online():
    url = f"https://{MI_REGION}.api.io.mi.com/app/home/device_list"
    r = S.get(url, timeout=10)
    r.raise_for_status()
    devices = (r.json().get("result") or {}).get("list") or []
    for d in devices:
        if str(d.get("did")) == str(MI_DEVICE_DID):
            return bool(d.get("is_online", d.get("isOnline", False)))
    return False

@app.route("/status")
def status():
    try:
        return Response("UP" if is_online() else "DOWN", mimetype="text/plain")
    except:
        return Response("ERROR", status=500, mimetype="text/plain")
