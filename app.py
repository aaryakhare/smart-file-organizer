from flask import Flask, render_template, request
from organizer import organize_folder
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        folder_path = request.form["folder_path"]
        result = organize_folder(folder_path)
    return render_template(
        "index.html",
        result=result
    )

if __name__ == "__main__":
    app.run(debug=True)