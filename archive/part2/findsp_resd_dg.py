import v3_11 as v3
import pickle

'''
with open('data.pickle1.tcl', mode='wb') as fo1:
  pickle.dump(l_scam, fo1)

with open('data.pickle2.tcl', mode='wb') as fo2:
  pickle.dump(l_pays, fo2)
'''

#ll=[33,33,2,1,2,0,0,1]
#print(ll)
#ll=list(set(ll))
#for a in ll:
#  print(a)


suf='findsp3'

###read
with open(suf+'.l_spam.tcl', mode='br') as fi1:
  l_spam = pickle.load(fi1)
with open(suf+'.l_pays.tcl', mode='br') as fi2:
  l_pays = pickle.load(fi2)
with open(suf+'.dg.tcl', mode='br') as fi3:
  dg = pickle.load(fi3)

'''
l_spam[n]
  --> spam adres[n]

l_pays
l_pays[0]['GDVWOYCULBEYT7TKGZKAO5R4HDOL3MNTJLB2MXZ76CQNUF6KN4HHHMAW'][0]['to']
l_pays[n][a][m][attr] attr: amount, from, to, ut, hush
  --> one tx of payment data ... all tx of payment in l_pays

dg[a]['out']
  --> a_out ... there is tx 'from a to a_out' ( a=input adr, a_out=output adr )
dg[a]['in']
  --> a_out ... there is tx 'from a_out to a' ( a=input adr, a_out=output adr )

'''

'''
print(len(l_spam))
l_spam=list(set(l_spam))
for a in l_spam:
  print(a)
'''

def find_path(dg, start, goal):
    # Find a path from the start node to the goal node
    stack = [(start, [start])]
    
    while stack:
        (node, path) = stack.pop()
        
        for next_node in dg.get(node, {}).get('out', []):
            if next_node in path:
                continue
            if next_node == goal:
                return path + [next_node]
            else:
                stack.append((next_node, path + [next_node]))
    
    return None

from collections import deque

def find_path_undirected(dg, start, goal):
    # Find a path from a start node to a goal node (undirected graph)
    queue = deque([(start, [start])])
    visited = set()
    
    while queue:
        node, path = queue.popleft()
        visited.add(node)
        
        for next_node in dg.get(node, {}).get('out', []):
            if next_node not in visited:
                if next_node == goal:
                    return path + [next_node]
                queue.append((next_node, path + [next_node]))
                visited.add(next_node)
        
        # Consider opposite edges as well
        for n in dg:
            if node in dg[n].get('out', []) and n not in visited:
                if n == goal:
                    return path + [n]
                queue.append((n, path + [n]))
                visited.add(n)
    
    return None


'''
l=find_path(dg,'GAEPEDJT2CCQAMULRN5QNMGTOGOZREWESKF245ATYU4FKYCM4SSOBQ67','GBSCN5MCGRZIYKKO4RM4GWEDDE4H5D5O4BNAUC5LHDUTPXRJX7Z5XJS3')
print(l)
exit()

l=find_path(dg, 'GA6DL74T6UPEXRYZT4Z6FD7ZWTKJMD63AEAA333ZUJBB6ZJKICBYXFHD', 'GAEPEDJT2CCQAMULRN5QNMGTOGOZREWESKF245ATYU4FKYCM4SSOBQ67')
print(l)
exit()
'''



ii=1
ff=0
print("### check path from dg to GBU7PR3VSIWZGQZYOHP6KEUEBJPX4HYN6FMHDB5VQNJ2NNVCWU4D5ANE ###")

aGBU7="GBU7PR3VSIWZGQZYOHP6KEUEBJPX4HYN6FMHDB5VQNJ2NNVCWU4D5ANE"
print("len(dg)",len(dg))
nn=0
nOK=0
nNG=0
for k in dg:
  nn+=1
  pp=find_path(dg,k,aGBU7)
  #pp=find_path_undirected(dg,k,aGBU7)
  if pp:
      #print(f"Path found: {' -> '.join(pp)}")
      #print(type(pp))
      #print(pp)
      #print(nn,"## ok",v3.sAdr(k),"==>",v3.sAdr(aGBU7))
      nOK+=1
  else:
      #print(nn,"### No path found.",v3.sAdr(k),"==>",v3.sAdr(aGBU7))
      nNG+=1

print("nn",nn)
print("nOK",nOK)
print("nNG",nNG)

#print(l_pays[1])
#print("## len(l_pays[1])",len(l_pays[1]))


print("#####")
ii=0
for d1 in l_pays:
  ii+=1
  ain=0
  aout=0
  for k1 in d1:
    for xx in d1[k1]:
      #print(xx['amount'])
      if k1 == xx['to']: #in
        ain+=float(xx['amount'])
      if k1 == xx['from']: #out
        aout+=float(xx['amount'])
    print(ii,k1,"in",ain,"out",aout)



exit()

