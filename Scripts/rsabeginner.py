from Crypto.Util.number import inverse

e = 65537
c = 36750775360709769054416477187492778112181529855266342655304
n = 722701705953209869350758464900325184734255523491631018301919
#find p and q in factordb from n

p = 892582974910679288224965877067
q = 809674535888980601722190167357
# the formula is phi = (p -1) * (q - 1)
phi = (p - 1 ) * (q - 1)
# now we don't know d 
d = inverse(e, phi)
m = pow(c, d, n)
#if you print it, it will be in number. now we can print it in hex
print(m)
var = hex(m)[2:]
print(bytes.fromhex(var).decode('utf-8'))

