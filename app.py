import os
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from logic.scoring_engine import run_pipeline

# -----------------------
# App Configuration
# -----------------------

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
ALLOWED_EXTENSIONS = {"csv"}

app = Flask(__name__)
app.secret_key = "studyconcepts-secret-key"  # change in production
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------
# Helpers
# -----------------------

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# -----------------------
# Routes
# -----------------------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "trends" not in request.files:
            flash("No file part in request.")
            return redirect(request.url)

        file = request.files["trends"]

        if file.filename == "":
            flash("No file selected.")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Only CSV files are allowed.")
            return redirect(request.url)

        filename = file.filename
        upload_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(upload_path)

        try:
            output_path = run_pipeline(upload_path)
        except Exception as e:
            flash(f"Error processing file: {str(e)}")
            return redirect(request.url)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

# -----------------------
# Entry Point
# -----------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
