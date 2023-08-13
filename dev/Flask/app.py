from flask import Flask, render_template, url_for, request
from utils import SkinDiagnosis
from config_path import skinmodel1_path, skinmodel2_path, skinmodel3_path, skindisease_step_path, skinlabel_decode_path

app = Flask(__name__)

@app.route("/")
def main():
    disease, link, details = "", "", ""
    return render_template("index.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        img = request.files["image"]
        img_path = "static/img/" + img.filename
        img.save(img_path)

        output = SkinDiagnosis(img_path, skinmodel1_path, skinmodel2_path,
                               skinmodel3_path, skinlabel_decode_path, skindisease_step_path)
        disease, link, details = output
        return render_template("index2.html", disease=disease, link=link, details=details, img=img_path)


if __name__ == "__main__":
    app.run(debug=True)
