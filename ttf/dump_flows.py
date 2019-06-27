import json
import subprocess
import time


def response(flow):
    print(flow.request.path)

    if "cmcm.com" not in flow.request.host or "abyssrium" not in flow.request.path:
        return

    filestub = "flows/{}_{}".format(time.time(), flow.request.path.replace("/", ""))
    request = saveAndDecode("{}_request".format(filestub), flow.request.content)
    response = saveAndDecode("{}_response".format(filestub), flow.response.content)

    if "otherbox" in flow.request.path:
        res = json.loads(response)
        if res["count"] == 0:
            res["list"] = [{
                    "index": "Orb",
                    "id": 18986,
                    "text": "Orb Gift",
                    "heart": 1000000,
                    "gem": 1000000,
                }, {
                    "index": "Gift",
                    "id": 18986,
                    "text": "Gem Gift",
                    "heart": 1000000,
                    "gem": 1000000,
                }, {
                    "index": "Seaweed",
                    "id": 18986,
                    "text": "Seaweed Gift",
                    "heart": 100000,
                    "gem": 100000,
                }, {
                    "index": "Shell",
                    "id": 18986,
                    "text": "Clam Gift",
                    "heart": 100000,
                    "gem": 100000,
                }, {
                    "index": "SeaUrchin",
                    "id": 18986,
                    "text": "Sea Urchin Gift",
                    "heart": 100000,
                    "gem": 100000,
                }, {
                    "index": "Crab",
                    "id": 18986,
                    "text": "Crab Gift",
                    "heart": 100000,
                    "gem": 100000,
                }, {
                    "index": "Krill",
                    "id": 18986,
                    "text": "Krill Gift",
                    "heart": 100000,
                    "gem": 100000,
                }, {
                    "index": "Boost24HR",
                    "id": 18986,
                    "text": "Boost",
                    "heart": 0,
                    "gem": 0,
                }]
            res["count"] = len(res["list"])

        mod = json.dumps(res).encode("utf8")
        mod = saveAndEncrypt("{}_modify".format(filestub), mod)
        flow.response.content = mod


def saveAndDecode(name, content):
    f = open("{}.b64".format(name), "wb")
    f.write(content)
    f.close()

    subprocess.call(["mono", "DoCrypt.exe", "decrypt", "{}.b64".format(name), "{}.dec".format(name)])

    f = open("{}.dec".format(name), "rb")
    data = f.read()
    f.close()

    return data

def saveAndEncrypt(name, content):
    f = open("{}.mod".format(name), "wb")
    f.write(content)
    f.close()

    subprocess.call(["mono", "DoCrypt.exe", "encrypt", "{}.mod".format(name), "{}.mod.b64".format(name)])

    f = open("{}.mod.b64".format(name), "rb")
    data = f.read()
    f.close()
    
    return data
