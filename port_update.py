import requests

#       all data returned in objects
#       {"name","date","version","url"}

def generalized_drdteam_info(page):
    base_url = "http://devbuilds.drdteam.org"
    url = base_url+"/"+page+"/"
    
    r = requests.get(url)
    page_data = r.text
    
    chunk = page_data[page_data.find('<td class="x-filename"><a href="')+32:]
    filename = chunk[:chunk.find('">')]
    download_url = base_url + filename
    
    chunk = page_data[page_data.find('<td class="x-date">')+19:]
    date = chunk[:chunk.find('</td>')]
    
    version = filename[filename.find("-")+1:filename.rfind("-")]
    
    output = {"name":page, "date":date, "url":download_url, "version":version}
    
    return output

def get_gzdoom_info():
    return generalized_drdteam_info("gzdoom")
    
def get_zdoom_info():
    return generalized_drdteam_info("zdoom")

def get_prboomplus_info():
    url = "http://prboom-plus.sourceforge.net/history.html"
    
    r = requests.get(url)
    page_data = r.text
    
    chunk = page_data[page_data.find('<span class="ver">')+18:]
    version = chunk[:chunk.find("</span>")]
    
    chunk = page_data[page_data.find('@&nbsp;')+7:]
    date = chunk[:chunk.find("</span>")]
    
    chunk = chunk[chunk.find('<a href="')+9:]
    download_url = chunk[:chunk.find('">win32')]
    
    output = {"name":"prboom-plus", "date":date, "url":download_url, "version":version}
    return output

def get_eternity_info():
    return generalized_drdteam_info("eternity")
    
def  get_zandronum_info():
    url = "http://zandronum.com/download"
    base_url = "http://zandronum.com"
    
    r = requests.get(url)
    page_data = r.text
    
    chunk = page_data[page_data.find("version is <strong>")+19:]
    version = chunk[:chunk.find("</strong>")]
    
    chunk = chunk[chunk.find("released on ")+12:]
    date = chunk[:chunk.find(".</p>")]
    
    chunk = chunk[chunk.find('a href="')+8:]
    download_url = base_url + chunk[:chunk.find('">')]
    
    output = {"name":"zandronum", "version":version, "date":date, "url":download_url}
    return output
    
def get_doomretro_info():
    url = "https://github.com/bradharding/doomretro/releases.atom"
    
    r = requests.get(url)
    page_data = r.text
    
    chunk = page_data[page_data.find("<updated>")+9:]
    date = chunk[:chunk.find("</updated>")]
    
    chunk = chunk[chunk.find("<title>DOOM RETRO ")+18:]
    version = chunk[:chunk.find("</title>")]
    
    r = requests.get("https://github.com/bradharding/doomretro/releases/")
    dpage_data = r.text
    
    chunk = dpage_data[dpage_data.find('<ul class="release-downloads">'):]
    chunk = chunk[chunk.find('<a href="')+9:]
    download_url = "https://www.github.com"+chunk[:chunk.find('" rel=')]
    
    output = {"name":"doom retro", "version":version, "url":download_url, "date":date}
    return output
    
#todo:
#  -chocolate doom
#  -cripsy doom
#  -chocorenderlimits
    
def print_info(data):
    print("---")
    print("Port: "+data["name"])
    print("Latest version: "+data["version"])
    print("Updated on: "+data["date"])
    print("Download: "+data["url"])

def get_all_info():
    output = []
    output.append(get_gzdoom_info())
    output.append(get_zdoom_info())
    output.append(get_eternity_info())
    output.append(get_prboomplus_info())
    output.append(get_zandronum_info())
    output.append(get_doomretro_info())
    return output
    
data = get_all_info()
for d in data:
    print_info(d)
