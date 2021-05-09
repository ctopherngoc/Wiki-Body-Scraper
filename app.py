from flask import Flask, redirect, url_for, render_template, request, send_file
from scrape import Scrape

app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        try:
            url = request.form['url']
            print(url)
            Scrape(url)
            return send_file("text.csv", mimetype="text/csv")
            #return render_template("success.html")
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return render_template("index.html", errors=errors)
    return render_template("index.html", errors=errors, results=results)


if __name__ == "__main__":
    app.run(debug=True)
