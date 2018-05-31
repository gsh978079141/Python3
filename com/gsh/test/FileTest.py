myfile=open("/Volumes/GSH/Python/python_test/test.txt",'r+',encoding='utf-8')
myfile.writelines('2')
print(myfile.readlines())
