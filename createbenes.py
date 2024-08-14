import numpy as np

def getcol(x):
  # x is the number of signals
  d = x.bit_length() 
  if (1<<(d-1)) == x:
    d = d -1
  return 1+2*(d-1)

def getrow(x):
  # cols are d, rows are based on no. of inputs
  if (x%2) :
    r = (x+1)//2
  else:
    r = x//2
  return r

def genmatrix(x):
  # x is the number of signals
  d = getcol(x)
  # print(d)
  # cols are d, rows are based on no. of inputs
  r = getrow(x)
  # print(r)
  mat = np.zeros((r,d))
  return mat, r, d

def mirrorarr(matrix, arr): 
  # theory : if a flop outputs to another flop then mirror of output flop inputs to mirror of input flop
  locations = []
  mloc = []
  for x in arr:
    locations.append([-1, -1])
    mloc.append([-1, -1])

  COL = matrix.shape[1]
  for r, row in enumerate(matrix):
    for c, col in enumerate(row):
      if col > 0:
        # print(col, locations)
        locations[int(col)] = [r, c]
        mloc[int(col)] = [r, COL-1-c]

  for i, connection in enumerate(arr):
    sender1 = connection[0]
    sender2 = connection[1]
    receiver = i
    newsender = int(matrix[mloc[receiver][0], mloc[receiver][1]])

    if sender1 > 0:
      newreceiver1 = int(matrix[mloc[sender1][0], mloc[sender1][1]])
      if(arr[newreceiver1][0] < 0):
        arr[newreceiver1][0] = newsender
      else:
        arr[newreceiver1][1] = newsender
    
    if sender2 > 0:
      newreceiver2 = int(matrix[mloc[sender2][0], mloc[sender2][1]])
      if(arr[newreceiver2][0] < 0):
        arr[newreceiver2][0] = newsender
      else:
        arr[newreceiver2][1] = newsender

    # filling missing connections on center line 0s
  centercol = COL // 2

  for r in range(matrix.shape[0]):
    if matrix[r][centercol] != 0:
      continue
    # it is 0
    # find leftmost output if none then must be the last row and theoretically should not happen, still adding condition for same
    source = -1
    for c in range(centercol, -1, -1):
      if matrix[r][c] == 0:
        continue
      source = int(matrix[r][c])
      break
    # find rightmost for destination
    dest = -1
    for c in range(centercol, COL):
      if matrix[r][c] == 0:
        continue
      # else we found the flop
      dest = int(matrix[r][c])
      break
    # print(source, dest)
    if source > 0 and dest > 0 :
      if(arr[dest][0] < 0):
        arr[dest][0] = source
      else:
        arr[dest][1] = source
  return arr

