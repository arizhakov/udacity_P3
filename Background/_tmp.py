'''
def parse_array(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v = re.sub('[*]', '', v)
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    return [v]
    

A = "{* Hydracarina|* Hydrachnellae|* Hydrachnidia}"

print parse_array(A)
'''

def strip_parans(A):
    print "strip A pre", A
    if not (A.find('(') < 0) and (A.find(')') < 0):
        A = (A[:A.find('(')]+A[A.find(')')+1:]).strip()
    print "strip A post", A    
    return A

test = "Tick"
print strip_parans(test)

