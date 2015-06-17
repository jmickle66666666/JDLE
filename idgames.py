import requests

api_url="http://www.doomworld.com/idgames/api/api.php"

def api_call(action,params=None):
    append = ""
    if (params != None):
        for p in params.keys():
            append+="&{0}={1}".format(p,params[p])
    req_url = "{0}?action={1}{2}&out=json".format(api_url,action,append)
    r = requests.get(req_url)
    json = r.json()
    if ("error" in json):
        print("***")
        print("API Error: {0}".format(json["error"]["type"]))
        print("Message: {0}".format(json["error"]["message"]))
        print("***")
    return r.json()

def ping():
    return api_call("ping")
    
def dbping():
    return api_call("dbping")
    
def about():
    return api_call("about")
    
def get(id=None,file=None):
    if (id != None):
        params = {"id":id}
    if (file != None):
        params = {"file":file}
    return api_call("get",params)

def getparentdir(id=None,name=None):
    if (id != None):
        params = {"id":id}
    if (name != None):
        params = {"name":name}
    return api_call("getparentdir",params)
        
def getdirs(id=None,name=None):
    if (id != None):
        params = {"id":id}
    if (name != None):
        params = {"name":name}
    return api_call("getdirs",params)
    
def getfiles(id=None,name=None):
    if (id != None):
        params = {"id":id}
    if (name != None):
        params = {"name":name}
    return api_call("getfiles",params)
    
def getcontents(id=None,name=None):
    if (id != None):
        params = {"id":id}
    if (name != None):
        params = {"name":name}
    return api_call("getcontents",params)
    
def latestvotes(limit=None):
    if (limit != None):
        return api_call("latestvotes",{"limit":limit})
    return api_call("latestvotes")
    
def latestfiles(limit=None,startid=None):
    params = {}
    if (limit != None):
        params["limit"] = limit
    if (startid != None):
        params["startid"] = startid
    return api_call("latestfiles",params)
    
def search(query,type=None,sort=None,dir=None):
    params = {"query":query}
    if (type != None):
        params["type"] = type
    if (sort != None):
        params["sort"] = sort
    if (dir != None):
        params["dir"] = dir
    return api_call("search",params)