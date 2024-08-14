import graphviz
from cb1 import *

def creategraph(d, count, matrix):
  f = graphviz.Digraph('finite_state_machine', filename='fsm.gv', engine = "fdp", graph_attr={'splines':'false'})
  f.attr(rankdir='LR')
  f.attr('node', shape='box')
  COL = matrix.shape[1]
  ROW = matrix.shape[0]

  maxx = COL * 2 * 50

  # cluster counts
  clusters = [0 for x in range(count)]
  for r in range(ROW):
    #with f.subgraph(name="cluster_{}".format(r)) as cl:
    #  cl.attr(rank='same')
    for c in range(COL):
      val = int(matrix[r][c])
      if val == 0:
        continue
      clusters[val] = c
      #with f.subgraph(name="cluster_{}".format(c)) as cl:
      f.node("NODE_{}".format(val), pos="{},{}!".format(2*c, maxx - 3*r))


  #for i in range(1, count):
  #  with f.subgraph(name="cluster_{}".format(clusters[i])) as c:
  #    c.node("NODE_{}".format(i))

  # making nodes for all inputs 
  counter = 1
  # first col of inputs
  with f.subgraph(name='cluster_input') as c:
    for i in range(ROW):
      val = int(matrix[i][0])
      if val > 0 :
        c.node("inpt_{}".format(counter), pos = "{},{}!".format(-5, maxx - 3*counter))
        c.node("inpt_{}".format(counter+1), pos = "{},{}!".format(-5, maxx - 3*counter-3))
        f.edge("inpt_{}".format(counter),"NODE_{}".format(val), label = "input")
        f.edge("inpt_{}".format(counter+1),"NODE_{}".format(val), label = "input")
        counter += 2
      else :
        c.node("inpt_{}".format(counter), pos = "{},{}!".format(-5, maxx - 3*counter))
        for j in range(COL):
          val = int(matrix[i][j])
          if val > 0:
            break
        f.edge("inpt_{}".format(counter),"NODE_{}".format(val), label = "input")
        counter += 1

  # last col of outputs
  counter =1 
  with f.subgraph(name='cluster_output') as c:
    for i in range(ROW):
      val = int(matrix[i][COL-1])
      if val > 0 :
        c.node("otpt_{}".format(counter), pos = "{},{}!".format(2*COL, maxx - 3*counter))
        c.node("otpt_{}".format(counter+1), pos = "{},{}!".format(2*COL, maxx - 3*counter-3))
        f.edge("NODE_{}".format(val), "otpt_{}".format(counter),  label = "output")
        f.edge("NODE_{}".format(val), "otpt_{}".format(counter+1),label = "output")
        counter += 2
      else :
        c.node("otpt_{}".format(counter), pos = "{},{}!".format(2*COL, maxx - 3*counter))
        for j in range(COL-1, -1, -1):
          val = int(matrix[i][j])
          if val > 0:
            break
        f.edge("NODE_{}".format(val), "otpt_{}".format(counter),  label = "output")
        counter += 1


  for key in d.keys():
    print(key)
    if key[0] == 'w':
      nds = key.split('_')
      f.edge("NODE_{}".format(nds[1]), "NODE_{}".format(nds[2]), label=key)
  print(f)
  f.view()

if __name__ == "__main__":
  x = input("No. of Inputs : ")
  x = int(x)
  m, count, arr = do(x)
  print(m)
  d = createcod(m, count, arr)
  creategraph(d, count, m)

