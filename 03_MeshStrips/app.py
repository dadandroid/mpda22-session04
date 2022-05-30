from flask import Flask
import ghhops_server as hs

app = Flask(__name__)
hops = hs.Hops(app)

import meshpath as mp
import meshutils as mu



#MESH STRIPPER COMPONENT ---------------------
@hops.component(
    "/meshstripper",
    name="meshstripper",
    description=" Make a networkx graph with mesh vertices as nodes and mesh edges as edges ",
    inputs=[
        hs.HopsMesh("Mesh","M","Mesh to make networkx graph for"),
        hs.HopsString ("WeightMode ","W","Weight Mode"),
        hs.HopsInteger("StartPoint ","S","Start"),
        hs.HopsInteger("EndPoint ","E","End")
    ],
    outputs=[
        hs.HopsPoint("ShortestPath", "SP" ,"Shortest Path",hs.HopsParamAccess.LIST),
        hs.HopsString("FacesIndex", "I" ,"Faces indexes",hs.HopsParamAccess.LIST),
        hs.HopsInteger("Lengths","L","tree lengths",hs.HopsParamAccess.LIST),
    ])

def meshstripper(mesh,weightMode,S, E):

    strips=[]
    allindexes=[]
    slen=[]

    g = mp.graphFromMesh(mesh, weightMode)

    count = 0

    while len(g.nodes) > 0 :

        if count==0:
            sw = mp.findShortestPath(g, S, E)   

        else:
            startpoint = mu.getStartPoint(g)
            sw = mp.AllShortestPaths(g, startpoint)   

        pathPoints = sw[0]
        pathIndexes = sw[1]
        pathLen = sw[2]
        pathNodes = sw[3]

        strips.extend(pathPoints)
        allindexes.extend(pathIndexes)
        slen.append(pathLen)
        
        g.remove_nodes_from(pathNodes)
        count +=1

    return strips, allindexes, slen





if __name__== "__main__":
    # app.run()
    app.run(debug=True)

