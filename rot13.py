#!/usr/bin/env python3
# rot13: comparison of rot13 algorithms.
# Copyright Tom Vincent <http://www.tlvince.com/contact/>

# The Zen of Python from this.py
s = """Gur Mra bs Clguba, ol Gvz Crgref

Ornhgvshy vf orggre guna htyl.
Rkcyvpvg vf orggre guna vzcyvpvg.
Fvzcyr vf orggre guna pbzcyrk.
Pbzcyrk vf orggre guna pbzcyvpngrq.
Syng vf orggre guna arfgrq.
Fcnefr vf orggre guna qrafr.
Ernqnovyvgl pbhagf.
Fcrpvny pnfrf nera'g fcrpvny rabhtu gb oernx gur ehyrf.
Nygubhtu cenpgvpnyvgl orngf chevgl.
Reebef fubhyq arire cnff fvyragyl.
Hayrff rkcyvpvgyl fvyraprq.
Va gur snpr bs nzovthvgl, ershfr gur grzcgngvba gb thrff.
Gurer fubhyq or bar-- naq cersrenoyl bayl bar --boivbhf jnl gb qb vg.
Nygubhtu gung jnl znl abg or boivbhf ng svefg hayrff lbh'er Qhgpu.
Abj vf orggre guna arire.
Nygubhtu arire vf bsgra orggre guna *evtug* abj.
Vs gur vzcyrzragngvba vf uneq gb rkcynva, vg'f n onq vqrn.
Vs gur vzcyrzragngvba vf rnfl gb rkcynva, vg znl or n tbbq vqrn.
Anzrfcnprf ner bar ubaxvat terng vqrn -- yrg'f qb zber bs gubfr!"""

def modulo():
    """Implementation using modulo operation.

    @author: Tim Peters (from this.py)
    """
    d = {}
    for c in (65, 97):
        for i in range(26):
            d[chr(i+c)] = chr((i+13) % 26 + c)
    return "".join([d.get(c, c) for c in s])

def transTable(r=13):
    """Implementation using translation table"""
    import string
    alpha = string.ascii_uppercase + string.ascii_lowercase
    rot13 = alpha[r:r*2] + alpha[r-r:r] + alpha[r*3:r*4] + alpha[r*2:r*3]
    table = bytes.maketrans(alpha.encode(), rot13.encode())
    return bytes.translate(s.encode(), table).decode()

if __name__ == '__main__':
    """Compare the runtimes"""
    from timeit import Timer
    m = Timer("modulo()", "from __main__ import modulo")
    t = Timer("transTable()", "from __main__ import transTable")
    a = m.timeit(1000)
    b = t.timeit(1000)
    print(a)
    print(b)
