from sympy import factorint

n = 26929046846473124003532832568969842074333194427020631396710179649912560295145863945660807125690267613214652288231147603980768143952543627803505415923151617876169586802683985305849281212776088716710873907785486324774950164184750173792686541883840405023542887241541150989621527136251980260542276387940041941525637947851232157752327471637854379201141828488768863497889369286922766980090638115441849366774888453313813913181187597813384557908206533460192455487291233315951896572541895413661161032591081975203971740902498552786070371247301548619209819126046729272113326171232667012435526954782000575928611642682839117890587

factors = factorint(n)
print(factors)