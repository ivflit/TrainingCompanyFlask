from flask import Flask, jsonify, request

app = Flask(__name__)

trainers = {}
trainer_id_counter = 1 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006) 