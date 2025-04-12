from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load the blacklisted NGOs data
with open('blacklisted.json', 'r') as f:
    blacklisted_data = json.load(f)

@app.route('/api/check-ngo', methods=['POST'])
def check_ngo():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'NGO name is required'}), 400
    
    ngo_name = data['name'].strip()
    
    # Check if the NGO name exists in the blacklisted data
    for ngo in blacklisted_data:
        if ngo_name.lower() == ngo.get('Name of NPODARPAN', '').lower():
            return jsonify({
                'status': 'blacklisted',
                'details': ngo
            })
    
    return jsonify({'status': 'not blacklisted'})

if __name__ == '__main__':
    app.run(debug=True)
