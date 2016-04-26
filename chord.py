import json
x = json.load(file("antlr.json"))
authors = set(y["author"] for y in x["commits"])
commit_to_author = dict([(y["commitID"],y["author"]) for y in x["commits"]])
links = dict([(author,dict()) for author in authors])

just_types = [y["type"] for y in x["dates"]]
types = set(just_types)
type_count = dict((jtype,just_types.count(jtype)) for jtype in types)

big_types = set(jtype for jtype in types if type_count[jtype] > 8 *22)
def inc(commit,jtype,off=1):
    author = commit_to_author[commit]
    val = off + links[author].get(jtype,0)
    links[author][jtype] = val


def dec(commit,jtype):
    inc(commit,jtype,off=-1)

    
for d in x["dates"]:
    if d["type"] in big_types:        
        inc(d["commitID"],d["type"])


def link_to_node(name,link,minsize=10):
    size = max(minsize,sum(link.values()))
    imports = [i for i in link.keys() if i in big_types]
    name = name.split(" <")[0]
    return {"name":name,"size":size,"imports":imports}

nodes = [link_to_node(author, links[author]) for author in authors]
nodes = [node for node in nodes if node["size"] > 0 and len(node["imports"]) > 0]
nodes = nodes + [link_to_node(jtype, {}) for jtype in big_types]

json.dump(nodes,file("chord.json","w"),indent=1)
