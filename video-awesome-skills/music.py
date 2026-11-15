# Synthesizes a 44 s background track (pads + kick + hats + scene whooshes) -> music.wav
import numpy as np, wave, sys
SR=44100; D=44.0; BPM=112; n=int(SR*D); t=np.arange(n)/SR; beat=60/BPM
out=np.zeros(n)
def note(f): return 440*2**((f-69)/12)
chords=[[57,60,64,69],[53,57,60,65],[48,52,55,60],[55,59,62,67]]  # Am F C G
bar=beat*4
for i in range(int(D/bar)+1):
    s=int(i*bar*SR); e=min(n,int((i+1)*bar*SR))
    if s>=n: break
    tt=np.arange(e-s)/SR; env=np.minimum(1,tt/0.3)*np.minimum(1,(bar-tt)/0.3)
    for m in chords[i%4]:
        f=note(m); out[s:e]+=0.05*env*(np.sin(2*np.pi*f*tt)+0.3*np.sin(2*np.pi*2*f*tt+0.5))
    b=note(chords[i%4][0]-24)
    for k in range(4):  # bass pulse
        bs=s+int(k*beat*SR); be=min(n,bs+int(beat*0.8*SR)); bt=np.arange(be-bs)/SR
        out[bs:be]+=0.12*np.exp(-bt*4)*np.sin(2*np.pi*b*bt)
rng=np.random.default_rng(1)
for k in range(int(D/beat)):
    s=int(k*beat*SR)
    if 2.0<k*beat<D-1.5:  # kick
        L=int(0.25*SR); kt=np.arange(L)/SR; e=min(n,s+L)
        out[s:e]+=(0.5*np.exp(-kt*14)*np.sin(2*np.pi*(50+90*np.exp(-kt*30))*kt))[:e-s]
    h=s+int(beat/2*SR); L=int(0.05*SR)
    if h+L<n: out[h:h+L]+=0.04*rng.standard_normal(L)*np.exp(-np.arange(L)/SR*80)
for c in [4.2,10,17.5,24.5,33,38.5]:  # whoosh at scene cuts
    L=int(0.6*SR); s=int((c-0.35)*SR); w=rng.standard_normal(L)
    w=np.convolve(w,np.ones(30)/30,'same')*np.sin(np.pi*np.arange(L)/L)**2
    out[s:s+L]+=0.35*w
fade=np.minimum(1,t/1.0)*np.minimum(1,(D-t)/2.0); out*=fade
out=out/np.max(np.abs(out))*0.8
with wave.open(sys.argv[1] if len(sys.argv)>1 else 'music.wav','w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes())
