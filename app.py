import os
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from pathlib import Path
from main.ProfileApplier import ProfileApplier

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'  # change this to a secure location on production

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'input_excel' in request.files:
        file = request.files['input_excel']

        # Check if the user does not select file
        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process the file with your ProfileApplier
            profile_name = request.form['profile_name']
            applier = ProfileApplier(input_excel=Path(filepath), profile_name=profile_name)
            applier.apply()

            # For demonstration, saving output to the same directory
            output_path = Path(filepath).with_name("output_" + filename)
            applier.save_output(output_path)

            return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=output_path.name, as_attachment=True)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)