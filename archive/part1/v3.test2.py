import v3_11 as v3
#import v3_test_out_VTH99 as md
import v3_test_out_VTH999 as md

'''#############
#a="GDVWOYCULBEYT7TKGZKAO5R4HDOL3MNTJLB2MXZ76CQNUF6KN4HHHMAW" #seo
#a="GCEXIRDHTESXA7ZXZDTS5L7XWTVJOKGACKHURKLI2CYXWQ6E22TWFILW" #test shief
a="GCEXIRDHTESXA7ZXZDTS5L7XWTVJOKGACKHURKLI2CYXWQ6E22TWFILW"
#l=v3.getPaymentsForOneAdr(a,0)
l=v3.getPaymentsForOneAdr(a,48)
for xx in l:
  print(xx)
'''############


def find_path(dg, start, goal):
    # スタートノードからゴールノードへの経路を見つける
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
    # スタートノードからゴールノードへの経路を見つける（無向グラフ）
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
        
        # 無向グラフのため、逆方向のエッジも考慮する
        for n in dg:
            if node in dg[n].get('out', []) and n not in visited:
                if n == goal:
                    return path + [n]
                queue.append((n, path + [n]))
                visited.add(n)
    
    return None



path="from_GING.txt"
with open(path) as f:
  s = f.read()
lg=s.split("\n")
f.close()

for aa in lg:
  print(aa[0]+aa[1]+aa[2]+aa[3],aa)

dg=md.mk_dg()
print("###### dg ######")
for k in dg:
  a4=k[0]+k[1]+k[2]+k[3]
  a4_in_num = len(dg[k]['in'])
  a4_out_num= len(dg[k]['out'])
  print(a4,"a4_in_num",a4_in_num,"a4_out_num",a4_out_num)
# 経路の探索
'''
print("###### path to GBU7 ######")
start_node = 'GCEXIRDHTESXA7ZXZDTS5L7XWTVJOKGACKHURKLI2CYXWQ6E22TWFILW'
goal_node = 'GBU7PR3VSIWZGQZYOHP6KEUEBJPX4HYN6FMHDB5VQNJ2NNVCWU4D5ANE'
path = find_path(dg, start_node, goal_node)

if path:
    print(f"Path found: {' -> '.join(path)}")
else:
    print("No path found.")
'''

dswap={
  'GCEXIRDHTESXA7ZXZDTS5L7XWTVJOKGACKHURKLI2CYXWQ6E22TWFILW':'xxx',
  'GDNNVSW7C5VVIQNRV4PE36NA3XQ5FZYGKPDFTZ3CYCS6IFWW2LOWBBJ5':'xxx',
  'GC5RUYERW53YKP7BDZ6RRZDODPEP4ZPQ42YLULLWYS2C3VWWZ3DXNNUM':'GBZMQ5P6UFL77AW4WWPJGGPRHD6VQ37D2MS2NBZNSPGSKNKFRJIQJRBS',
  'GAJKWKGIH4SCCEVGF3MW2LPW27ZRCLOTWJMCR3M76UHNAWNKQG6MYMLG':'GB4XPICNOBVR7QMQ3MF6JVAKJMJMYJT4YVWWHLP7V5RD3HOHA34NE3KL',
  'GCIUYHCSXOUDMXOO2VQXNGBLFZAQH5OYB5PHFC5ZESM4INFY7HLKOQJF':'GC5WLUELPULACNIB5OEBH325TZTDTEBUAJ7ULJYUMBPHZMXWFHJUUIDV',
  'GCCX7KWGDYZ2UIGTJZBVQVEI2DP3MVSBKWA3QG24CLETBRTE6BTVJZBG':'GB2Q4LNTSYNZVOYHKX64B64CQFJ4KUKZ3J7FKIYUFSC5GESHGYNKFPUO',
  'xxx':'yyy',
}

dnodir={
  'GBZMQ5P6UFL77AW4WWPJGGPRHD6VQ37D2MS2NBZNSPGSKNKFRJIQJRBS':'GB2Q4LNTSYNZVOYHKX64B64CQFJ4KUKZ3J7FKIYUFSC5GESHGYNKFPUO',
  'GB4XPICNOBVR7QMQ3MF6JVAKJMJMYJT4YVWWHLP7V5RD3HOHA34NE3KL':'GBZMQ5P6UFL77AW4WWPJGGPRHD6VQ37D2MS2NBZNSPGSKNKFRJIQJRBS',
  'xxx':'yyy',
}

print("###### path  ######")
for ii in range(len(lg)):
  for jj in range(len(lg)):
    if ii != jj :
      start_node = lg[ii]
      goal_node=lg[jj]
      print("ii=,",ii,"   jj=",jj)
      print("start_node",start_node)
      print("goal_node ",goal_node)
      if start_node in dnodir or goal_node in dnodir.values():
        print("### ignore direction from",start_node,"to",goal_node)
        path = find_path_undirected(dg, start_node, goal_node)
      else:
        if start_node in dswap or goal_node in dswap.values():
          print("### switch direction from",start_node,"to",goal_node)
          path = find_path(dg, goal_node ,start_node)
        else:
          path = find_path(dg, start_node, goal_node)

      if path:
        print(f"Path found: {' -> '.join(path)}")
        print(type(path))
        print(path)
      else:
        print("### No path found.")
