import numpy as np, soundfile as sf
from scipy.signal import lfilter
SR=44100
def note(m): return 440*2**((m-69)/12)
def env(n,a=0.005,d=0.1,s=0.0):
    t=np.arange(n)/SR; return np.where(t<a,t/a,np.exp(-(t-a)/d)*(1-s)+s)
def saw(f,n,det=0):
    t=np.arange(n)/SR; ds=[0] if det==0 else [-det,0,det]
    return sum(2*((t*f*(1+d))%1)-1 for d in ds)/len(ds)
def sq(f,n): t=np.arange(n)/SR; return np.sign(np.sin(2*np.pi*f*t))
def tri(f,n): t=np.arange(n)/SR; return 2*np.abs(2*((t*f)%1)-1)-1
def sine(f,n): t=np.arange(n)/SR; return np.sin(2*np.pi*f*t)
def lp(x,a): return lfilter([a],[1,a-1],x)
def make(fn,bpm,key,major,prog,style,lead,seed,bars=24):
    rng=np.random.default_rng(seed)
    beat=60/bpm; s16=int(beat/4*SR); bl=16*s16; N=bl*bars
    L=np.zeros(N);R=np.zeros(N);duck=np.ones(N)
    def add(x,p,gl=1,gr=1):
        if p>=N: return
        e=min(N,p+len(x)); L[p:e]+=x[:e-p]*gl; R[p:e]+=x[:e-p]*gr
    def kick(n):
        t=np.arange(n)/SR; f=48+130*np.exp(-t*32); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)
    def snare(n):
        t=np.arange(n)/SR; return rng.normal(0,1,n)*np.exp(-t*16)*0.45+np.sin(2*np.pi*185*t)*np.exp(-t*22)*0.35
    def hat(n,o=False):
        t=np.arange(n)/SR; x=rng.normal(0,1,n); x=x-lp(x,0.3); return x*np.exp(-t*(12 if o else 70))*0.22
    scale=[0,2,4,5,7,9,11] if major else [0,2,3,5,7,8,10]
    pent=[0,2,4,7,9] if major else [0,3,5,7,10]
    # motif: 2 bars, 16th grid
    def motif():
        m=[];st=0
        while st<32:
            m.append((st,int(rng.choice(pent))+12*int(rng.choice([0,0,1]))))
            st+=int(rng.choice([2,2,3,4,2,6]))
        return m
    A=motif();B=motif()
    swing = style=="lofi"
    for b in range(bars):
        deg,qual=prog[b%len(prog)]; root=key+deg
        chord=[0,4,7] if qual=="M" else [0,3,7]
        intro=b<2
        for st in range(16):
            p=b*bl+st*s16+(int(s16*0.28) if swing and st%2==1 else 0)
            kpat={"four":st%4==0,"lofi":st in(0,7,10),"trap":st in(0,6,11),"pop":st in(0,6,8,14),"house":st%4==0}[style]
            if kpat and not intro:
                add(kick(int(0.35*SR)),p)
                d=np.minimum(1,0.3+np.arange(int(beat*SR))/(beat*SR)*1.4); e=min(N,p+len(d)); duck[p:e]=np.minimum(duck[p:e],d[:e-p])
            spat={"four":st in(4,12),"lofi":st in(4,12),"trap":st==8,"pop":st in(4,12),"house":st in(4,12)}[style]
            if spat and b>=1: add(snare(int(0.25*SR))*(0.6 if style=="lofi" else 0.8),p)
            if b>=1:
                if style=="trap":
                    if st%2==0 or (b%2==1 and st>=12): add(hat(int(0.06*SR))*0.7,p,0.8,1)
                elif style=="house":
                    if st%4==2: add(hat(int(0.15*SR),True),p,0.8,1)
                    elif st%2==0: add(hat(int(0.05*SR))*0.5,p)
                elif st%2==0: add(hat(int(0.08*SR),st%4==2)*(0.9 if st%4==2 else 0.55),p,1,0.7)
            # bass
            bpat={"four":st%2==0,"lofi":st in(0,7,10),"trap":st in(0,6,11),"pop":st in(0,3,6,8,11,14),"house":st%4==2}[style]
            if bpat:
                n=int(s16*(3 if style in("lofi","trap") else 1.8)); f=note(root-24+(12 if style=="four" and st%4==2 else 0))
                w=sine(f,n)*0.8+lp(saw(f,n),0.08)*0.5 if style in("trap","lofi") else lp(saw(f,n),0.12)
                add(w*env(n,0.003,0.18 if style!="trap" else 0.5,0.3)*0.55,p)
        # chords
        n=bl; pad=0
        for iv in chord+[12]:
            if style=="lofi": pad=pad+tri(note(root+iv),n)*0.6+sine(note(root+iv),n)
            else: pad=pad+saw(note(root+iv-12),n,0.006)
        pad=lp(pad,0.04 if style!="lofi" else 0.08)*(0.09 if style!="lofi" else 0.07)
        if style=="pop":  # stabs
            for st in (0,3,6,10,12):
                x=lp(sum(saw(note(root+iv),s16*2,0.004) for iv in chord),0.2)*env(s16*2,0.003,0.12)*0.12; add(x,b*bl+st*s16)
        add(pad*np.minimum(1,np.arange(n)/(0.02*SR)),b*bl)
        # lead
        if b>=2 and lead!="none":
            mot=A if (b//2)%2==0 else B
            off=(b%2)*16
            for st,iv in mot:
                if off<=st<off+16:
                    p=b*bl+(st-off)*s16; n=int(s16*2.5); f=note(key+12+iv)
                    if lead=="pluck": x=lp(sq(f,n)*0.5+saw(f*2,n)*0.3,0.25)*env(n,0.002,0.09)
                    elif lead=="bell": x=(sine(f*2,n)+0.5*sine(f*4,n)*env(n,0.001,0.05))*env(n,0.002,0.25)*0.7
                    elif lead=="saw": x=lp(saw(f,n,0.01),0.3)*env(n,0.004,0.15,0.2)
                    elif lead=="keys": x=(tri(f,n)+0.3*sine(f*2,n))*env(n,0.003,0.3)
                    elif lead=="arp":
                        x=np.zeros(n)
                    add(x*0.2,p,1,0.75); add(x*0.08,p+int(s16*3),0.4,1)
            if lead=="arp":
                for st in range(16):
                    iv=(chord+[12])[st%4]; n=int(s16*1.2); f=note(root+12+iv)
                    add(lp(saw(f,n),0.3)*env(n,0.002,0.07)*0.13,b*bl+st*s16,1 if st%2 else 0.6,0.6 if st%2 else 1)
    pump=0.55+0.45*duck if style in("four","house","pop") else 0.8+0.2*duck
    L*=pump;R*=pump
    m=np.stack([L,R],1); m/=np.max(np.abs(m))*1.1; m=np.tanh(m*1.5)/np.tanh(1.5)
    sf.write(fn,m.astype(np.float32),SR); print(fn,round(N/SR,1))
M,m="M","m"
make("m1.wav",124,57,False,[(0,m),(-4,M),(3,M),(-2,M)],"four","pluck",11)          # EDM Am
make("m2.wav",84,62,False,[(0,m),(-2,M),(-4,M),(-5,m)],"lofi","keys",22)           # lofi Dm
make("m3.wav",116,60,True,[(0,M),(7,M),(9,m),(5,M)],"pop","bell",33)              # pop C
make("m4.wav",140,54,False,[(0,m),(-4,M),(-2,M),(-5,m)],"trap","bell",44)          # trap F#m
make("m5.wav",108,64,False,[(0,m),(-4,M),(-7,M),(-2,M)],"four","arp",55)           # synthwave Em
make("m6.wav",132,62,True,[(5,M),(7,M),(4,m),(9,m)],"pop","saw",66)               # anime royal road D
make("m7.wav",120,55,False,[(0,m),(-4,M),(-2,M),(-7,M)],"house","keys",77)         # house Gm
make("m8.wav",128,58,True,[(5,M),(7,M),(4,m),(9,m)],"four","pluck",88)            # jpop Bb
