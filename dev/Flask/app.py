from flask import Flask, render_template, url_for, request
from utils import SkinDiagnosis
from config_path import SKINMODEL1_PATH, SKINMODEL2_PATH, SKINMODEL3_PATH, SKINDISEASE_STEP_PATH, SKINLABEL_DECODE_PATH

app = Flask(__name__)

@app.route("/")
def main():
    disease, link, details = "", "", ""
    return render_template("index.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        img = request.files["image"]
        IMG_PATH = "static/img/" + img.filename
        img.save(IMG_PATH)

        output = SkinDiagnosis(IMG_PATH, SKINMODEL1_PATH, SKINMODEL2_PATH,
                               SKINMODEL3_PATH, SKINLABEL_DECODE_PATH, SKINDISEASE_STEP_PATH)
        disease, link, details = output
        return render_template("index2.html", disease=disease, link=link, details=details, img=IMG_PATH)


if __name__ == "__main__":
    app.run(debug=True)
