from flask import Flask, jsonify
from flask_cors import CORS

app= Flask(__name__)
cors = CORS(app, origin="http://localhost:5173")

@app.route("/api/users", methods=['GET'])
def members():
    return jsonify(
        {
        "users": [
            'DezS',
            'Cookie',
            'Bread'
        ]
    })

if __name__ =="__main__":
    app.run(debug=True, port=8080)