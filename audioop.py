# audioop stub voor Python 3.13 compatibiliteit
def bias(fragment, width, bias): return fragment
def mul(fragment, width, factor): return fragment
def tostereo(fragment, width, lfactor, rfactor): return fragment
def tomono(fragment, width, lfactor, rfactor): return fragment
def ratecv(fragment, width, nchannels, inrate, outrate, state, weightA=1, weightB=0): return fragment, state
def lin2lin(fragment, width, newwidth): return fragment
def ulaw2lin(fragment, width): return fragment
def lin2ulaw(fragment, width): return fragment
def alaw2lin(fragment, width): return fragment
def lin2alaw(fragment, width): return fragment
def findfactor(fragment, reference): return 1.0
def findfit(fragment, reference): return 0, 1.0
def findmax(fragment, nframes): return 0
def getsample(fragment, width, index): return 0
def avg(fragment, width): return 0
def avgpp(fragment, width): return 0
def max(fragment, width): return 0
def maxpp(fragment, width): return 0
def minmax(fragment, width): return 0, 0
def rms(fragment, width): return 0
def cross(fragment, width): return 0
def add(fragment1, fragment2, width): return fragment1
def reverse(fragment, width): return fragment
