import json

def format_json(json):
    output = json.replace("{","{\n")
    output = output.replace("}","\n}")
    output = output.replace(",",",\n")
    output = output.replace(" ","")
    
    def chunk_tab(str,tab):
        out = str
        if "{" in out:
            out = out[:out.find("{")+1] + chunk_tab(out[out.find("{")+1:out.rfind("}")-1], tab + 1) + out[out.rfind("}")-1:]
        tabstr = ""
        for i in range(0,tab):
            tabstr += "    "
        return out.replace("\n","\n"+tabstr)
    
    return chunk_tab(output,0)
    