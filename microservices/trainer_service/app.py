from flask import Flask, jsonify, request

app = Flask(__name__)

trainers = {}
trainer_id_counter = 1 

@app.route('/trainers', methods=['POST'])
def register_trainer():
    global trainer_id_counter
    data = request.get_json()
    name = data.get('name')
    preferred_cities = data.get('preferred_cities', [])
    skill_areas = data.get('skill_areas', [])

    if not name or not skill_areas:
        return jsonify({'message': 'Name and skill areas are required.'}), 400

    trainer_id = trainer_id_counter
    trainers[trainer_id] = {
        'id': trainer_id,
        'name': name,
        'preferred_cities': preferred_cities,
        'skill_areas': skill_areas
    }

    trainer_id_counter += 1
    return jsonify({'message': 'Trainer registered successfully', 'trainer_id': trainer_id}), 201
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006) 