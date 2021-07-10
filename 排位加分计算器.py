
#使用说明：这是个第五人格排位加分计算器，只需要胜率即可算出您的排位效率（局平均加分）。
#此加分仅供参考，适用于四阶及以上无段位保护分的玩家，不限阵营。
print("#使用说明：这是个第五人格排位加分计算器，只需要胜率即可算出您的排位效率（局平均加分）。")
print("#此加分仅供参考，适用于四阶及以上无段位保护分的玩家，不限阵营。")
print("#q求生者方可能会有1.5分的平均偏差，因为系统忽略了地窖和四出分并设定演绎分默认值为2.5每局。监管者可能有一分偏差。")
list=[100] #possible outcome
lista=[100] #win number
listb=[100] #total win+lost
Flist=[] #Final list
b=1
while b<101:
    a=0
    while a<b:
        r=round(10000*a/b)/100
        list.append(r)
        lista.append(a)
        listb.append(b)
        a+=1
    b+=1


#Useless-
def sortlist(list0):
    list0.sort()
    last=list0[-1]
    for i in range(len(list0)-2,-1,-1):
        if list0[i]==last:
            list0.remove(list0[i])
        else:
            last=list0[i]
    return list0
#-

print(list)
print(lista)
print(listb)
blist=sorted(list)
k=float(input("胜率？"))
w=list.index(k) #find input from total
P=list.count(k)
print("Possible Combinations:",P)
Type=str(input("S(求生者) or H(监管者)"))
print(Type)
count=1
while count<P+1:
    if Type=="S":
        AvF=(lista[w]*count*8-(listb[w]-lista[w])*count*7+(100-count*listb[w])*2+250)/100
    elif Type=="H":
        AvF=(lista[w]*count*12-(listb[w]-lista[w])*count*6+(100-count*listb[w])*3.5)/100
    else:
        AvF=0
    print("Win(赢):",lista[w]*count,"Lost(输):",(listb[w]-lista[w])*count,"Tie(平):",100-count*listb[w],"AvF(平均加分)=",AvF)
    Flist.append(AvF)
    count+=1
print("Max Average:",max(Flist))
print("Min Average:",min(Flist))

