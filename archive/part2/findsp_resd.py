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
with open('findsp.dg.tcl', mode='br') as fi3:
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


print(len(l_spam))
l_spam=list(set(l_spam))
for a in l_spam:
  print(a)




exit()


