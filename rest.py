import json
import requests

class Result:
    def __init__(self, code, message, content = None):
        self.code = code
        self.message = message
        self.content = content

    def json(self):
        o = {"code": self.code, "message": self.message}
        if self.content:
            o["content"] = self.content
        return json.dumps(o)

    def from_response(response):
        if response.status_code == 200:
            j = json.loads(response.text)
            return Result(j["code"], j["message"], j["content"] if "content" in j else None)
        else:
            return Result(response.status_code, "Failed to connect to remote host")

    def __repr__(self):
        return self.json()

class Call:
    def get(address, action, params = []):
        url = "http://" + address + "/" + action + "/" + "/".join([str(p) for p in params])
        return Result.from_response(requests.get(url))