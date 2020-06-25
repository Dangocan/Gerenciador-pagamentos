from flask import Flask

app = Flask(__name__)

@app.route("/entrar")
def entrar():
    return render_template("login.html")

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)

