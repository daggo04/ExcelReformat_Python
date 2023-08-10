import os
from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
from main.ProfileApplier import ProfileApplier
import tempfile
import zipfile

app = Flask(__name__)

VERSION = "0.0.1"
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
MAX_FILES = 10
MAX_TOTAL_SIZE_MB = 10  # let's say 50 MB as an example
MAX_TOTAL_SIZE_BYTES = MAX_TOTAL_SIZE_MB * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('input_excel')
        
        if not files:
            return "No file uploaded!", 400

        # Check number of files
        if len(files) > MAX_FILES:
            return jsonify(error="You can process a maximum of {MAX_FILES} files at once."), 400

        # Check total size
        total_size = sum(f.content_length for f in files if f)
        if total_size > MAX_TOTAL_SIZE_BYTES:
            return jsonify(error=f"Total file size exceeds the {MAX_TOTAL_SIZE_MB} MB limit!"), 400

        with tempfile.TemporaryDirectory() as tmpdir:
            output_files = []

            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(tmpdir, filename)
                    file.save(filepath)

                    profile_name = request.form['profile_name']
                    applier = ProfileApplier(input_excel=Path(filepath), profile_name=profile_name)
                    applier.apply()

                    output_filename = "converted_" + filename
                    output_path = os.path.join(tmpdir, output_filename)
                    applier.save_output(Path(output_path))
                    output_files.append(output_path)

            if output_files:
                zip_name = "converted_files.zip"
                zip_path = os.path.join(tmpdir, zip_name)

                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for output_file in output_files:
                        zipf.write(output_file, os.path.basename(output_file))

                return send_from_directory(tmpdir, zip_name, as_attachment=True)
            else:
                return "No valid files processed", 400

    profiles_dir = Path("resources/profiles")
    profile_files = [f.stem for f in profiles_dir.glob('*.json')]
    return render_template('index.html', profiles=profile_files)



if __name__ == "__main__":
    app.run(debug=False)
