import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import requests
from dotenv import dotenv_values, load_dotenv

app = Flask(__name__)

base_path = os.path.dirname(os.path.abspath(__file__))
env_file = ".env"
env_path = os.path.join(base_path, env_file)

def get_env_value(key:str, default:str="", env_path:str=".env"):
    if os.path.exists(env_path) and load_dotenv(env_path):
        return dotenv_values(env_path)[key] or default
    else:
        return default


# 환경 변수 로드
app.secret_key = get_env_value("SECRET_KEY", "dev_key_for_local")
API_BASE_URL = get_env_value("API_BASE_URL", "http://drf.service.sh/")
AUTH_URL = API_BASE_URL + get_env_value("AUTH_URL", "api/users/login-in-portal/")


# -----------------------------
# Routes
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            resp = requests.post(AUTH_URL, json={"user_mailid": username, "password": password})
            resp.raise_for_status()
            if resp.status_code == 200:
                _json:dict= resp.json()
                tokens:dict = _json.get("tokens")
                portal_info:list[dict] = _json.get("portal_info")
                user_info:dict = _json.get("user_info")
                session["user"] = user_info.get("user성명")
                session["tokens"] = tokens
                session["portal_info"] = portal_info
                session["user_info"] = user_info
                return redirect(url_for("portal"))
            else:
                return render_template("login.html", error=resp.json().get("message"))

        except Exception as e:
            return render_template("login.html", error=str(e))
    return render_template("login.html")

@app.route("/portal")
def portal():
    if "user" not in session:
        return redirect(url_for("login"))

    ### 바로 link 사용하도록 변환
    portal_info:list[dict] = session.get("portal_info")
    for site in portal_info:
        site["logo"] = API_BASE_URL + site["logo"]
    return render_template("portal.html", sites=portal_info)

@app.route("/logout")
def logout():
    for key in ["user", "tokens", "portal_info", "user_info"]:
        session.pop(key, None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'shinwoo.ico', mimetype='image/vnd.microsoft.icon')