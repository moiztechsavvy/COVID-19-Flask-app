from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from tensor import Inference

app = Flask(__name__)
data = {}
data["content"] = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    if data:
        return render_template('index.html', data=data)
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    
    if request.method == 'POST':
        f = request.files['file']
        print()
        f.save(os.path.join('images/', f.filename))
        
        model = Inference('models/COVIDNet-CXR-Large', 'model.meta', 'model-8485', 'images/' + f.filename)
        model.opperate()
        data["content"] = str(model.getPrediction() + ':  ' + model.getConfidence())
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)