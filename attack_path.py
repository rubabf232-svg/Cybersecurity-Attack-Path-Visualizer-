import networkx as nx

def build_graph(nodes, edges):
    g=nx.Graph()
    for n in nodes:
        g.add_node(n["id"],label=n["label"],type=n["type"])
    g.add_edges_from(edges)
    return g

def find_attack_paths(g,source,target,max_paths=20):
    if source not in g or target not in g or not nx.has_path(g,source,target): return []
    paths=[]
    for p in nx.all_simple_paths(g,source,target,cutoff=6):
        paths.append(p)
        if len(paths)>=max_paths: break
    return paths

def calculate_risk(g,source,target,paths):
    if not paths: return 0
    shortest=min(len(p) for p in paths)
    path_factor=max(0,45-(shortest-1)*8)
    exposure_factor=min(35,len(paths)*10)
    t=g.nodes[target].get("type","")
    critical=20 if t=="Database" else 10 if t=="Server" else 5
    return min(100,path_factor+exposure_factor+critical)
