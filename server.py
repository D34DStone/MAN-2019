from flask import Flask, render_template, send_from_directory, send_file, request, jsonify
from random import randint
from LSB import lsb_decode, lsb_encode
from pydub.pydub import AudioSegment
from array import array

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
file_counter = 0

@app.route("/")
def index_handle():
    return render_template("index.html")

@app.route("/scripts/<p>", methods=["GET"])
def scripts_handle(p):
    return send_file('scripts/' + p)

@app.route("/encode/lsb", methods=["POST"])
def encode_lsb_handle():
    if not request.args.get("msg"):
        return jsonify({
            "Res": "Err"
        })

    if 'file' not in request.files:
        return jsonify({
            "Res": "ERR"
        })

    file=request.files['file']
    if file.filename == '':
        return jsonify({
            "Res": "ERR"
        })

    filename = str(randint(100000, 1000000 - 1))
    file.save(app.config['UPLOAD_FOLDER'] + filename + '.wav')

    src_song = AudioSegment.from_wav(app.config['UPLOAD_FOLDER'] + filename + '.wav')
    samples = list(src_song.get_array_of_samples())
    new_samples = lsb_encode(samples, request.args.get("msg"), claster_size=4, sample_size=2*8)
    out_song = src_song._spawn(array('h', new_samples))
    out_song.export(app.config['UPLOAD_FOLDER'] + 'c' + filename + '.wav', format="wav")

    return jsonify({
        "Res": "OK",
        "filename": 'c' + filename + '.wav' 
    })


@app.route("/decode/lsb", methods=["POST"])
def decode_lsb_handle():
    if 'file' not in request.files:
        return jsonify({
            "Res": "ERR"
        })

    file=request.files['file']
    if file.filename == '':
        return jsonify({
            "Res": "ERR"
        })

    filename = str(randint(100000, 1000000 - 1))
    file.save(app.config['UPLOAD_FOLDER'] + filename + '.wav')
    src_song = AudioSegment.from_wav(app.config['UPLOAD_FOLDER'] + filename + '.wav')
    samples = list(src_song.get_array_of_samples())
    msg = lsb_decode(samples)

    with open(app.config['UPLOAD_FOLDER'] + filename + '.txt', 'w') as f:
        f.write(msg)

    return jsonify({
        "Res": "OK",
        "filename": filename + '.txt' 
    })

@app.route('/download/<p>')
def download_p_handle(p):
    return send_file('uploads/' + p)

app.run(host='0.0.0.0', port=5000, debug=True)