def CM(totalsignals, matrix, startpointr, startpointc, startcount, arr, inputs):
  # arr is supposed to store what are the outputs of the corresponding flop
  # so we pass over the input flop id which is used to assign destination flop to the input key
  #base case
  if (totalsignals == 2):
    matrix[startpointr,startpointc] = startcount
    startcount += 1
    arr[startcount - 1] = [inputs[0], inputs[1]]
    return matrix, startcount, arr
  
  if totalsignals < 2:
    return matrix, startcount, arr

  rows = matrix.shape[0]
  cols = matrix.shape[1]

  # fill for current total signals
  flops  = totalsignals // 2
  wires = totalsignals % 2
  splitpoint = (flops + wires) // 2
  inputcount = 0
  newinputs_topsplit = []
  newinputs_botsplit = []
  floplist = []
  for i in range(flops):
    matrix[startpointr + i,startpointc] = startcount
    floplist.append(startcount)
    startcount = startcount + 1
    # every time we mark a flop we use two inputs
    arr[startcount - 1 ]  = [inputs[inputcount], inputs[inputcount+1]]
    inputcount = inputcount + 2
  if wires:
    floplist.append(inputs[-1])
  # symmetric filling
  for i in range(flops):
    matrix[startpointr + i,cols -1 - startpointc] = startcount
    startcount = startcount + 1
  # recursively fill the matrix for the 2 splits
  newinputs_topsplit = [jj for jj in floplist]
  newinputs_botsplit = [jj for jj in floplist]
  if wires:
    newinputs_topsplit.pop()
  
  if ( totalsignals % 2):
    (matrix, startcount, arr) = CM(totalsignals//2, matrix, startpointr, startpointc+2, startcount, arr, newinputs_topsplit)
    (matrix, startcount, arr) = CM(totalsignals//2 + wires, matrix, startpointr+splitpoint, startpointc+1, startcount, arr, newinputs_botsplit)
  else:
    (matrix, startcount, arr) = CM(totalsignals//2, matrix, startpointr, startpointc+1, startcount, arr, newinputs_topsplit)
    (matrix, startcount, arr) = CM(totalsignals//2, matrix, startpointr+splitpoint, startpointc+1, startcount, arr, newinputs_botsplit)
  
  return matrix, startcount, arr

def do(x):
  m, r, d = genmatrix(x)
  
  arr = []
  for i in range(r*d+1):
    arr.append([-1, -1])
  # print(arr)
  inputs = []
  for i in range(x):
    inputs.append(-1*i - 1)
  m1, startcount, arr = CM(x, m, 0, 0, 1, arr, inputs)
  # defining connections
  # print(m1, startcount, arr)
  arr = mirrorarr(m1, arr[:min(startcount+1, r*d+1)])

  return m1, startcount, arr

def createoutarr(arr):
  outarr =[]
  for i in range(len(arr)):
    outarr.append([])
  for i, x in enumerate(arr):
    if(x[0] > 0):
      outarr[x[0]].append(i)
    if(x[1] > 0):
      outarr[x[1]].append(i)
  # add padding of -1
  # print(outarr)
  for i, x in enumerate(outarr):
    for _ in range(2-len(x)):
      outarr[i].append(-1)
  return outarr
  # outarr now contains which flop outputs to which flops

def createcod(m, count , arr):

  COL = m.shape[1]
  # for i, v in enumerate(arr):
  #   print(i, v)

  # print select wires
  for i in range(1, count):
    # print("input sel{}".format(i))
    pass

  # print input wires 
  c = 1
  for i in m[:, 0]:
    if i != 0:
      # print("input in_{}".format(c))
      # print("input in_{}".format(c+1))
      c += 2
    else:
      # print("input in_{}".format(c))
      pass

  # print output wires
  arr1 = createoutarr(arr)
  # d = {}
  c = 1
  for i in m[:, COL-1]:
    if i != 0:
      # print("output in_{}".format(c))
      # print("output in_{}".format(c+1))
      # d[int(i)] = [c, c+1]
      v = int(i)
      # print(v)
      # print(arr1)
      arr1[v][0] = int(-1*c)
      arr1[v][1] = int(-1*(c+1))
      c += 2
    else:
      # print("output in_{}".format(c))
      for x in range(COL-1, -1, -1):
        if m[-1, x] == 0:
          continue
        else:
          v = int(m[-1, x])
          if arr1[v][0] < 0:
            arr1[v][0] = int(-1*c)
          else:
            if arr1[v][1] < 0:
              arr1[v][1] = int(-1*c)


  # instantiate flops and meanwhile create list of wires
  d = {}

  for i in range(1, count):
    # get the inputs from arr
    # get the outputs from arr1
    # wires are named wire_srcflop_destflop
    # if srcflop is negative -- wire_in(value)_destflop
    w1 = "w_{}_{}".format(arr[i][0], i) if ( arr[i][0] > 0) else "in_{}".format(int(-1*arr[i][0]))
    w2 = "w_{}_{}".format(arr[i][1], i) if ( arr[i][1] > 0) else "in_{}".format(int(-1*arr[i][1]))
    w3 = "w_{}_{}".format(i, arr1[i][0]) if ( arr1[i][0] > 0) else "out_{}".format(-1*int(arr1[i][0]))
    w4 = "w_{}_{}".format(i, arr1[i][1]) if ( arr1[i][1] > 0) else "out_{}".format(-1*int(arr1[i][1]))
    d[w1] = 1
    d[w2] = 1
    d[w3] = 1
    d[w4] = 1
    print("twotwomux flop{} (.d1({}), .d2({}), .q1({}), .q2({}), .sel(sel{}))".format(i, w1, w2, w3, w4, i))

  for key, value in d.items():
    if key.startswith("w_"):
      # print("wire {}".format(key))
      pass

if __name__ == "__main__":
  m, count, arr = do(32)
  print(m)
  createcod(m, count, arr)
