#motorcycles=['honda','yamaha','suzuki']
#print(motorcycles)
#motorcycles[0]='ducati'
#print(motorcycles)
#motorcycles.append('ducati')
#print(motorcycles)
motorcycles=[]
motorcycles.append('honda');
motorcycles.append('yamaha');
motorcycles.append('suzuki')
print(motorcycles)
motorcycles.insert(0,'ducati')
print(motorcycles)
#el motorcycles[0]
#print(motorcycles)
#del motorcycles[1]
#print(motorcycles)
#last_woned=motorcycles.pop()
#print("The last motorcycles i owned was a "+last_woned.title()+".")
#first_owned=motorcycles.pop(0)
#print("The first motorcycles i owned was a "+first_owned.title()+".")
#print(motorcycles)

motorcycles.remove('ducati')
print(motorcycles)

temp=motorcycles.index(0)
print(temp)
