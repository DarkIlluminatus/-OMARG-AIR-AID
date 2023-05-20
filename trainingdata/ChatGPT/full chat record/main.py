import json
import quart
import quart_cors
from quart import request, send_file

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Keep track of conversation history. Does not persist if Python session is restarted.
_HISTORY = {}

@app.post("/history/<string:username>")
async def update_history(username):
    request_data = await quart.request.get_json(force=True)
    _HISTORY[username] = request_data["history"]
    return quart.Response(response='OK', status=200)

@app.get("/history/<string:username>")
async def get_history(username):
    return quart.Response(response=json.dumps(_HISTORY.get(username, [])), status=200)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
