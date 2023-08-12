from flask import Flask, render_template, url_for, request
from utils import SkinDiagnosis
model1_path = 'tools/model_isskin.pth'
model2_path = 'tools/model_ishealthy2.pth'
model3_path = 'tools/model_disease2.pth'
label_decode_path = 'tools/label_decode2.txt'
disease_step_path = 'tools/disease_step.json'

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

        output = SkinDiagnosis(img_path, model1_path, model2_path,
                               model3_path, label_decode_path, disease_step_path)
        disease, link, details = output
        return render_template("index2.html", disease=disease, link=link, details=details, img=img_path)


if __name__ == "__main__":
    app.run(debug=True)
