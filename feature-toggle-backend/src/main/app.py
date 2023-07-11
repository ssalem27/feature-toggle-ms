from flask import Flask, request
import uuid, logging, argparse, time, copy, json

app = Flask(__name__)
flagList = []
flagVersions = {}

def versionAdd(flagEntry):
    version = copy.deepcopy(flagEntry)
    if version["id"] not in flagVersions:
        flagVersions[version["id"]] = []

    flagVersions[version["id"]].append(version)


@app.route("/api/about", methods = ["GET"])
def about():
    #from welcome.json take name of app and message
    return

@app.route("/api/settings", methods = ["GET"])
def settings():
    return

@app.route("/api/flag", methods =["POST"])
def setFlag():
    flag = request.json
    dateAdded = time.time()
    flagid = str(uuid.uuid4())
    flagEntry = {
        "description": flag["description"],
        "key": flag["key"],
        "id": flagid,
        "dateAdded": dateAdded,
        "lastModified": dateAdded,
        "type": flag["type"],
        "value": flag["value"]
    }
    flagList.append(flagEntry)
    versionAdd(flagEntry)
    return flagEntry

@app.route("/api/flag", methods = "GET")
def getFlag():
    valType =request.args.get("type",default=None, type=str)
    key = request.args.get("key", default=None, type=str)

    for flag in flagList:
        if(flag["key"] == key):
            if(flag["type"] == valType):
                return flag
            else:
                return "Flag type must be {}, Your type: {}".format(valType,flag["type"]), 500
    
    return "Flag not found", 500

@app.route("/api/flags", methods = "GET")
def getFlags():
    return flagList

@app.route("/api/flag", methods= "DELETE")
def deleteFlag():
    global flagList
    flagid = request.args.get("id", default = None, type=str)
    flagList =list(filter(lambda flag: flag["id"] != flagid, flagList))
    return flagList

@app.route("/api/flag", methods = "PUT")
def updateFlag():
    flagEntry = request.json
    flagid = flagEntry["id"]
    jsonKeys = flagEntry.keys()
    for flag in flagList:
        if flag["id"] == flagid:
            for key in jsonKeys:
                if key in item and key!="dateAdded":
                    flag[key] = flagEntry[key]
                flag["lastModified"] = time.time()
                versionAdd(flag)
                return flag
    
    return "Flag not found", 500

@app.route("/api/flaghistory", methods="PUT")
def getHistory():
    id = request.args.get("id", default = None, type = "str")
    if id in flagVersions:
        return flagVersions[id]
    return "Flag not found", 500

