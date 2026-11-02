import subprocess,os,re,numpy as np,soundfile as sf
from kokoro_onnx import Kokoro
S=os.path.dirname(os.path.abspath(__file__))
KK=Kokoro(f"{S}/kokoro/kokoro-v1.0.onnx",f"{S}/kokoro/voices-v1.0.bin")
# Voces elegidas por Xavi: chico = muestra 06 (em_santa), chica = muestra 12 (mezcla ef_dora+af_heart)
SRC=os.environ.get("SRC_VIDEO",f"{S}/in.mp4"); FONTS=f"{S}/fonts"; LOGO=f"{S}/logo.png"
SUBS=[("Manga Tracker","Manga Tráker"),("trackear","trakear"),("manhwas","manjuas"),("manhwa","manjua"),("manhua","manjúa"),
      ("top tier","top táier"),("Play Store","Plei Stor"),("POV:","")]
def to_say(t):
    for a,b in SUBS: t=re.sub(a,b,t,flags=re.I)
    return t
def tts(text,voice,fn):
    v="em_santa" if voice=="chico" else 0.5*KK.get_voice_style("ef_dora")+0.5*KK.get_voice_style("af_heart")
    a,sr=KK.create(to_say(text),voice=v,speed=1.0,lang="es")
    thr=0.02*np.max(np.abs(a)); idx=np.where(np.abs(a)>thr)[0]
    a=a[max(0,idx[0]-int(0.02*sr)):idx[-1]+int(0.06*sr)]
    sf.write(fn,a,sr); return len(a)/sr
def ts(t,srt=False):
    t=max(0,t); h=int(t//3600); m=int(t%3600//60); s=t%60
    if srt: return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s%1)*1000))%1000:03d}"
    return f"{h}:{m:02d}:{s:05.2f}"
HDR="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,MTBlack,112,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00E43F7B,0,0,0,0,100,100,0,0,1,10,7,2,40,40,600,1
Style: Title,Luckiest Guy,84,&H00FFFFFF,&H00FFFFFF,&H00E43F7B,&H00000000,0,0,0,0,100,100,2,0,3,22,0,8,40,40,210,1
Style: End1,Luckiest Guy,128,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,3,0,1,9,6,5,40,40,0,1
Style: End2,Luckiest Guy,86,&H004DE1FF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,2,0,1,8,5,5,40,40,0,1
Style: End3,MTBlack,58,&H00FFFFFF,&H00FFFFFF,&H00E43F7B,&H00000000,0,0,0,0,100,100,0,0,3,20,0,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
def word_groups(show):
    words=show.split(); g=[];cur=[]
    for w in words:
        if cur and len(" ".join(cur+[w]))>12: g.append(cur); cur=[]
        cur.append(w)
        if w[-1] in ",.!?:…": g.append(cur); cur=[]
    if cur: g.append(cur)
    return g
