from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TEST_MAPPING_URL = "https://raw.githubusercontent.com/SailLoftAdmin/SailloftTestRepo/main/translation.json"

def load_test_mapping():
    try:
        response = requests.get(TEST_MAPPING_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Failed to fetch test mapping:", e)
        return {}

@app.route('/run', methods=['POST'])
def handle_request():
    payload = request.get_json(force=True)
    commit_id = payload.get("commitID")
    test_names = payload.get("tests", [])

    print(f"Got request for commit {commit_id} with tests {test_names}")

    test_mapping = load_test_mapping()

    cmds = []
    for name in test_names:
        cmd = test_mapping.get(name)
        if cmd:
            cmds.append(cmd)
        else:
            return jsonify({"error": f"Unknown test: {name}"}), 400

    cmd_csv = ",".join(cmds)
    print(cmd_csv)
    return jsonify({
        "commitID": commit_id,
        "commands": cmd_csv
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=8000)
