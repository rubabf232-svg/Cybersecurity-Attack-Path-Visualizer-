import json
import networkx as nx
import streamlit as st
import plotly.graph_objects as go
from attack_path import build_graph, find_attack_paths, calculate_risk

st.set_page_config(page_title="Cybersecurity Attack Path Visualizer", page_icon="🛡️", layout="wide")
st.title("🛡️ Cybersecurity Attack Path Visualizer")
st.caption("Defensive simulation for understanding network attack paths.")

DEFAULT_NODES=[
{"id":"internet","label":"Internet","type":"External"},
{"id":"web","label":"Web Server","type":"Server"},
{"id":"workstation","label":"Employee PC","type":"Workstation"},
{"id":"internal","label":"Internal Server","type":"Server"},
{"id":"database","label":"Database","type":"Database"},
{"id":"admin","label":"Admin PC","type":"Workstation"}]
DEFAULT_EDGES=[("internet","web"),("web","internal"),("workstation","internal"),("internal","database"),("internal","admin")]

if "nodes" not in st.session_state: st.session_state.nodes=DEFAULT_NODES.copy()
if "edges" not in st.session_state: st.session_state.edges=DEFAULT_EDGES.copy()

with st.sidebar:
    st.header("Simulation Controls")
    ids=[n["id"] for n in st.session_state.nodes]
    source=st.selectbox("Compromised starting node",ids)
    target=st.selectbox("Target node",ids,index=min(4,len(ids)-1))
    st.divider()
    st.subheader("Add Node")
    nid=st.text_input("Node ID")
    label=st.text_input("Label")
    ntype=st.selectbox("Type",["Server","Workstation","Database","Firewall","External"])
    if st.button("Add Node") and nid and nid not in ids:
        st.session_state.nodes.append({"id":nid,"label":label or nid,"type":ntype}); st.rerun()
    st.subheader("Add Connection")
    ids=[n["id"] for n in st.session_state.nodes]
    a=st.selectbox("From",ids,key="a"); b=st.selectbox("To",ids,index=min(1,len(ids)-1),key="b")
    if st.button("Add Connection") and a!=b and (a,b) not in st.session_state.edges and (b,a) not in st.session_state.edges:
        st.session_state.edges.append((a,b)); st.rerun()
    if st.button("Reset Demo Network"):
        st.session_state.nodes=DEFAULT_NODES.copy(); st.session_state.edges=DEFAULT_EDGES.copy(); st.rerun()

G=build_graph(st.session_state.nodes,st.session_state.edges)
paths=find_attack_paths(G,source,target)
risk=calculate_risk(G,source,target,paths)
severity="HIGH" if risk>=70 else "MEDIUM" if risk>=40 else "LOW"

c1,c2,c3,c4=st.columns(4)
c1.metric("Nodes",len(G.nodes)); c2.metric("Connections",len(G.edges)); c3.metric("Possible Paths",len(paths)); c4.metric("Risk Score",f"{risk}/100")
st.subheader(f"Overall Exposure: {severity}")

pos=nx.spring_layout(G,seed=42)
ex=[]; ey=[]
for u,v in G.edges():
    x0,y0=pos[u]; x1,y1=pos[v]; ex += [x0,x1,None]; ey += [y0,y1,None]
edge_trace=go.Scatter(x=ex,y=ey,mode="lines",hoverinfo="none",line=dict(width=1.5))

comp=set(x for p in paths for x in p)
nx_=[]; ny=[]; txt=[]; hov=[]
for n in G.nodes():
    x,y=pos[n]; nx_.append(x); ny.append(y); txt.append(G.nodes[n]["label"])
    hov.append(f"ID: {n}<br>Type: {G.nodes[n]['type']}")
node_trace=go.Scatter(x=nx_,y=ny,mode="markers+text",text=txt,textposition="bottom center",
    hovertext=hov,hoverinfo="text",marker=dict(size=30,color=["red" if n in comp else "lightblue" for n in G.nodes()],line=dict(width=2)))
fig=go.Figure([edge_trace,node_trace])
fig.update_layout(height=560,showlegend=False,margin=dict(l=20,r=20,t=20,b=20),
                  xaxis=dict(visible=False),yaxis=dict(visible=False))
st.plotly_chart(fig,use_container_width=True)

st.subheader("Attack Path Analysis")
if paths:
    for i,p in enumerate(paths,1): st.write(f"**Path {i}:** "+" → ".join(p))
else: st.info("No path exists between the selected nodes.")

report={"source":source,"target":target,"risk_score":risk,"severity":severity,
        "nodes":st.session_state.nodes,"connections":[list(e) for e in st.session_state.edges],"paths":paths}
st.download_button("📄 Download JSON Report",json.dumps(report,indent=2),
                   "attack_path_report.json","application/json")
with st.expander("Network data"): st.json(report)
