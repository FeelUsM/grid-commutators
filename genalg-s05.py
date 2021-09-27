k = [[" 1 ", " 1 ", " 1 ", " 1 "], 
     [" 1 ", " 1 ", " i_", "-i_"], 
     [" 1 ", "-i_", " 1 ", " i_"], 
     [" 1 ", " i_", "-i_", " 1 "]]


n = [[" 1", "cx", "cy", "cz"], 
     ["cx", " 1", "cz", "cy"], 
     ["cy", "cz", " 1", "cx"], 
     ["cz", "cy", "cx", " 1"]]

c = ["1","cx","cy","cz"]
s = ["1","sx","sy","sz"]
rules = '\n'.join(c[i]+'*'+s[j]+' = '+
		  k[i][j]+'*'+n[j][i]+';' 
       for i in range(1,4) for j in range(1,4))
print()#koef symbols
print(' '.join(c[1:]))
print(' '.join(s[1:]))
print(rules)
print('---')
print()#koef symbol rules
