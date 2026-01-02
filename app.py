from flask import Flask, render_template, request, send_file
from logic.scoring import run_pipeline
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        trends = request.files["trends"]
        path = os.path.join(app.config["UPLOAD_FOLDER"], trends.filename)
        trends.save(path)

        output_path = run_pipeline(path)
        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
