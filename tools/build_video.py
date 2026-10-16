import subprocess, os, re, glob, math, sys, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SP = "/tmp/claude-0/-home-claude/79301e99-9948-5b0a-bfde-0d11879a8fdc/scratchpad"
TR = "/root/.claude/projects/-home-claude/79301e99-9948-5b0a-bfde-0d11879a8fdc/tool-results"
B = os.path.join(SP, "build")
os.makedirs(B, exist_ok=True)
FPS = 30
TEMPO = float(os.environ.get("TEMPO", "0.94"))
GAP = 0.5
LEAD = 0.8  # lead-in silence for first segment

T = {}
T["s0"] = "What if nothing anyone said could shake you? Not insults, not criticism, not even silence from people you love. Today I'll show you how the Stoics built an unbreakable inner calm, and how you can start building yours tonight. Stay until the end, because the last lesson is the one that changes everything."
T["s1"] = "Think about the last time someone's words ruined your day. A rude comment. A cold message. A look that lasted one second too long. And yet that person has probably forgotten about it already, while you are still carrying it. This is the quiet tax we pay for letting other people hold the remote control of our emotions. The Stoic philosopher Epictetus taught that people are disturbed not by things, but by the views they take of them. In other words, the pain you feel is not coming from outside. It is being built inside, by you."
T["l1"] = "Lesson one. Separate what is yours from what is not. Epictetus said some things are up to us, and some things are not. Your thoughts, your choices, your effort, your response, those belong to you. Other people's opinions, their moods, their reactions, the past, those never will. Most suffering comes from fighting a battle on the wrong side of that line. Try this today. When something bothers you, ask one question: is this up to me? If the answer is no, you are allowed to put it down. Not in defeat, but in wisdom."
T["l2"] = "Lesson two. Create a gap. Between what happens and how you react, there is a small space, sometimes just two seconds. Those two seconds are where your freedom lives. Marcus Aurelius, who ruled the Roman Empire while surrounded by flatterers, schemers and enemies, began his mornings by reminding himself that he would meet difficult people that day. Not to become bitter, but to be ready. When you expect friction, it stops being a shock. Next time you feel anger rising, breathe in slowly, count to five, and only then decide whether this deserves a response at all."
T["l3"] = "Lesson three. An insult is just a gift you are free to refuse. Imagine someone hands you a package full of garbage. You would not open it, thank them, and carry it around all day. Yet that is exactly what we do with harsh words. Seneca wrote that the wise person is not harmed by insults because they do not give the insult the authority to define them. Ask yourself: is there any truth here I can learn from? If yes, keep the lesson and throw away the tone. If no, let it pass, like wind against a mountain."
T["l4"] = "Lesson four. Stop chasing approval. Marcus Aurelius noticed how strange it is that we love ourselves more than anyone, yet care more about other people's opinion of us than our own. Think about it. Most people are too busy worrying about themselves to judge you as harshly as you imagine. And the ones who do judge you rarely walk your road or pay your bills. When you live to be approved of, you hand your peace to strangers. When you live by your own values, no applause can inflate you and no criticism can break you."
T["cta"] = "Quick pause. If you are finding value in this video, take two seconds to subscribe to SelfGrow and hit the like button. It costs you nothing, and it helps us bring you a new lesson of discipline and calm every single day. Now let's keep going, because the next lessons are where it gets practical."
T["l5"] = "Lesson five. Rehearse the hard moments. The Stoics practiced something called premeditation of adversity. Each morning, imagine what could go wrong: a difficult conversation, an unfair word, a plan that falls apart. Not to live in fear, but to remove the shock. A prepared mind does not panic. It adapts. Take two minutes tonight, picture tomorrow's most stressful moment, and decide calmly how you want to respond. When it arrives, you will feel like you have already been there, and you will answer with the calm of someone who has already won the first round inside their own head."
T["l6"] = "Lesson six. Learn the power of silence. You do not need to defend yourself in every argument, correct every false story, or prove your worth to every doubter. Silence is not weakness. It is control. The person who can stay quiet while provoked holds all the power in the room, because nothing can be taken from someone who is not reacting. Epictetus advised that if someone speaks badly of you, you can simply answer that they clearly do not know your other faults, or they would not have mentioned only these. Humor, calm and detachment make a stronger shield than any argument."
T["l7"] = "Lesson seven. Review your day like a wise judge. Seneca ended every evening by asking himself three questions: what bad habit did I improve today, what flaw did I resist, and in what way am I better? No guilt, no drama, just honest reflection. Write down one moment today when you lost your calm, and one moment when you kept it. Over weeks, a pattern appears. You see your triggers, you see your progress, and you slowly become the kind of person whose peace is not a mood, but a character."
T["l8"] = "Lesson eight. Choose your company carefully. Being untouchable does not mean being alone in a cave. It means knowing whose opinion deserves a seat at your table. Spend time with people who challenge you kindly, who tell you the truth, and who grow alongside you. Limit time with those who thrive on drama or drain your energy. Stoicism is not about coldness. It is about protecting your inner calm so that you can show up with more love, more patience, and more strength for the people who truly matter."
T["l9"] = "Lesson nine. Turn the obstacle into the path. Marcus Aurelius wrote that the impediment to action advances action, and what stands in the way becomes the way. Every insult, every setback, every difficult person is training equipment. A weightlifter does not resent the weight, because resistance is how strength is built. The next time life pushes against you, ask what skill this is trying to teach you: patience, courage, clarity, or humility. The moment you see difficulty as a teacher instead of an enemy, it loses half its power over you. And the other half disappears when you act, because action is the best medicine for a worried mind."
T["l10"] = "Lesson ten. Remember how short life is. The Stoics practiced memento mori, the reminder that our time is limited. This is not a dark thought. It is a liberating one. When you remember that your days are numbered, petty arguments suddenly look tiny. That coworker's comment, that cousin's gossip, that stranger's opinion online, none of it deserves a piece of the one life you have. Ask yourself each morning: if this were my last week, would I spend it being upset about this? Most of the time, the answer sets you free instantly. Spend your energy on what builds you, and let the rest fade."
T["ch"] = "So here is your seven day challenge. Day one, sort your worries into what you control and what you do not. Day two, practice the two second pause. Day three, refuse one insult in your mind. Day four, do one thing without seeking approval. Day five, rehearse tomorrow's hardest moment. Day six, stay silent once when you want to react. Day seven, review the week and write down how you have changed. You do not need to become a philosopher. You only need to practice, one small moment at a time."
T["end"] = "Remember, being emotionally untouchable does not mean feeling nothing. It means feeling everything, and still choosing who you become. The storm will come, but you are the mountain. If this video gave you something valuable, please do three small things for me. Subscribe to SelfGrow so you never miss a new lesson. Like this video so more people can find it. And share it with one person who needs this calm today. Tell me in the comments which lesson hit you hardest. Thank you for watching, and I will see you in the next video. Stay strong, stay disciplined, and keep growing."

