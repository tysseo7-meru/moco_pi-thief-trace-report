import v3_11 as v3
import pickle

#l=[{1:[10,100]},{2:[21,234]},{3:[33,321]}]
#for d in l:
#  a=list(d)[0]
#  print(a)
#  print(type(a))
#exit()

'''#############
#a="GDVWOYCULBEYT7TKGZKAO5R4HDOL3MNTJLB2MXZ76CQNUF6KN4HHHMAW" #seo
#a="GCEXIRDHTESXA7ZXZDTS5L7XWTVJOKGACKHURKLI2CYXWQ6E22TWFILW" #test shief
a="GCEXIRDHTESXA7ZXZDTS5L7XWTVJOKGACKHURKLI2CYXWQ6E22TWFILW"
#l=v3.getPaymentsForOneAdr(a,0)
l=v3.getPaymentsForOneAdr(a,48)
for xx in l:
  print(xx)
'''############

#path="from_GING.txt"
#path="from_GING_test.txt"
path="sa2405.txt"
#path="sa2405_test.txt"
with open(path) as f:
  s = f.read()
lg=s.split("\n")
f.close()

print(len(lg))
lg=list(set(lg))
print(len(lg))

lg_org=lg
for aa in lg:
  print(aa[0]+aa[1]+aa[2]+aa[3]+aa[4],aa)

#VTH=0
#VTH=48
#VTH=99
VTH=999
print("### VTH",VTH)


def getAdr (ain,lin):
  for d in lin:
    a=list(d)[0]
    if a == ain :
      return(lin)
 
  ll=v3.getPaymentsForOneAdr(ain,VTH)
  d1={}
  d2={}
  l1=[]
  for xx in ll:
    yy=xx.split(",")
    d1={
      'amount':yy[1],
      'from':  yy[3],
      'to':    yy[5],
      'ut':    yy[9],
      'hush':  yy[11]
    }
    l1.append(d1)
  d2={ain:l1}
  lin.append(d2)
  return(lin)









l_pays=[]
l_spam=[]

def mkPays():
  global l_pays
  global l_spam
  for ii in range(len(lg)):
    print("###",lg[ii])
    #l1=v3.getPaymentsForOneAdr(lg[ii],VTH)
    l_pays=getAdr(lg[ii],l_pays)
    #print(l_pays)
    print(len(l_pays))
    #print(l_pays[0]['GDVWOYCULBEYT7TKGZKAO5R4HDOL3MNTJLB2MXZ76CQNUF6KN4HHHMAW'][0]['to'])
    for dd in l_pays:
      for kk in dd:
        for dp in dd[kk]:
          #l_pays=getAdr(dp['to'],l_pays)  # too hard!
          if lg[ii] != dp['to'] :
            if float(dp['amount']) > VTH:
              l_spam.append(dp['to'])
          #else:
          #  if float(dp['amount']) > VTH:
          #    l_spam.append(dp['from'])
  #print(l_spam)
  #print(l_pays)
  print("len(l_spam)",len(l_spam))
  print("len(l_pays)",len(l_pays))

  #l_spam_u = list(l_spam)
  #print("len(l_spam_u)",len(l_spam_u))
  l_spam=list(set(l_spam))
  print("len(l_spam)",len(l_spam))


def mklg(lg):
  lg_new=[]
  for a in l_spam:
    if a not in lg:
      lg_new.append(a)
  return(lg_new)

def cplist(lin):
  lout=[]
  for ee in lin:
    lout.append(ee)
  return(lout)
  
#ddb={}
l_spam=cplist(lg)
l_pays=[]

#print("lg",lg)
print("len(lg)",len(lg))
mkPays()
#print("lg",lg)
print("len(lg)",len(lg))
lg=mklg(lg)
#print("lg",lg)
print("len(lg)",len(lg))


mkPays()
lg=mklg(lg)
#print("lg",lg)
print("len(lg)",len(lg))








dg={}
for x in l_pays:
  for a in l_spam:
    if a not in x:
      continue
    for yy in x[a]:


      #yy=xx.split(",")
      if a==yy['from'] :   # from a --> to
        sdir='out'
      else:                # from   --> to a
        sdir='in'
      dtmp={}
      ltmp=[]
      if a not in dg:
        ltmp.append(yy['to'])
        dtmp[sdir]=ltmp
        dg[a] = dtmp
      else:
        if sdir in dg[a]:
          ltmp=dg[a][sdir]
          if yy['to'] not in dg[a][sdir]:
            ltmp.append(yy['to'])
            dg[a][sdir]=ltmp
        else:
          ltmp.append(yy['to'])
          dg[a][sdir]=ltmp




#print("### ddb ###")
#print(ddb)
#print("### dg ###")
#print(dg)

'''##############################################
print("###### dg in/out ######")
for k in dg:
  a4=k[0]+k[1]+k[2]+k[3]
  if 'in' in dg[k]:
    a4_in_num = len(dg[k]['in'])
  else:
    a4_in_num = 0
  if 'out' in dg[k]:
    a4_out_num= len(dg[k]['out'])
  else:
    a4_out_num= 0
  print(a4,"in",a4_in_num,"out",a4_out_num)
'''##############################################


with open('findsp.l_spam.tcl', mode='wb') as fo1:
  pickle.dump(l_spam, fo1)

with open('findsp.l_pays.tcl', mode='wb') as fo2:
  pickle.dump(l_pays, fo2)

with open('findsp.dg.tcl', mode='wb') as fo3:
  pickle.dump(dg, fo3)


###read
#with open('data.pickle1.tcl', mode='br') as fi:
#  l_spam = pickle.load(fi)

exit()


