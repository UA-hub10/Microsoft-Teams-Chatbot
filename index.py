import json
from flask_cors import CORS, cross_origin
from flask import Flask, request, Response
from TeamsBot import Agents

Agentsobj = Agents()
app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
@cross_origin()
def home():
    return {"health":"200"}

@app.route("/api/messages", methods=["POST"])
@cross_origin()
def agent():
    try:
        data_string = request.get_data()
        data = json.loads(data_string)
        query = data.get("query")
        response = Agentsobj.Response(query)
        response = response["output"]
        return response
       
    except Exception as e:
        return Response(
            f"bad request! - {e} ",
            400,
        )

if __name__ == "__main__":
    app.run(debug=True)