SEGS = [
    ("s0", "2vtfmv", "71lce0"),
    ("s1", "eejmt6", "wqtjnj"),
    ("l1", "gjpk1x", "5d27ia"),
    ("l2", "jlrf8c", "p6l1ab"),
    ("l3", "su5e9k", "h9rmze"),
    ("l4", "pdfa13", "iw16zf"),
    ("cta", "n3tvxf", "71lce0"),
    ("l5", "erfmfk", "yjkvye"),
    ("l6", "5rjubx", "apbjv1"),
    ("l7", "dprdga", "u6p8cw"),
    ("l8", "5j4wmj", "73d2u0"),
    ("l9", "vvcb6x", "djva3q"),
    ("l10", "a5nqno", "wjab3c"),
    ("ch", "pfpx4n", "wr0y1d"),
    ("end", "l3s2ox", "niryal"),
]


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print("CMD FAILED:", " ".join(cmd)[:300])
        print(r.stderr[-1500:])
        sys.exit(1)
    return r.stdout


def find(suffix_id, ext):
    g = glob.glob(f"{TR}/mcp-Open_router-blob-*-{suffix_id}.{ext}")
    assert len(g) == 1, (suffix_id, g)
    return g[0]


def dur(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", path]).strip())


# ---------- 1. audio ----------
info = []
for sid, pcm, img in SEGS:
    src = find(pcm, "bin")
    raw = os.path.join(B, f"{sid}_raw.wav")
    af = f"atempo={TEMPO},aresample=44100"
    if sid == "s0":
        af += f",adelay={int(LEAD*1000)}"
    af += f",apad=pad_dur={GAP}"
    run(["ffmpeg", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", src, "-af", af, "-ac", "1", raw])
    d = dur(raw)
    target = math.ceil(d * FPS) / FPS
    final = os.path.join(B, f"{sid}.wav")
    run(["ffmpeg", "-y", "-i", raw, "-af", f"apad=whole_dur={target:.4f}", "-t", f"{target:.4f}", final])
    info.append(dict(id=sid, img=find(img, "jpg"), raw=d, dur=target, lead=(LEAD if sid == "s0" else 0.0)))
    print(sid, round(d, 2), round(target, 3))

total = sum(i["dur"] for i in info)
print("TOTAL seconds:", round(total, 1), "=", round(total / 60, 2), "min")
json.dump(info, open(os.path.join(B, "info.json"), "w"), indent=1)

# ---------- 2. title card ----------
bust = Image.open(info[0]["img"]).convert("RGB")
W, H = 1280, 720
card = bust.resize((W, int(bust.height * W / bust.width)), Image.LANCZOS)
card = card.crop((0, 0, W, H)) if card.height >= H else card.resize((W, H))
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
px = ov.load()
for x in range(W):
    a = int(235 * max(0.0, 1 - x / 820) ** 0.8)
    for y in range(H):
        px[x, y] = (0, 0, 0, a)
card = Image.alpha_composite(card.convert("RGBA"), ov)
d = ImageDraw.Draw(card)
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"


def txt(y, s, size, fill, glow=None):
    f = ImageFont.truetype(FB, size)
    if glow:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        gd.text((58, y), s, font=f, fill=glow)
        g = g.filter(ImageFilter.GaussianBlur(14))
        card.alpha_composite(g)
    d2 = ImageDraw.Draw(card)
    d2.text((58, y), s, font=f, fill=fill, stroke_width=3, stroke_fill=(0, 0, 0, 255))


txt(120, "BECOME", 84, (255, 255, 255, 255))
txt(208, "EMOTIONALLY", 90, (255, 255, 255, 255))
txt(310, "UNTOUCHABLE", 90, (255, 212, 0, 255), glow=(177, 101, 255, 255))
# badge
f_b = ImageFont.truetype(FB, 34)
d = ImageDraw.Draw(card)
d.rounded_rectangle((58, 470, 58 + 500, 470 + 64), radius=14, fill=(177, 101, 255, 255))
d.text((58 + 22, 470 + 10), "STOIC LESSONS  |  SELFGROW", font=ImageFont.truetype(FB, 28), fill=(0, 0, 0, 255))
card.convert("RGB").save(os.path.join(B, "card.png"))
card.convert("RGB").save(os.path.join(SP, "thumb_preview.jpg"), quality=92)

# ---------- 3. subtitles ----------
def chunks(text, maxw=7):
    sents = re.split(r"(?<=[.?!:])\s+", text.strip())
    out = []
    for s in sents:
        parts = re.split(r"(?<=,)\s+", s)
        for p in parts:
            w = p.split()
            if not w:
                continue
            n = max(1, math.ceil(len(w) / maxw))
            size = math.ceil(len(w) / n)
            for k in range(0, len(w), size):
                out.append(" ".join(w[k:k + size]))
    # merge very short chunks (<=2 words) into previous
    merged = []
    for c in out:
        if merged and len(c.split()) <= 2 and len(merged[-1].split()) + len(c.split()) <= maxw + 1:
            merged[-1] += " " + c
        else:
            merged.append(c)
    return merged


def ts(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1280", "PlayResY: 720", "WrapStyle: 0", "ScaledBorderAndShadow: yes", "",
       "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Default,Poppins,52,&H00FF65B5,&H000000FF,&H00000000,&H78000000,-1,0,0,0,100,100,0,0,1,4.5,2,2,90,90,48,1",
       "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
t0 = 0.0
for i in info:
    speech_start = t0 + i["lead"]
    speech_end = t0 + i["raw"] - GAP
    cs = chunks(T[i["id"]])
    weights = [len(c) + 6 for c in cs]
    tot = sum(weights)
    t = speech_start
    for c, w in zip(cs, weights):
        seg = (speech_end - speech_start) * w / tot
        a, b = t, t + seg
        ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Default,,0,0,0,,{c}")
        t = b
    t0 += i["dur"]
open(os.path.join(B, "subs.ass"), "w").write("\n".join(ass) + "\n")

# ---------- 4. video clips ----------
def make_clip(img, d, out, zoom_in=True, fade_in=0.0, fade_out=0.4, z0=0.0):
    N = max(1, round(d * FPS))
    z = f"1+0.10*on/{N}" if zoom_in else f"1.10-0.10*on/{N}"
    x = f"(iw-iw/zoom)*({0.35 if zoom_in else 0.65}+{0.3 if zoom_in else -0.3}*on/{N})"
    y = "(ih-ih/zoom)*0.5"
    vf = (f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
          f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s=1280x720:fps={FPS},format=yuv420p")
    if fade_in > 0:
        vf += f",fade=t=in:st=0:d={fade_in}"
    if fade_out > 0:
        vf += f",fade=t=out:st={max(0, d - fade_out):.3f}:d={fade_out}"
    run(["ffmpeg", "-y", "-loop", "1", "-framerate", str(FPS), "-i", img, "-frames:v", str(N), "-vf", vf,
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-r", str(FPS), "-pix_fmt", "yuv420p", out])


clips = []
# title card: first 5 seconds
c0 = os.path.join(B, "clip_card.mp4")
make_clip(os.path.join(B, "card.png"), 5.0, c0, zoom_in=True, fade_in=0.0, fade_out=0.0)
clips.append(c0)
for k, i in enumerate(info):
    d = i["dur"] - (5.0 if i["id"] == "s0" else 0.0)
    out = os.path.join(B, f"clip_{i['id']}.mp4")
    make_clip(i["img"], d, out, zoom_in=(k % 2 == 0), fade_in=(0.0 if i["id"] == "s0" else 0.4), fade_out=(0.4 if i["id"] != "end" else 1.2))
    clips.append(out)
    print("clip", i["id"], round(d, 1), flush=True)

open(os.path.join(B, "vlist.txt"), "w").write("".join(f"file '{c}'\n" for c in clips))
open(os.path.join(B, "alist.txt"), "w").write("".join(f"file '{os.path.join(B, i['id'] + '.wav')}'\n" for i in info))
run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(B, "alist.txt"), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", os.path.join(B, "audio_all.wav")])

# ---------- 5. final encode ----------
OUT = os.path.join(SP, "become_untouchable_01.mp4")
run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(B, "vlist.txt"), "-i", os.path.join(B, "audio_all.wav"),
     "-vf", f"ass={os.path.join(B, 'subs.ass')}", "-c:v", "libx264", "-preset", "medium", "-crf", "27", "-maxrate", "1200k", "-bufsize", "2400k",
     "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", "-shortest", OUT])
print("DONE", OUT, round(os.path.getsize(OUT) / 1e6, 1), "MB", round(dur(OUT), 1), "s")
