import graphviz
from cb1 import *

def creategraph(d, count, matrix):
  f = graphviz.Digraph('finite_state_machine', filename='fsm.gv')
  f.attr(rankdir='LR', size='8,5')
  f.attr('node', shape='box')

  for i in range(1, count):
    f.node("NODE_{}".format(i))

  # making nodes for all inputs 
  COL = matrix.shape[1]
  ROW = matrix.shape[0]
  counter = 1

  # first col of inputs
  with f.subgraph(name='cluster_0') as c:
    for i in range(ROW):
      val = int(matrix[i][0])
      if val > 0 :
        c.node("inpt_{}".format(counter))
        c.node("inpt_{}".format(counter+1))
        f.edge("inpt_{}".format(counter),"NODE_{}".format(val), label = "input")
        f.edge("inpt_{}".format(counter+1),"NODE_{}".format(val), label = "input")
        counter += 2
      else :
        c.node("inpt_{}".format(counter))
        for j in range(COL):
          val = int(matrix[i][j])
          if val > 0:
            break
        f.edge("inpt_{}".format(counter),"NODE_{}".format(val), label = "input")
        counter += 1

  # last col of outputs
  counter =1 
  with f.subgraph(name='cluster_1') as c:
    for i in range(ROW):
      val = int(matrix[i][COL-1])
      if val > 0 :
        c.node("otpt_{}".format(counter))
        c.node("otpt_{}".format(counter+1))
        f.edge("NODE_{}".format(val), "otpt_{}".format(counter),  label = "output")
        f.edge("NODE_{}".format(val), "otpt_{}".format(counter+1),label = "output")
        counter += 2
      else :
        c.node("otpt_{}".format(counter))
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
  f.view()

if __name__ == "__main__":
  x = input("No. of Inputs : ")
  x = int(x)
  m, count, arr = do(x)
  print(m)
  d = createcod(m, count, arr)
  creategraph(d, count, m)

