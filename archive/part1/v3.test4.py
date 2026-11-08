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
with open('data.pickle1.tcl', mode='br') as fi:
  l_spam = pickle.load(fi)

print(len(l_spam))
l_spam=list(set(l_spam))
print(len(l_scam))

#for a in l_scam:
#  print(a)


exit()


