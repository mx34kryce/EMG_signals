
import os,natsort

directory_path = f"Data/jong1334"
list=os.listdir(directory_path)
print(list)
sorted_list=natsort.natsorted(list)
print(sorted_list)