def weight(w): return len(re.sub(r"[^\wáéíóúñü]","",w,flags=re.I))+1.5+(4 if w[-1] in ",.!?…" else 0)
def make(name,title,scenes,end_show,voice,music,outdir):
    d=f"{S}/build/{name}"; os.makedirs(d,exist_ok=True); os.makedirs(outdir,exist_ok=True)
    items=scenes+[(None,None,end_show)]
    t=0.3; plan=[]; ev=[]; srt=[]
    for i,(a,b,show) in enumerate(items):
        w=f"{d}/{i}.wav"; ld=tts(show,voice,w)
        last = a is None
        need=max(ld+0.25,1.0)+(0.3 if i==0 else 0)+(1.2 if last else 0)
        start=t if i>0 else 0.3
        plan.append((a,b,need,start,ld))
        # karaoke events
        groups=word_groups(show); allw=[w for g in groups for w in g]
        tot=sum(weight(x) for x in allw); c=start
        for g in groups:
            gt=[]; 
            for x in g: dw=ld*weight(x)/tot; gt.append((c,c+dw,x)); c+=dw
            gs,ge=gt[0][0],gt[-1][1]
            srt.append((gs,ge," ".join(g)))
            for k,(ws,we,x) in enumerate(gt):
                parts=[]
                for j,(_,_,y) in enumerate(gt):
                    y=y.upper()
                    if j==k: parts.append("{\\c&H004DE1FF&\\fscx100\\fscy100\\t(0,90,\\fscx116\\fscy116)\\t(90,180,\\fscx108\\fscy108)}"+y+"{\\c&H00FFFFFF&\\fscx100\\fscy100}")
                    else: parts.append(y)
                pop="{\\fad(0,0)}" 
                if k==0: pop="{\\t(0,80,\\fscx104\\fscy104)\\t(80,160,\\fscx100\\fscy100)}"
                if not last: ev.append(f"Dialogue: 1,{ts(ws)},{ts(we if k<len(gt)-1 else ge+0.12)},Sub,,0,0,0,,{pop}"+" ".join(parts))
        t=start+need if i>0 else 0.3+need-0.3
        if i==0: t=need
    total=t
    endt=plan[-1][3]-0.05
    # title (two lines with |)
    tl=title.replace("|","\\N")
    ev.insert(0,f"Dialogue: 2,{ts(0)},{ts(endt)},Title,,0,0,0,,{{\\fad(150,0)\\t(0,200,\\fscx106\\fscy106)\\t(200,350,\\fscx100\\fscy100)}}{tl}")
    ev.append(f"Dialogue: 3,{ts(endt+0.1)},{ts(total)},End1,,0,0,0,,{{\\pos(540,1060)\\fad(150,0)\\fscx70\\fscy70\\t(0,220,\\fscx108\\fscy108)\\t(220,350,\\fscx100\\fscy100)}}MANGA TRACKER")
    ev.append(f"Dialogue: 3,{ts(endt+0.35)},{ts(total)},End2,,0,0,0,,{{\\pos(540,1200)\\fad(150,0)}}GRATIS EN PLAY STORE")
    ev.append(f"Dialogue: 3,{ts(endt+0.7)},{ts(total)},End3,,0,0,0,,{{\\pos(540,1340)\\fad(150,0)\\t(0,600,\\fscx106\\fscy106)\\t(600,1200,\\fscx100\\fscy100)}}ENLACE EN MI PERFIL")
    open(f"{d}/s.ass","w").write(HDR+"\n".join(ev)+"\n")
    with open(f"{outdir}/{name}.srt","w") as R:
        n=0
        for (a,b,x) in srt:
            if a>=endt: continue
            n+=1; R.write(f"{n}\n{ts(a,1)} --> {ts(b,1)}\n{x}\n\n")
    # video
    fc=[];labels=[];prev=None
    for i,(a,b,need,start,ld) in enumerate(plan):
        if a is None:
            a,b=prev[1]-0.05,prev[1]
            fc.append(f"[0:v]trim={b-1.2}:{b},setpts=PTS-STARTPTS,fps=30,reverse,trim=end_frame=1,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={need+0.2},trim=0:{need},setpts=PTS-STARTPTS,boxblur=8:1,eq=brightness=-0.32:saturation=0.7[p{i}]")
        else:
            L=b-a; f=L/need
            if f>=1:
                sp=min(f,2.2); fc.append(f"[0:v]trim={a}:{a+need*sp},setpts=(PTS-STARTPTS)/{sp},fps=30,trim=0:{need},setpts=PTS-STARTPTS[p{i}]")
                prev=(a,a+need*sp)
            else:
                sl=min(1/f,1.35); fc.append(f"[0:v]trim={a}:{b},setpts={sl}*(PTS-STARTPTS),fps=30,tpad=stop_mode=clone:stop_duration={need},trim=0:{need},setpts=PTS-STARTPTS[p{i}]")
                prev=(a,b)
        labels.append(f"[p{i}]")
    n=len(labels)
    fc.append("".join(labels)+f"concat=n={n}:v=1:a=0,split[a][b]")
    fc.append("[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=28:2,eq=brightness=-0.28:saturation=1.3[bg]")
    fc.append("[b]crop=iw:ih-34:0:34,scale=-2:1920:flags=lanczos,eq=contrast=1.04:saturation=1.08,unsharp=5:5:0.6[fg]")
    fc.append(f"[bg][fg]overlay=(W-w)/2:0[base]")
    fc.append(f"[{n+1}:v]scale=420:420,format=rgba[lg]")
    fc.append(f"[base][lg]overlay=x=(W-w)/2:y=480:enable='gte(t,{endt+0.05})',subtitles={d}/s.ass:fontsdir={FONTS}[v]")
    ins=[]
    for i in range(len(items)):
        ins+=["-i",f"{d}/{i}.wav"]
    fc2=[]
    for i,(_,_,_,start,_) in enumerate(plan):
        fc2.append(f"[{n+2+i}:a]aresample=44100,adelay={int(start*1000)}:all=1[a{i}]")
    fc2.append("".join(f"[a{i}]" for i in range(len(items)))+f"amix=inputs={len(items)}:normalize=0,apad,atrim=0:{total},asplit[vo][sc]")
    fc2.append(f"[{n+2+len(items)}:a]atrim=0:{total},afade=t=in:d=0.4,afade=t=out:st={total-1.3}:d=1.3,volume=0.32[mu]")
    fc2.append("[mu][sc]sidechaincompress=threshold=0.02:ratio=5:attack=15:release=350:makeup=1[mud]")
    fc2.append("[vo]volume=1.0[vo2];[vo2][mud]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[au]")
    # inputs: 0 src, then n+1 logo index must be n+1 -> we place n dummy? fix ordering below
    cmd=["ffmpeg","-v","error","-y","-i",SRC]
    # pad inputs so logo is index n+1: add n copies? simpler: re-index
    fc_all=";".join(fc+fc2)
    fc_all=fc_all.replace(f"[{n+1}:v]","[1:v]")
    for i in range(len(items)): fc_all=fc_all.replace(f"[{n+2+i}:a]",f"[{2+i}:a]")
    fc_all=fc_all.replace(f"[{n+2+len(items)}:a]",f"[{2+len(items)}:a]")
    cmd+=["-loop","1","-i",LOGO]+ins+["-stream_loop","-1","-i",music,"-filter_complex",fc_all,"-map","[v]","-map","[au]","-t",f"{total:.2f}",
         "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-r","30","-c:a","aac","-b:a","192k","-movflags","+faststart",f"{outdir}/{name}.mp4"]
    subprocess.run(cmd,check=True)
    return total
