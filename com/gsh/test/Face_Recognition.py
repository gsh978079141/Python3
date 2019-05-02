string = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
''' Tips: K -> M, O -> Q, E -> G'''
replace1 = ''.join([chr(ord(i) + 2) for i in string])
print(replace1)
replace2 = replace1.replace('"', ' ').replace('{', 'a').replace('|', 'b').replace('0', '.')
print(replace2)
string2 = "map"
print(''.join([chr(ord(i) + 2) for i in string2]))
