import json
import redis
from PIL import Image
from io import BytesIO
from flask import Flask, render_template


app = Flask(__name__)
app.config["DEBUG"] = False
with open('config.json', 'r') as f:
	config = json.load(f)
r = redis.Redis(
	host=config["redis"]["host"], 
	port=config["redis"]["port"], 
	db=config["redis"]["db"]
	)
r.set("name", "a")
print(r.get("name"))
@app.route('/')
def home():
	return "OK"
	'''
	return render_template(
		config["template"]["uploader"], 
		img_data=""
		), 200
	'''

@app.route('/index')
def index():
    return "Hello, World!"

if __name__ == "__main__":
	app.run(host=config["host"])