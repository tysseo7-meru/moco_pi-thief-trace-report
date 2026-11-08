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

###read
with open('findsp.l_spam.tcl', mode='br') as fi1:
  l_spam = pickle.load(fi1)
with open('findsp.l_pays.tcl', mode='br') as fi2:
  l_pays = pickle.load(fi2)

print(len(l_spam))
l_spam=list(set(l_spam))
for a in l_spam:
  print(a)



exit()


