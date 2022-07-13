import json
import redis
from PIL import Image
from io import BytesIO
from flask import Flask, render_template, redirect, request
from werkzeug.utils import secure_filename
import base64


app = Flask(__name__)
app.config["DEBUG"] = False
with open('config.json', 'r') as f:
	config = json.load(f)
r = redis.Redis(
	host=config["redis"]["host"], 
	port=config["redis"]["port"], 
	db=config["redis"]["db"]
	)

allowed_exts = {'jpg', 'jpeg','png','JPG','JPEG','PNG'}
def check_allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_exts

@app.route('/', methods=['GET', 'POST'])
def setter():
	if request.method == 'POST':
		if 'file' not in request.files:
			print('No file attached in request')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			print('No file selected')
			return redirect(request.url)
		if file and check_allowed_file(file.filename):
			filename = secure_filename(file.filename)
			img = Image.open(file.stream)
			with BytesIO() as buf:
				img.save(buf, format=img.format)
				r.set('imgdata', buf.getvalue())   
		return render_template(
			config["template"]["setter"]
			), 200
	else:
		return render_template(
			config["template"]["setter"]
			), 200

@app.route('/getter', methods=['GET', 'POST'])
def getter():
	data = ""
	if r.exists("imgdata"):
		data = base64.b64encode(r.get("imgdata")).decode() 
	return render_template(
		config["template"]["getter"], 
		img_data=data
		), 200

if __name__ == "__main__":
	app.run(host=config["host"])