"""Thème Original Laptop : showroom violet nuit, lumière lilas, typo Syne + Manrope.

Les sélecteurs commençant par `.vt ` sont préfixés par `.stApp` à l'injection
pour l'emporter sur les styles par défaut de Streamlit.
"""

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Syne:wght@600;700;800&display=swap');
:root{--ink:#0D0618;--ink-2:#1A0B33;--violet:#7C3AED;--violet-d:#5B21B6;--violet-l:#A78BFA;--lilac:#F7F5FC;--lilac-2:#E9E3F7;--muted:#5F5775;--pink:#FF4D9D;--amber:#FFB86B;--wa:#128C54;--wa-dk:#0E7544;--sold:#B42318;}

/* ---- Cadre Streamlit ---- */
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],section.main{scroll-behavior:smooth;}
[data-testid="stAppViewContainer"]{overflow-x:hidden;}
.stApp{background:var(--lilac);color:var(--ink);}
.stApp,.stApp p,.stApp label,.stApp input,.stApp textarea,.stApp button,.stApp li,.stApp a,.stApp [data-baseweb="select"] *{font-family:'Manrope',system-ui,-apple-system,'Segoe UI',sans-serif;}
.stApp h1,.stApp h2,.stApp h3,.stApp h4{font-family:'Syne','Manrope',system-ui,sans-serif;}
header[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stSidebar"],[data-testid="collapsedControl"],[data-testid="stSidebarCollapsedControl"],#MainMenu,footer{display:none !important;}
.block-container{max-width:1180px;padding:0 1.25rem 0 !important;}
.stApp [data-testid="stVerticalBlock"]{gap:.9rem;}
.stApp [data-testid="stElementContainer"]:has(> [data-testid="stMarkdown"] style){display:none !important;}
.vt [data-testid="stHeaderActionElements"]{display:none !important;}

/* ---- Widgets ---- */
.stApp [data-testid="stWidgetLabel"] p,.stApp label p{font-weight:700;color:var(--ink);font-size:.9rem;}
.stApp [data-baseweb="input"],.stApp [data-baseweb="base-input"],.stApp [data-baseweb="textarea"],.stApp [data-baseweb="select"] > div{border-radius:14px !important;border-color:#D5CBEC !important;background:#fff !important;}
.stApp [data-baseweb="input"]:focus-within,.stApp [data-baseweb="textarea"]:focus-within,.stApp [data-baseweb="select"] > div:focus-within{border-color:var(--violet) !important;}
.stApp [data-testid="stForm"] [data-baseweb="input"],.stApp [data-testid="stForm"] [data-baseweb="base-input"],.stApp [data-testid="stForm"] [data-baseweb="textarea"],.stApp [data-testid="stForm"] [data-baseweb="select"] > div{background:var(--lilac) !important;}
.stApp [data-testid="stForm"]{background:#fff;border:1px solid var(--lilac-2);border-radius:24px;padding:1.5rem;}
.stApp .stButton > button,.stApp [data-testid="stFormSubmitButton"] > button{min-height:48px;border-radius:999px;font-weight:700;border:1.5px solid var(--ink);background:#fff;color:var(--ink);}
.stApp .stButton > button:hover,.stApp [data-testid="stFormSubmitButton"] > button:hover{border-color:var(--violet);background:var(--lilac-2);color:var(--ink);}
.stApp button[kind^="primary"],.stApp button[data-testid*="primary"]{background:var(--violet);border-color:var(--violet);color:#fff;}
.stApp button[kind^="primary"] p,.stApp button[data-testid*="primary"] p{color:#fff;}
.stApp button[kind^="primary"]:hover,.stApp button[data-testid*="primary"]:hover{background:var(--violet-d);border-color:var(--violet-d);color:#fff;}
.stApp button:focus-visible,.stApp a:focus-visible,.stApp summary:focus-visible{outline:3px solid var(--violet);outline-offset:2px;}

/* ---- Boutons maison ---- */
/* ---- Champs (Streamlit récent : react-aria) ---- */
.stApp [data-testid="stTextInputRootElement"],.stApp [data-testid="stTextAreaRootElement"],.stApp [data-testid="stNumberInputContainer"],.stApp [data-testid="stSelectbox"] [role="group"]{border-radius:14px !important;border:1px solid #D5CBEC !important;background:#fff !important;}
.stApp [data-testid="stTextInputRootElement"]:focus-within,.stApp [data-testid="stTextAreaRootElement"]:focus-within,.stApp [data-testid="stNumberInputContainer"]:focus-within,.stApp [data-testid="stSelectbox"] [role="group"]:focus-within{border-color:var(--violet) !important;}
.stApp [data-testid="stForm"] [data-testid="stTextInputRootElement"],.stApp [data-testid="stForm"] [data-testid="stTextAreaRootElement"],.stApp [data-testid="stForm"] [data-testid="stNumberInputContainer"],.stApp [data-testid="stForm"] [data-testid="stSelectbox"] [role="group"]{background:var(--lilac) !important;}

.vt .btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;min-height:48px;padding:0 1.5rem;border-radius:999px;font-weight:700;font-size:1rem;text-decoration:none !important;border:1.5px solid transparent;transition:background .15s,border-color .15s,color .15s;}
.vt .btn-block{display:flex;width:100%;}
.vt .btn-sm{min-height:40px;padding:0 1.15rem;font-size:.92rem;}
.vt .btn-violet{background:var(--violet);color:#fff !important;}
.vt .btn-violet:hover{background:var(--violet-d);}
.vt .btn-white{background:#fff;color:var(--ink) !important;}
.vt .btn-white:hover{background:var(--lilac-2);}
.vt .btn-wa{background:var(--wa);color:#fff !important;}
.vt .btn-wa:hover{background:var(--wa-dk);}
.vt .btn-ghost{background:transparent;color:#fff !important;border-color:rgba(255,255,255,.35);}
.vt .btn-ghost:hover{border-color:#fff;}
.vt .btn-line{background:#fff;color:var(--ink) !important;border-color:var(--ink);}
.vt .btn-line:hover{background:var(--lilac-2);}
.vt .nav a:focus-visible,.vt .hero a:focus-visible,.vt .foot a:focus-visible,.vt .band a:focus-visible{outline-color:#fff;}

/* ---- Navigation pilule flottante ---- */
.fb{width:100vw;margin-left:calc(50% - 50vw);}
.vt .nav{position:fixed;top:14px;left:50%;transform:translateX(-50%);width:min(1120px,calc(100% - 24px));z-index:999;background:rgba(13,6,24,.92);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.12);border-radius:999px;}
.vt .nav-in{height:60px;padding:0 .7rem 0 1.4rem;display:flex;align-items:center;gap:1.8rem;}
.vt .brand{display:flex;align-items:center;gap:.65rem;color:#fff !important;font-family:'Syne','Manrope',sans-serif;font-weight:800;font-size:1.1rem;letter-spacing:-.01em;text-decoration:none !important;margin-right:auto;}
.vt .brand i{display:grid;place-items:center;width:30px;height:30px;border-radius:10px;background:linear-gradient(135deg,var(--violet),var(--pink));font-style:normal;font-size:.75rem;color:#fff;}
.vt .nav-links{display:flex;gap:1.6rem;}
.vt .nav-links a{color:#CFC6E6 !important;font-weight:600;text-decoration:none !important;font-size:.93rem;}
.vt .nav-links a:hover{color:#fff !important;}

/* ---- Hero ---- */
.vt .hero{position:relative;overflow:hidden;color:#fff;padding:9rem 0 3.5rem;background:radial-gradient(55% 75% at 82% 25%,rgba(124,58,237,.6),transparent 62%),radial-gradient(40% 55% at 8% 95%,rgba(255,77,157,.28),transparent 62%),var(--ink);}
.vt .hero-in{max-width:1180px;margin:0 auto;padding:0 1.25rem;display:grid;grid-template-columns:1.05fr .95fr;gap:2rem;align-items:center;}
.vt .hero h1{font-size:clamp(2.3rem,5.4vw,4.5rem);line-height:1.03;letter-spacing:-.025em;font-weight:800;margin:0;padding:0;color:#fff;}
.vt .hero h1 span{display:block;}
.vt .hero h1 .soft{color:var(--violet-l);}
.vt .hero .lead{font-size:clamp(1.02rem,1.8vw,1.22rem);color:#CFC6E6;max-width:32em;margin:1.4rem 0 2rem;line-height:1.55;}
.vt .hero-cta{display:flex;flex-wrap:wrap;gap:.75rem;}
.vt .brands{max-width:1180px;margin:3.2rem auto 0;padding:0 1.25rem;display:flex;flex-wrap:wrap;align-items:center;gap:.55rem;}
.vt .brands b{color:#CFC6E6;font-weight:600;font-size:.88rem;margin-right:.6rem;}
.vt .brands span{border:1px solid rgba(255,255,255,.2);color:#fff;border-radius:999px;padding:.35rem .9rem;font-weight:600;font-size:.88rem;}

/* ---- Appareils dessinés en CSS ---- */
.vt .stage{position:relative;height:430px;}
.vt .laptop{position:absolute;right:0;top:30px;width:min(100%,440px);}
.vt .lid{aspect-ratio:16/10;background:#08030f;border:1px solid rgba(255,255,255,.18);border-radius:18px 18px 6px 6px;padding:10px;box-shadow:0 40px 90px rgba(124,58,237,.45);}
.vt .screen{position:relative;height:100%;border-radius:9px;overflow:hidden;background:radial-gradient(circle at 25% 30%,var(--amber),transparent 42%),radial-gradient(circle at 72% 62%,var(--pink),transparent 48%),linear-gradient(135deg,#4C1D95,#7C3AED);}
.vt .screen i{position:absolute;display:block;border-radius:6px;background:rgba(255,255,255,.22);backdrop-filter:blur(6px);}
.vt .screen .w1{left:8%;top:12%;width:34%;height:26%;}
.vt .screen .w2{left:46%;top:20%;width:42%;height:34%;background:rgba(255,255,255,.3);}
.vt .screen .w3{left:8%;bottom:10%;width:80%;height:9%;border-radius:999px;}
.vt .base{height:13px;margin:0 -5%;background:linear-gradient(#D8D0EE,#8F84AD);border-radius:0 0 22px 22px;}
.vt .phone{position:absolute;left:3%;bottom:0;width:150px;aspect-ratio:9/19;background:#08030f;border:1px solid rgba(255,255,255,.25);border-radius:32px;padding:7px;transform:rotate(-7deg);box-shadow:0 35px 70px rgba(0,0,0,.55);}
.vt .pscreen{position:relative;height:100%;border-radius:26px;overflow:hidden;background:radial-gradient(circle at 70% 25%,#7DD3FC,transparent 45%),radial-gradient(circle at 25% 75%,var(--pink),transparent 50%),linear-gradient(160deg,#7C3AED,#2E1065);}
.vt .island{position:absolute;left:50%;top:9px;transform:translateX(-50%);width:34%;height:14px;border-radius:999px;background:#08030f;}
.vt .pscreen i{position:absolute;left:12%;right:12%;display:block;border-radius:10px;background:rgba(255,255,255,.22);}
.vt .pscreen .p1{top:20%;height:20%;}
.vt .pscreen .p2{bottom:16%;height:11%;border-radius:999px;}
.vt .spec{position:absolute;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.22);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);color:#fff;border-radius:999px;padding:.5rem 1rem;font-size:.85rem;font-weight:700;}
.vt .spec::before{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:#4ADE80;margin-right:.55rem;}
.vt .spec.s1{right:2%;bottom:48px;}
.vt .spec.s2{left:30%;top:0;}

/* ---- Entrée de page (une seule fois) ---- */
@keyframes lc-rise{from{opacity:0;transform:translateY(26px);}to{opacity:1;transform:none;}}
.vt .rise{animation:lc-rise .9s cubic-bezier(.2,.7,.2,1) both;}
.vt .d1{animation-delay:.05s;}.vt .d2{animation-delay:.18s;}.vt .d3{animation-delay:.32s;}.vt .d4{animation-delay:.46s;}.vt .d5{animation-delay:.3s;}
@media (prefers-reduced-motion:reduce){.vt .rise{animation:none;}html,body,[data-testid="stMain"],section.main{scroll-behavior:auto;}}

/* ---- Sections ---- */
.vt .anchor{scroll-margin-top:90px;}
.vt .sec{padding:4.5rem 0 .5rem;}
.vt .sec h2{font-size:clamp(1.8rem,3.8vw,2.8rem);line-height:1.08;letter-spacing:-.02em;font-weight:800;margin:0 0 .6rem;padding:0;color:var(--ink);}
.vt .sec .sub{color:var(--muted);font-size:1.05rem;max-width:40em;margin:0;line-height:1.55;}
.vt .count{color:var(--muted);font-weight:600;font-size:.95rem;margin:.4rem 0 0;}

/* ---- Pastilles de catégorie (st.pills) ---- */
.stApp [data-testid="stButtonGroup"] button{border-radius:999px !important;min-height:48px;padding:0 1.4rem;border:1.5px solid var(--lilac-2);background:#fff;color:var(--ink);font-weight:700;}
.stApp [data-testid="stButtonGroup"] button p{font-weight:700;}
.stApp [data-testid="stButtonGroup"] button:hover{border-color:var(--violet);}
.stApp [data-testid="stButtonGroup"] button[aria-checked="true"],.stApp [data-testid="stButtonGroup"] button[aria-pressed="true"],.stApp [data-testid="stButtonGroup"] button[kind*="Active"],.stApp [data-testid="stButtonGroup"] button[data-testid*="Active"]{background:var(--ink);border-color:var(--ink);color:#fff;}
.stApp [data-testid="stButtonGroup"] button[aria-checked="true"] p,.stApp [data-testid="stButtonGroup"] button[aria-pressed="true"] p,.stApp [data-testid="stButtonGroup"] button[kind*="Active"] p,.stApp [data-testid="stButtonGroup"] button[data-testid*="Active"] p{color:#fff;}

/* ---- Catalogue ---- */
.vt .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(285px,1fr));gap:1.3rem;align-items:start;margin:.5rem 0;}
.vt .dev{background:#fff;border:1px solid var(--lilac-2);border-radius:26px;padding:.6rem;}
.vt .dev-media{position:relative;aspect-ratio:1/1;border-radius:20px;overflow:hidden;background:var(--lilac-2);}
.vt .dev-media img{width:100%;height:100%;object-fit:cover;display:block;}
.vt .dev-media .tag{position:absolute;left:.7rem;top:.7rem;font-size:.78rem;font-weight:800;padding:.32rem .8rem;border-radius:999px;background:#fff;color:var(--ink);}
.vt .dev-media .tag-neuf{background:var(--violet);color:#fff;}
.vt .dev-media .tag-reco{background:#DDFBE9;color:#0B6B3A;}
.vt .dev.is-sold .dev-media img{filter:grayscale(1) brightness(.55);}
.vt .dev-media .sold{position:absolute;inset:0;display:grid;place-items:center;color:#fff;font-family:'Syne',sans-serif;font-weight:800;font-size:1.8rem;}
.vt .dev-body{padding:1rem .9rem .9rem;}
.vt .dev-body .cat{font-size:.78rem;font-weight:800;color:var(--violet);text-transform:uppercase;letter-spacing:.08em;}
.vt .dev-body h3{font-size:1.28rem;font-weight:800;letter-spacing:-.01em;margin:.2rem 0 0;padding:0;line-height:1.15;color:var(--ink);}
.vt .chips{display:flex;flex-wrap:wrap;gap:.4rem;margin:.75rem 0 0;}
.vt .chips span{display:inline-flex;align-items:center;gap:.4rem;background:var(--lilac);border-radius:999px;padding:.3rem .75rem;font-size:.85rem;font-weight:600;color:#3B2F57;}
.vt .chips span i{display:block;width:11px;height:11px;border-radius:50%;border:1px solid rgba(0,0,0,.18);}
.vt .price{margin:1rem 0 1rem;}
.vt .price strong{display:block;font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;letter-spacing:-.02em;line-height:1.1;}
.vt .price span{color:var(--muted);font-size:.9rem;font-weight:600;}
.vt .more{margin:0 0 1rem;border-top:1px solid var(--lilac-2);}
.vt .more summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:.92rem;padding:.75rem 0 .2rem;}
.vt .more summary::-webkit-details-marker{display:none;}
.vt .more summary::after{content:"+";display:grid;place-items:center;width:26px;height:26px;border-radius:50%;background:var(--lilac);font-size:1.15rem;font-weight:600;line-height:1;}
.vt .more[open] summary::after{content:"\2212";}
.vt .more-in p{margin:.5rem 0 .8rem;color:#3B2F57;font-size:.95rem;line-height:1.55;}
.vt .thumbs{display:grid;grid-template-columns:repeat(3,1fr);gap:.4rem;}
.vt .thumbs img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:12px;display:block;}
.vt .empty{background:#fff;border:1.5px dashed var(--violet-l);border-radius:24px;padding:2.2rem;text-align:center;color:var(--muted);}
.vt .empty strong{display:block;color:var(--ink);font-family:'Syne',sans-serif;font-size:1.25rem;margin-bottom:.3rem;}

/* ---- Bandeau échange ---- */
.vt .band{margin-top:4.5rem;border-radius:30px;padding:2.4rem 2.6rem;color:#fff;display:flex;flex-wrap:wrap;gap:1.5rem 2rem;align-items:center;justify-content:space-between;background:radial-gradient(60% 120% at 100% 0%,rgba(255,77,157,.55),transparent 60%),linear-gradient(120deg,var(--violet-d),var(--violet));}
.vt .band h2{font-size:clamp(1.5rem,3vw,2.2rem);font-weight:800;line-height:1.1;letter-spacing:-.02em;margin:0 0 .4rem;padding:0;color:#fff;}
.vt .band p{margin:0;color:#EDE6FF;max-width:34em;line-height:1.5;}

/* ---- Bento ---- */
.vt .bento{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-top:2rem;}
.vt .bento .big{grid-column:span 2;grid-row:span 2;border-radius:30px;padding:2rem;color:#fff;display:flex;flex-direction:column;justify-content:flex-end;min-height:300px;background:radial-gradient(70% 70% at 90% 0%,rgba(124,58,237,.8),transparent 65%),radial-gradient(50% 50% at 0% 100%,rgba(255,77,157,.35),transparent 65%),var(--ink);}
.vt .bento .big strong{font-family:'Syne',sans-serif;font-weight:800;font-size:clamp(3.4rem,8vw,6.2rem);line-height:.95;letter-spacing:-.04em;}
.vt .bento .big em{font-style:normal;font-family:'Syne',sans-serif;font-weight:700;font-size:1.5rem;margin:.2rem 0 .8rem;color:var(--violet-l);}
.vt .bento .big p{margin:0;color:#CFC6E6;max-width:22em;line-height:1.5;}
.vt .cell{background:#fff;border:1px solid var(--lilac-2);border-radius:24px;padding:1.3rem 1.3rem 1.4rem;}
.vt .cell svg{width:44px;height:44px;padding:10px;border-radius:14px;background:var(--lilac);stroke:var(--violet);fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;}
.vt .cell h3{font-size:1.05rem;font-weight:800;margin:.9rem 0 .25rem;padding:0;color:var(--ink);}
.vt .cell p{margin:0;color:var(--muted);font-size:.93rem;line-height:1.5;}

/* ---- Étapes ---- */
.vt .steps{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;margin-top:2rem;}
.vt .steps div.st{border-top:2px solid var(--ink);padding-top:1rem;}
.vt .steps .n{font-family:'Syne',sans-serif;font-weight:800;color:var(--violet);font-size:.95rem;letter-spacing:.08em;}
.vt .steps h3{font-size:1.3rem;font-weight:800;margin:.35rem 0 .3rem;padding:0;}
.vt .steps p{margin:0;color:var(--muted);line-height:1.5;}

/* ---- Contact ---- */
.vt .contact-side p{color:var(--muted);line-height:1.55;margin:0 0 1.2rem;}
.vt .contact-side .btn{margin:0 .5rem .6rem 0;}

/* ---- Pied de page ---- */
.vt .foot{position:relative;overflow:hidden;background:var(--ink);color:#CFC6E6;margin-top:5rem;padding:3.2rem 0 0;}
.vt .foot-in{max-width:1180px;margin:0 auto;padding:0 1.25rem;display:flex;flex-wrap:wrap;gap:2rem 4rem;justify-content:space-between;}
.vt .foot p{margin:.35rem 0 0;font-size:.95rem;}
.vt .foot a{color:#CFC6E6 !important;text-decoration:none !important;}
.vt .foot a:hover{color:#fff !important;}
.vt .foot .brand{color:#fff !important;}
.vt .foot .big-word{font-family:'Syne',sans-serif;font-weight:800;letter-spacing:-.04em;line-height:.8;font-size:clamp(3rem,13vw,10.5rem);white-space:nowrap;color:rgba(255,255,255,.07);margin:2.5rem 0 -.1em;text-align:center;user-select:none;}
.vt .foot .copy{max-width:1180px;margin:0 auto;padding:1rem 1.25rem 1.6rem;font-size:.85rem;position:relative;}

/* ---- Mobile ---- */
@media (max-width:860px){
.vt .nav-links{display:none;}
.vt .nav-in{gap:1rem;padding-left:1.1rem;}
.vt .hero{padding:7rem 0 2.5rem;}
.vt .hero-in{grid-template-columns:1fr;gap:1rem;}
.vt .stage{height:340px;margin-top:.5rem;}
.vt .laptop{width:min(92%,340px);top:20px;}
.vt .phone{width:112px;}
.vt .brands{margin-top:2rem;}
.vt .bento{grid-template-columns:repeat(2,1fr);}
.vt .bento .big{grid-column:span 2;grid-row:auto;min-height:240px;}
.vt .steps{grid-template-columns:1fr;gap:1.2rem;}
.vt .band{padding:1.8rem 1.5rem;}
.vt .sec{padding-top:3.2rem;}
}
"""

ADMIN_EXTRA = ".block-container{padding-top:2rem !important;padding-bottom:3rem !important;}"


def build_css(admin: bool = False) -> str:
    css = CSS.replace(".vt ", ".stApp .vt ")
    if admin:
        css += ADMIN_EXTRA
    return css
