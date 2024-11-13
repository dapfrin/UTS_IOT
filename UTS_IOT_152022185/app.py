from datetime import datetime
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

data_store = [
    {
        'id': 12,
        'temperature': 33,
        'humidity': 33,
        'brightness': 33,
        'timestamp': '2024-07-06 09:08:07'
    },
    {
        'id': 177,
        'temperature': 33,
        'humidity': 33,
        'brightness': 33,
        'timestamp': '2024-09-08 09:08:07'
    },
]

next_id = max(entry['id'] for entry in data_store)

@app.get('/')
def serve_index():
    return send_file('templates/index.html')

@app.post('/api/data')
def receive_data():
    global next_id
    json_data = request.get_json()

    if not request.is_json or not json_data:
        return jsonify({'message': 'Invalid JSON'}), 400

    next_id += 1
    entry = {
        'id': next_id,
        'temperature': int(json_data['temperature']),
        'humidity': int(json_data['humidity']),
        'brightness': int(json_data['brightness']),
        'timestamp': datetime.now().isoformat()
    }

    data_store.append(entry)

    return jsonify({'message': 'Data successfully received'}), 201

@app.get('/api/stats')
def fetch_data():
    temperature_data = [entry['temperature'] for entry in data_store]
    months_years = [
        {'month_year': datetime.fromisoformat(entry['timestamp']).strftime('%m-%Y')}
        for entry in data_store
    ]

    max_temp = max(temperature_data)
    min_temp = min(temperature_data)
    avg_temp = sum(temperature_data) / len(temperature_data)

    return jsonify({
        'max_temperature': max_temp,
        'min_temperature': min_temp,
        'average_temperature': avg_temp,
        'temperature_humidity_brightness_data': data_store,
        'monthly_data': months_years
    })

if __name__ == '_main_':
    app.run(host='0.0.0.0', port=9990, debug=True)