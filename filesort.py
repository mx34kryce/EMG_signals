
import os,natsort

username='jong1334'
directory_path = f"Data/{username}"
list=os.listdir(directory_path)
txt= open(directory_path+'/'+list[0],'r')
value = txt.readlines() 
for i in range(len(value)):
    value[i]=int(value[i].strip())
txt.close()
print(value)
context = {'value':value}