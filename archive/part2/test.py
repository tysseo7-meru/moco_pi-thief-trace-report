import v3_11 as v3
import pickle


VTH=999
#VTH=100
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


lp=[]

a="GAEPEDJT2CCQAMULRN5QNMGTOGOZREWESKF245ATYU4FKYCM4SSOBQ67"

lp=getAdr(a,lp)

for p in lp[0][a]:
  print(p)
print("len(lp[0][a])",len(lp[0][a]))

exit()


