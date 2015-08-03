import requests

api_url = "http://www.doomworld.com/idgames/api/api.php"


def api_call(action, params=None):
    append = ""
    if params is not None:
        for p in params.keys():
            append += "&{0}={1}".format(p, params[p])
    req_url = "{0}?action={1}{2}&out=json".format(api_url, action, append)
    r = requests.get(req_url)
    json = r.json()
    if "error" in json:
        print("***")
        print("API Error: {0}".format(json["error"]["type"]))
        print("Message: {0}".format(json["error"]["message"]))
        print("***")
    return r.json()


def ping():
    return api_call("ping")


def db_ping():
    return api_call("dbping")


def about():
    return api_call("about")


def get(id=None, file=None):
    if id is not None:
        params = {"id": id}
    if file is not None:
        params = {"file": file}
    return api_call("get", params)


def get_parent_dir(id=None, name=None):
    if id is not None:
        params = {"id": id}
    if name is not None:
        params = {"name": name}
    return api_call("getparentdir", params)


def get_dirs(id=None, name=None):
    if id is not None:
        params = {"id": id}
    if name is not None:
        params = {"name": name}
    return api_call("getdirs", params)


def get_files(id=None, name=None):
    if id is not None:
        params = {"id": id}
    if name is not None:
        params = {"name": name}
    return api_call("getfiles", params)


def get_contents(id=None, name=None):
    if id is not None:
        params = {"id": id}
    if name is not None:
        params = {"name": name}
    return api_call("getcontents", params)


def latest_votes(limit=None):
    if limit is not None:
        return api_call("latestvotes", {"limit": limit})
    return api_call("latestvotes")


def latest_files(limit=None, startid=None):
    params = {}
    if limit is not None:
        params["limit"] = limit
    if startid is not None:
        params["startid"] = startid
    return api_call("latestfiles", params)


def search(query, type=None, sort=None, dir=None):
    params = {"query": query}
    if type is not None:
        params["type"] = type
    if sort is not None:
        params["sort"] = sort
    if dir is not None:
        params["dir"] = dir
    return api_call("search", params)
    
if __name__ == '__main__':
    print(latest_files())
