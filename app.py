import re

import streamlit as st

# ------------------------------------------------------------------
# AMIGO DE LA CORTE
# No text inputs, no databases, no analytics, no accounts.
# The only state is which language/mode/button/checkbox is selected,
# held in memory for the current browser session and never stored.
# ------------------------------------------------------------------

# The selected mode from the previous run (widget state is kept in memory only).
mode = st.session_state.get("mode", "kid")
lang = st.session_state.get("lang", "es")

st.set_page_config(
    page_title="Amigo de la Corte",
    page_icon=None if mode == "adult" else "🏛️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 20-underscore blank for writing a name by hand
BLANK = "_" * 20

# Matches emoji, pictographs, dingbats, variation selectors and joiners (plus one trailing space)
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\u2300-\u23FF\u2600-\u27BF\u2B00-\u2BFF\uFE00-\uFE0F\u200D]+ ?"
)


def clean(text: str) -> str:
    """Adults mode: strip every emoji. Kids mode: leave text untouched."""
    if mode == "adult":
        return EMOJI_RE.sub("", text)
    return text


def X(es, en):
    """Pick text by language (emoji-filtered by mode)."""
    return clean(es if lang == "es" else en)


def S(es_kid, es_adult, en_kid, en_adult):
    """Pick text by language AND reading level (emoji-filtered by mode)."""
    if lang == "es":
        return clean(es_kid if mode == "kid" else es_adult)
    return clean(en_kid if mode == "kid" else en_adult)


def html(block: str):
    """Render HTML safely: strip leading spaces so Markdown never treats it as a code block."""
    cleaned = "\n".join(line.strip() for line in block.strip().splitlines())
    st.markdown(clean(cleaned), unsafe_allow_html=True)


def md(text: str):
    """Markdown with emoji filtering."""
    st.markdown(clean(text))


# ------------------------------------------------------------------
# STYLES
# ------------------------------------------------------------------
html("""
<style>
#MainMenu, footer, header {visibility: hidden;}
.stApp {background: linear-gradient(180deg, #eef2ff 0%, #f8fafc 40%);}
.stApp, .stApp p, .stApp li, .stApp label, .stApp span {color: #0f172a;}

/* ================================================================
   RESPONSIVE DEVICE FRAMING
   ================================================================ */
.block-container, [data-testid="stMainBlockContainer"] {
    width: 100% !important;
    box-sizing: border-box !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-top: 1.2rem !important;
    padding-bottom: 3rem !important;
}

/* ---- Phones: fill 100% of the viewport with fluid padding ---- */
@media (max-width: 600px) {
    .block-container, [data-testid="stMainBlockContainer"] {
        max-width: 100% !important;
        padding-left: clamp(0.75rem, 4vw, 1.1rem) !important;
        padding-right: clamp(0.75rem, 4vw, 1.1rem) !important;
    }
    [data-testid="stHorizontalBlock"] {flex-wrap: nowrap !important; gap: 0.45rem !important;}
    [data-testid="stColumn"], [data-testid="column"] {min-width: 0 !important; flex: 1 1 0 !important; width: auto !important;}
    .stButton > button {font-size: 12.5px; padding: 12px 2px;}
}

/* ---- iPads / tablets: compact, readable, no awkward stretching ---- */
@media (min-width: 601px) and (max-width: 1024px) {
    .block-container, [data-testid="stMainBlockContainer"] {
        max-width: 540px !important;
        padding-left: 1.1rem !important;
        padding-right: 1.1rem !important;
    }
    .app-title {font-size: 26px;}
    .app-sub {font-size: 14px;}
    .info-card {padding: 15px 16px;}
    .info-card h4 {font-size: 18px;}
    .info-card p {font-size: 15.5px; line-height: 1.5;}
    .rights-card {padding: 20px 16px;}
    .rights-card .big {font-size: 25px;}
    .rights-card .icon {font-size: 38px;}
    .stTabs [data-baseweb="tab"] {padding: 8px 12px;}
    .stTabs [data-baseweb="tab"] p {font-size: 13px;}
    .warn-box, .tip-box, .call-guide {font-size: 15px;}
}

/* ---- Desktop / laptop: 480px phone-preview frame on a neutral page ---- */
@media (min-width: 1025px) {
    .stApp {background: #e5e7eb !important;}
    .block-container, [data-testid="stMainBlockContainer"] {
        max-width: 480px !important;
        margin-top: 20px !important;
        margin-bottom: 20px !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
        background: linear-gradient(180deg, #eef2ff 0%, #f8fafc 40%);
        border: 8px solid #27272a;
        border-radius: 36px;
        box-shadow: 0 24px 60px rgba(15,23,42,0.28), 0 4px 12px rgba(15,23,42,0.12);
    }
}

/* ---------- Header ---------- */
.app-title {font-size: 30px; font-weight: 800; color: #1e3a8a; margin: 0; letter-spacing: -0.5px;}
.app-sub {font-size: 15px; color: #475569; margin: 2px 0 14px 0;}

/* ---------- Pill tabs ---------- */
.stTabs [data-baseweb="tab-list"] {gap: 8px; flex-wrap: wrap; border-bottom: none; padding-bottom: 6px;}
.stTabs [data-baseweb="tab"] {
    background: #ffffff; border-radius: 999px; padding: 10px 16px; height: auto;
    font-weight: 700; color: #1e293b; border: 1px solid #e2e8f0;
    box-shadow: 0 2px 6px rgba(15,23,42,0.06);
}
.stTabs [data-baseweb="tab"] p {color: inherit; font-size: 14px; margin: 0;}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1e3a8a, #3b82f6) !important;
    color: #ffffff !important; border: none;
}
.stTabs [aria-selected="true"] p {color: #ffffff !important;}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {display: none;}

/* ---------- Switches (radio as pills) ---------- */
div[role="radiogroup"] {gap: 8px; flex-wrap: wrap;}
div[role="radiogroup"] > label {
    background: #ffffff; border: 2px solid #cbd5e1; border-radius: 999px;
    padding: 8px 18px; box-shadow: 0 2px 6px rgba(15,23,42,0.06); cursor: pointer;
}
div[role="radiogroup"] > label > div:first-child {display: none;}
div[role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(135deg, #f59e0b, #f97316); border-color: #f97316;
}
div[role="radiogroup"] > label:has(input:checked) p {color: #ffffff !important;}
div[role="radiogroup"] p {font-weight: 800; font-size: 15px; margin: 0;}

/* ---------- Tap buttons ---------- */
.stButton > button {
    width: 100%; border-radius: 16px; padding: 14px 6px; font-weight: 800;
    font-size: 15px; border: 2px solid #1e3a8a; background: #ffffff; color: #1e3a8a;
    box-shadow: 0 4px 0 #1e3a8a, 0 8px 14px rgba(30,58,138,0.18);
    transition: all .1s ease;
}
.stButton > button:hover {border-color: #3b82f6; color: #1d4ed8;}
.stButton > button:active {transform: translateY(3px); box-shadow: 0 1px 0 #1e3a8a;}

/* ---------- 3D courtroom map ---------- */
.court-wrap {perspective: 900px; padding: 8px 0 22px 0;}
.court-floor {
    background: linear-gradient(160deg, #1e293b, #0f172a);
    border-radius: 22px; padding: 26px 16px 30px 16px; text-align: center;
    transform: rotateX(14deg); transform-origin: center bottom;
    box-shadow: 0 24px 40px rgba(15,23,42,0.35), inset 0 0 0 2px rgba(255,255,255,0.05);
}
.block {
    color: #ffffff !important; font-weight: 800; border-radius: 12px;
    transition: all .25s ease; opacity: 0.78; letter-spacing: .2px;
}
.block * {color: #ffffff !important;}
.block.active {opacity: 1; transform: translateY(-6px) scale(1.04); outline: 3px solid #fde047; filter: brightness(1.12);}
.judge {
    background: linear-gradient(135deg, #a16207, #78350f); width: 74%; margin: 0 auto 22px auto;
    padding: 16px 10px; font-size: 17px; box-shadow: 0 10px 0 #451a03, 0 18px 22px rgba(0,0,0,0.45);
}
.court-row {display: flex; gap: 14px; justify-content: center; margin-bottom: 22px;}
.fiscal {
    background: linear-gradient(135deg, #ef4444, #991b1b); flex: 1; padding: 14px 6px; font-size: 14px;
    box-shadow: 0 8px 0 #450a0a, 0 14px 18px rgba(0,0,0,0.4);
}
.interp {
    background: linear-gradient(135deg, #3b82f6, #1e3a8a); flex: 1; padding: 14px 6px; font-size: 14px;
    box-shadow: 0 8px 0 #172554, 0 14px 18px rgba(0,0,0,0.4);
}
.you {
    background: linear-gradient(135deg, #0ea5e9, #0369a1); width: 46%; margin: 0 auto; padding: 12px 6px;
    font-size: 14px; border: 2px dashed #bae6fd;
    box-shadow: 0 8px 0 #082f49, 0 14px 18px rgba(0,0,0,0.4); opacity: 1;
}

/* ================================================================
   3D ISOMETRIC CHARACTER AVATARS (pure CSS)
   ================================================================ */
@keyframes popin {from {opacity: 0; transform: translateY(8px) scale(.97);} to {opacity: 1; transform: none;}}
.avatar-stage {
    position: relative; height: 290px; margin: 14px 0 6px 0; border-radius: 22px; overflow: hidden;
    background: radial-gradient(ellipse at 50% 28%, #ffffff 0%, #e2e8f0 60%, #cbd5e1 100%);
    box-shadow: 0 10px 24px rgba(15,23,42,0.14), inset 0 0 0 2px rgba(255,255,255,0.7);
    animation: popin .35s ease;
}
.avatar-tag {
    position: absolute; left: 50%; bottom: 10px; transform: translateX(-50%); z-index: 5;
    background: rgba(15,23,42,0.88); color: #ffffff !important; padding: 5px 16px;
    border-radius: 999px; font-weight: 800; font-size: 14px; white-space: nowrap;
}
.stage-judge {--cy: 175px;}
.stage-fiscal {--cy: 170px;}

/* isometric floor tile */
.iso-floor {
    position: absolute; z-index: 1; left: 50%; top: var(--fy);
    width: var(--s); height: var(--s);
    margin-left: calc(var(--s) / -2); margin-top: calc(var(--s) / -2);
    background: linear-gradient(135deg, #f8fafc, #cbd5e1);
    border: 3px solid rgba(255,255,255,0.85); border-radius: 12px;
    box-shadow: 0 0 0 2px #94a3b8, 10px 14px 22px rgba(15,23,42,0.25);
    transform: rotateX(54.7356deg) rotateZ(45deg);
}
.floor-judge {--s: 190px; --fy: 204px;}
.floor-fiscal {--s: 150px; --fy: 207px;}

/* generic isometric cuboid (orthographic: no perspective) */
.cube {
    position: absolute; z-index: 2;
    width: var(--w); height: var(--h);
    left: calc(50% - var(--w) / 2); top: calc(var(--cy) - var(--h) / 2);
    transform-style: preserve-3d;
    transform: rotateX(-35.264deg) rotateY(-45deg);
}
.cube .face {position: absolute; backface-visibility: hidden; box-sizing: border-box;}
.cube .f-front  {width: var(--w); height: var(--h); left: 0; top: 0; background: var(--c-front); transform: translateZ(calc(var(--d) / 2));}
.cube .f-back   {width: var(--w); height: var(--h); left: 0; top: 0; background: var(--c-left); transform: rotateY(180deg) translateZ(calc(var(--d) / 2));}
.cube .f-right  {width: var(--d); height: var(--h); left: calc((var(--w) - var(--d)) / 2); top: 0; background: var(--c-right); transform: rotateY(90deg) translateZ(calc(var(--w) / 2));}
.cube .f-left   {width: var(--d); height: var(--h); left: calc((var(--w) - var(--d)) / 2); top: 0; background: var(--c-left); transform: rotateY(-90deg) translateZ(calc(var(--w) / 2));}
.cube .f-top    {width: var(--w); height: var(--d); left: 0; top: calc((var(--h) - var(--d)) / 2); background: var(--c-top); transform: rotateX(90deg) translateZ(calc(var(--h) / 2));}
.cube .f-bottom {width: var(--w); height: var(--d); left: 0; top: calc((var(--h) - var(--d)) / 2); background: var(--c-bottom); transform: rotateX(-90deg) translateZ(calc(var(--h) / 2));}

/* Judge: dark charcoal bench */
.cube.judge-bench {
    --w: 170px; --h: 70px; --d: 70px;
    --c-front: linear-gradient(180deg, #273449, #1e293b);
    --c-right: linear-gradient(180deg, #172033, #0f172a);
    --c-left: #0f172a; --c-back: #0f172a;
    --c-top: linear-gradient(135deg, #475569, #334155);
    --c-bottom: #020617;
}
.judge-bench .f-front {border-top: 5px solid #a16207;}
.judge-bench .plate {
    position: absolute; left: 50%; top: 50%; width: 46px; height: 14px; margin: -4px 0 0 -23px;
    background: linear-gradient(#fde68a, #b45309); border-radius: 3px;
}

/* Fiscal: crimson block */
.cube.suit-block {
    --w: 110px; --h: 90px; --d: 70px;
    --c-front: linear-gradient(180deg, #c42222, #b91c1c);
    --c-right: linear-gradient(180deg, #8f1616, #7f1d1d);
    --c-left: #7f1d1d; --c-back: #7f1d1d;
    --c-top: linear-gradient(135deg, #ef4444, #dc2626);
    --c-bottom: #450a0a;
}
.suit-block .collar {
    position: absolute; left: 50%; top: 4px; width: 34px; height: 24px; margin-left: -17px;
    background: #ffffff; clip-path: polygon(0 0, 100% 0, 50% 100%);
}
.suit-block .tie {
    position: absolute; left: 50%; top: 10px; width: 9px; height: 22px; margin-left: -4.5px;
    background: #0f172a; clip-path: polygon(25% 0, 75% 0, 100% 80%, 50% 100%, 0 80%);
}
.suit-block .case {
    position: absolute; left: 50%; bottom: 8px; width: 56px; height: 34px; margin-left: -28px;
    background: linear-gradient(#92400e, #78350f); border: 2px solid #451a03; border-radius: 6px;
    box-sizing: border-box;
}
.suit-block .case-handle {
    position: absolute; left: 50%; top: -12px; width: 22px; height: 12px; margin-left: -11px;
    border: 3px solid #451a03; border-bottom: none; border-radius: 8px 8px 0 0; box-sizing: border-box;
}
.suit-block .case-clasp {
    position: absolute; left: 50%; top: 9px; width: 12px; height: 8px; margin-left: -6px;
    background: #fde68a; border-radius: 2px;
}

/* character sprites */
.fig {position: absolute; left: 50%; z-index: 3; filter: drop-shadow(0 5px 4px rgba(15,23,42,0.35));}
.head {
    position: absolute; width: 46px; height: 50px; border-radius: 50% 50% 46% 46%;
    background: linear-gradient(#fcd9b6, #f0b98d);
}
.head .hair {position: absolute; left: -2px; top: -4px; width: 50px; height: 24px; border-radius: 25px 25px 6px 6px; background: #1f2937;}
.head.wig .hair {background: #e5e7eb; height: 28px;}
.head .eye {position: absolute; top: 26px; width: 5px; height: 6px; border-radius: 50%; background: #1e293b;}
.head .eye.l {left: 13px;}
.head .eye.r {left: 28px;}
.head .smile {position: absolute; left: 15px; top: 36px; width: 16px; height: 7px; border-bottom: 3px solid #b45309; border-radius: 0 0 12px 12px;}

.fig-judge {width: 80px; height: 100px; margin-left: -40px; bottom: 144px;}
.fig-judge .robe {
    position: absolute; left: 0; top: 44px; width: 80px; height: 56px; border-radius: 40px 40px 6px 6px;
    background: linear-gradient(90deg, #020617, #1f2937 50%, #020617);
}
.fig-judge .jabot {position: absolute; left: 27px; top: 46px; width: 26px; height: 22px; background: #ffffff; clip-path: polygon(0 0, 100% 0, 50% 100%);}
.fig-judge .head {left: 17px; top: 0;}
.fig-judge .gavel {
    position: absolute; left: 66px; top: 72px; width: 34px; height: 7px; background: #92400e;
    border-radius: 3px; transform: rotate(-30deg); transform-origin: left center;
}
.fig-judge .gavel::after {content: ""; position: absolute; right: -4px; top: -5px; width: 10px; height: 17px; background: #78350f; border-radius: 3px;}

.fig-fiscal {width: 46px; height: 58px; margin-left: -23px; bottom: 157px;}
.fig-fiscal .neck {position: absolute; left: 15px; top: 44px; width: 16px; height: 14px; background: #e8b88d;}
.fig-fiscal .head {left: 0; top: 0;}

/* Interpreter: navy circle with neon-blue border and headset */
.iso-shadow {
    position: absolute; z-index: 1; left: 50%; top: 206px; width: 200px; height: 46px; margin-left: -100px;
    border-radius: 50%; background: radial-gradient(ellipse, rgba(15,23,42,0.45), transparent 70%);
}
.iv-circle {
    position: absolute; z-index: 2; left: 50%; top: 52px; width: 150px; height: 150px; margin-left: -75px;
    border-radius: 50%; overflow: hidden; box-sizing: border-box;
    background: radial-gradient(circle at 32% 26%, #3b82f6 0%, #1d4ed8 55%, #1e3a8a 100%);
    border: 2px solid #00d4ff;
    box-shadow: 0 0 18px 3px rgba(0,212,255,0.55), 0 10px 0 #172554, 0 16px 18px rgba(2,6,23,0.45);
}
.iv-circle .iv-body {position: absolute; left: 23px; top: 98px; width: 100px; height: 70px; border-radius: 50px 50px 0 0; background: linear-gradient(#0f172a, #1e293b);}
.iv-circle .iv-collar {position: absolute; left: 60px; top: 98px; width: 26px; height: 24px; background: #ffffff; clip-path: polygon(0 0, 100% 0, 50% 100%);}
.iv-circle .iv-neck {position: absolute; left: 64px; top: 82px; width: 18px; height: 20px; background: #e8b88d;}
.iv-circle .iv-head {left: 50px; top: 32px;}
.iv-circle .hs-band {
    position: absolute; left: 44px; top: 22px; width: 58px; height: 44px; box-sizing: border-box;
    border: 5px solid #0b1220; border-bottom: none; border-radius: 30px 30px 0 0;
}
.iv-circle .hs-cup {position: absolute; top: 46px; width: 12px; height: 24px; border-radius: 6px; background: #00d4ff; border: 2px solid #0b1220; box-sizing: border-box;}
.iv-circle .hs-cup.l {left: 38px;}
.iv-circle .hs-cup.r {left: 96px;}
.iv-circle .hs-boom {
    position: absolute; left: 42px; top: 68px; width: 26px; height: 16px; box-sizing: border-box;
    border-left: 3px solid #0b1220; border-bottom: 3px solid #0b1220; border-radius: 0 0 0 14px;
}
.iv-circle .hs-dot {position: absolute; left: 64px; top: 80px; width: 8px; height: 8px; border-radius: 50%; background: #00d4ff;}

/* ---------- Info cards ---------- */
.info-card {
    background: #ffffff; border-radius: 18px; padding: 20px; margin: 14px 0;
    box-shadow: 0 8px 20px rgba(15,23,42,0.10); border-left: 8px solid #3b82f6;
}
.info-card h4 {margin: 0 0 8px 0; font-size: 20px; color: #0f172a;}
.info-card p {margin: 0; font-size: 17px; line-height: 1.55; color: #1e293b;}
.info-judge {border-left-color: #a16207;}
.info-fiscal {border-left-color: #b91c1c;}
.info-interp {border-left-color: #1d4ed8;}
.hint {text-align: center; color: #64748b; font-size: 15px; margin: 10px 0;}

.emergency-box {
    background: linear-gradient(135deg, #fb923c, #ea580c); padding: 22px; border-radius: 18px;
    margin: 12px 0; box-shadow: 0 10px 22px rgba(234,88,12,0.35);
}
.emergency-box p {color: #ffffff !important;}
.emergency-box .emerg-sub {font-size: 15px; line-height: 1.5; margin: 14px 0 0 0; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.5);}

.tip-box {
    background: #eff6ff; border-left: 8px solid #3b82f6; border-radius: 14px;
    padding: 14px 16px; margin: 14px 0; font-size: 16px; line-height: 1.55; color: #1e3a8a;
}
.tip-box * {color: #1e3a8a !important;}

/* ---------- Flashcards ---------- */
.rights-card {padding: 26px 20px; border-radius: 16px; text-align: center; margin: 16px 0 6px 0; box-shadow: 0 10px 22px rgba(0,0,0,0.20);}
.rights-card .tag {font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 800; margin: 0; opacity: .92; color: #fff !important;}
.rights-card .icon {font-size: 44px; margin: 6px 0 0 0;}
.rights-card .icon:empty {display: none;}
.rights-card .big {font-size: 30px; font-weight: 900; line-height: 1.25; margin: 8px 0 0 0; color: #fff !important;}
.card-red {background: linear-gradient(135deg, #ef4444, #991b1b);}
.card-blue {background: linear-gradient(135deg, #3b82f6, #1e3a8a);}
.card-green {background: linear-gradient(135deg, #22c55e, #166534);}
.card-purple {background: linear-gradient(135deg, #8b5cf6, #5b21b6);}
.card-note {text-align: center; font-size: 15px; color: #334155; margin: 0 0 18px 0; padding: 0 6px;}

/* ---------- Checklist ---------- */
.check-head {
    background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: #ffffff !important; font-weight: 800;
    border-radius: 14px; padding: 10px 16px; margin: 20px 0 8px 0; font-size: 17px;
    box-shadow: 0 4px 10px rgba(30,58,138,0.25);
}
.warn-box {
    background: #fef3c7; border-left: 8px solid #f59e0b; border-radius: 14px;
    padding: 14px 16px; margin: 14px 0; font-size: 16px; line-height: 1.5; color: #78350f;
}
.warn-box * {color: #78350f !important;}

/* ---------- Wallet card: pure black & white, print-ready ---------- */
.wallet-card-border {border: 4px dashed #000000; padding: 20px; background: #ffffff; color: #000000; border-radius: 4px; margin-top: 10px;}
.wallet-card-border p, .wallet-card-border hr {color: #000000 !important;}
.wallet-card-border hr {border: none; border-top: 2px solid #000000; margin: 10px 0;}

/* ---------- "What to say when you call" guide ---------- */
.call-guide {
    background: #ffffff; border: 2px solid #1e3a8a; border-radius: 18px; padding: 18px 18px 14px 18px;
    margin: 18px 0; box-shadow: 0 8px 20px rgba(30,58,138,0.12);
}
.call-guide .cg-title {margin: 0 0 10px 0; font-size: 18px; font-weight: 800; color: #1e3a8a;}
.call-guide ul {margin: 0; padding-left: 20px;}
.call-guide li {font-size: 15.5px; line-height: 1.5; margin: 0 0 8px 0; color: #0f172a;}

/* ---------- Resource buttons ---------- */
.stLinkButton a {
    border-radius: 14px !important; font-weight: 800 !important; padding: 12px !important;
    border: 2px solid #1e3a8a !important; color: #1e3a8a !important; background: #fff !important;
}

@media print {
    .stTabs [data-baseweb="tab-list"], .stRadio, .app-title, .app-sub {display: none !important;}
}
</style>
""")

# ------------------------------------------------------------------
# SWITCHES: language + reading level
# ------------------------------------------------------------------
html("""
<p class="app-title">🏛️ Amigo de la Corte</p>
""")

st.markdown("**Idioma / Language:**")
lang = st.radio(
    "Idioma / Language",
    ["es", "en"],
    format_func=lambda x: "Español" if x == "es" else "English",
    horizontal=True,
    label_visibility="collapsed",
    key="lang",
)

st.markdown(X("**Ver versión para:**", "**View the version for:**"))
mode = st.radio(
    X("Ver versión para", "View the version for"),
    ["kid", "adult"],
    format_func=lambda m: clean(
        ("🧒 Niños" if m == "kid" else "🧑 Adultos") if lang == "es"
        else ("🧒 Kids" if m == "kid" else "🧑 Adults")
    ),
    horizontal=True,
    label_visibility="collapsed",
    key="mode",
)

html(f'<p class="app-sub">{X("Guía de preparación y derechos para niños, niñas, jóvenes y sus familias", "Preparation and rights guide for children, teens, and their families")}</p>')

if mode == "kid":
    st.success(X(
        "💙 Estás a salvo aquí. Esta guía es solo para ayudarte a sentirte más tranquilo o tranquila. No te pedimos tu nombre ni guardamos nada tuyo.",
        "💙 You are safe here. This guide is only here to help you feel calmer. We don't ask for your name and we don't save anything about you.",
    ))
else:
    st.info(X(
        "🔒 Esta herramienta no tiene formularios ni campos de texto, y no guarda información personal. Es una guía educativa, no asesoría legal.",
        "🔒 This tool has no forms or text fields and does not save personal information. It is an educational guide, not legal advice.",
    ))

if "role" not in st.session_state:
    st.session_state.role = None

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    X("🏛️ Mi Corte", "🏛️ My Court"),
    X("📣 Habla Por Mí", "📣 Speak For Me"),
    X("📋 Mi Audiencia", "📋 My Hearing"),
    X("🖨️ Tarjeta de Bolsillo", "🖨️ Pocket Card"),
    X("🤝 Recursos", "🤝 Resources"),
])

# ------------------------------------------------------------------
# CONTENT
# ------------------------------------------------------------------
ROLES = {
    "judge": {
        "css": "info-judge",
        "title": X("⚖️ El Juez", "⚖️ The Judge"),
        "text": S(
            "El juez es una persona que escucha con atención para decidir qué es lo mejor. "
            "No es tu enemigo y no está ahí para asustarte. Si no entiendes algo, "
            "puedes decir: «No entendí, ¿me lo puede explicar otra vez?». Es normal, y está bien pedirlo. "
            "Dile «Su Señoría» y cuéntale la verdad con calma. 💙",
            "El juez de inmigración decide si la persona puede permanecer legalmente en Estados Unidos. "
            "Trabaja para el Departamento de Justicia (EOIR), no para ICE. Diríjase a él como "
            "«Su Señoría» (Your Honor), responda con la verdad y pida aclaración si no entiende "
            "alguna pregunta. Los menores pueden pedir tiempo para conseguir abogado.",
            "The judge is a person who listens carefully to decide what is best. "
            "They are not your enemy and they are not there to scare you. If you don't understand something, "
            "you can say: “I didn't understand. Can you explain it again, please?” That is normal, and it is okay to ask. "
            "Say “Your Honor” and tell the truth calmly. 💙",
            "The immigration judge decides whether a person may legally remain in the United States. "
            "The judge works for the Department of Justice (EOIR), not for ICE. Address the judge as "
            "“Your Honor,” answer truthfully, and ask for clarification if you do not understand a question. "
            "Minors may ask for time to find a lawyer.",
        ),
    },
    "fiscal": {
        "css": "info-fiscal",
        "title": X("💼 El Fiscal", "💼 The Government Lawyer"),
        "text": S(
            "El fiscal es un abogado que trabaja para el gobierno. Su trabajo es hablar con el juez "
            "sobre las reglas de inmigración. No es tu abogado, solo hace su trabajo. "
            "No tienes que contestar sola o solo si te da miedo; puedes decir que quieres un abogado. 🌟",
            "El fiscal (abogado del gobierno, de la oficina legal de ICE) representa al gobierno "
            "en el caso. No es su abogado ni lo defiende. Puede hacer preguntas, y usted tiene derecho "
            "a consultar con un abogado antes de contestar preguntas importantes sobre el caso.",
            "The government lawyer (sometimes called the “prosecutor” or “trial attorney”) works for the government "
            "and talks to the judge about immigration rules. They are not your lawyer; they are just doing their job. "
            "You don't have to answer alone if you feel scared. You can say you want a lawyer. 🌟",
            "The government attorney (a trial attorney with ICE's legal office) represents the government "
            "in the case. They are not your lawyer and do not defend you. They may ask questions, and you have the right "
            "to talk to a lawyer before answering important questions about the case.",
        ),
    },
    "interprete": {
        "css": "info-interp",
        "title": X("🗣️ El Intérprete", "🗣️ The Interpreter"),
        "text": S(
            "El intérprete es un ayudante que cambia las palabras de inglés a español y de español a inglés, "
            "para que entiendas todo y el juez te entienda a ti. Si no entiendes una palabra, "
            "levanta la mano y dilo. Nadie se va a enojar. 🤗",
            "El intérprete traduce al español todo lo que se dice en la audiencia y al inglés lo que "
            "usted dice. Si no comprende la traducción o el dialecto, avise al juez de inmediato. "
            "Pida un intérprete antes de contestar cualquier pregunta si lo necesita.",
            "The interpreter is a helper who changes the words from English to Spanish and from Spanish to English, "
            "so you understand everything and the judge understands you. If you don't understand a word, "
            "raise your hand and say so. Nobody will be upset. 🤗",
            "The interpreter translates everything said in the hearing into Spanish and translates what you say "
            "into English. If you do not understand the interpretation or the dialect, tell the judge right away. "
            "Ask for an interpreter before answering any question if you need one.",
        ),
    },
}

# The big English phrases stay in English on purpose: they are meant to be shown to an official.
CARDS = [
    {
        "css": "card-red", "icon": "🤫",
        "tag": X("DERECHO A GUARDAR SILENCIO / RIGHT TO SILENCE", "RIGHT TO SILENCE / DERECHO A GUARDAR SILENCIO"),
        "big": "I am exercising my constitutional right to remain silent until I speak to a lawyer.",
        "note": S(
            "Esto significa: «Quiero quedarme callado o callada hasta hablar con un abogado». Respira hondo. No tienes que contestar preguntas tú solo o sola. 💙",
            "Puede negarse a contestar preguntas y pedir un abogado. No firme ningún documento sin antes hablar con un abogado. Nunca presente documentos falsos.",
            "This means: “I want to stay quiet until I talk to a lawyer.” Take a deep breath. You don't have to answer questions alone. 💙",
            "You may decline to answer questions and ask for a lawyer. Do not sign any document before speaking with a lawyer. Never present false documents.",
        ),
    },
    {
        "css": "card-blue", "icon": "🗣️",
        "tag": X("DERECHO A TRADUCCIÓN / INTERPRETER REQUEST", "INTERPRETER REQUEST / DERECHO A TRADUCCIÓN"),
        "big": "I require a Spanish interpreter. I do not understand English well enough.",
        "note": S(
            "Esto significa: «Necesito a alguien que hable español para entender». Está bien pedir ayuda para entender. 🌈",
            "Solicite un intérprete antes de responder preguntas o firmar algo. Si no entiende, es mejor decirlo que adivinar.",
            "This means: “I need someone who speaks Spanish so I can understand.” It is okay to ask for help understanding. 🌈",
            "Ask for an interpreter before answering questions or signing anything. If you don't understand, it is better to say so than to guess.",
        ),
    },
    {
        "css": "card-green", "icon": "📞",
        "tag": X("CONTACTAR A MI ADULTO DE CONFIANZA / ADULT SPONSOR", "CONTACT MY TRUSTED ADULT / ADULT SPONSOR"),
        "big": "Please allow me to call my adult sponsor immediately.",
        "note": S(
            "Esto significa: «Por favor, déjeme llamar a mi adulto de confianza». Tu familia o tu patrocinador quiere ayudarte. 🏡",
            "Pida comunicarse con el patrocinador o tutor. Memorice o lleve anotados los números importantes en papel, por si le quitan el celular.",
            "This means: “Please let me call my trusted adult.” Your family or sponsor wants to help you. 🏡",
            "Ask to contact the sponsor or guardian. Memorize important numbers or carry them written on paper in case the phone is taken.",
        ),
    },
    {
        "css": "card-purple", "icon": "🚪",
        "tag": X("PUERTA / AT THE DOOR", "AT THE DOOR / PUERTA"),
        "big": "I do not consent to entry unless you have a warrant signed by a judge.",
        "note": S(
            "Si tocan a la puerta y estás con un adulto, deja que el adulto hable. No tienes que abrir tú solo o sola. Quédate cerca de alguien que te cuide. 🧸",
            "Una orden administrativa de ICE (formularios I-200 o I-205) no autoriza a entrar a su casa. Solo una orden firmada por un juez lo permite. Puede pedir que se la pasen por debajo de la puerta o por la ventana, sin abrir.",
            "If someone knocks and you are with an adult, let the adult do the talking. You don't have to open the door alone. Stay close to someone who takes care of you. 🧸",
            "An ICE administrative warrant (forms I-200 or I-205) does not authorize entry into your home. Only a warrant signed by a judge does. You may ask them to slide it under the door or hold it to a window, without opening.",
        ),
    },
]

# Checklist: list of (section title, [items]) per language and level
CHECKLIST = {
    "es": {
        "kid": [
            ("🌙 Antes de tu cita en la corte", [
                "Pregunta a tu adulto de confianza: ¿cuándo y dónde es mi cita?",
                "Pídele que te ayude a buscar un abogado gratis (mira la pestaña Recursos). 💛",
                "Escribe en un papel el número de tu adulto de confianza.",
                "Pregúntale lo que te da miedo. Es normal tener preguntas.",
            ]),
            ("🎒 La noche anterior", [
                "Alista tu ropa limpia y cómoda.",
                "Guarda tu tarjeta de bolsillo y los papeles que te dieron en tu mochila.",
                "Come algo rico y descansa. Puedes abrazar tu peluche. 🧸",
            ]),
            ("🏛️ El día de la cita", [
                "Llega temprano con tu adulto. Hay una revisión de seguridad al entrar.",
                "Pon tu celular en silencio.",
                "Si no entiendes algo, di: «No entendí, por favor». Nadie se enoja.",
                "Pide un intérprete si lo necesitas.",
                "Cuenta la verdad con calma y respira hondo.",
                "Antes de irte, pregunta: ¿cuándo es mi próxima cita?",
            ]),
        ],
        "adult": [
            ("📄 Antes de la audiencia", [
                "Revise su aviso de audiencia: fecha, hora y dirección de la corte.",
                "Confirme la información de su caso en acis.eoir.justice.gov o al 1-800-898-7180.",
                "Contacte hoy a una organización gratuita para buscar abogado (pestaña Recursos).",
                "Si cambió de domicilio, notifique la nueva dirección a la corte de inmigración (formulario EOIR-33) dentro de 5 días.",
                "Reúna documentos: aviso de audiencia, identificaciones, actas de nacimiento, papeles del caso y datos del abogado.",
                "Anote en papel los teléfonos del patrocinador y del abogado.",
            ]),
            ("🎒 El día anterior", [
                "Planifique el transporte y pida permiso en el trabajo o la escuela.",
                "Prepare ropa limpia y cómoda para el menor.",
                "Imprima o guarde la tarjeta de bolsillo.",
            ]),
            ("🏛️ El día de la audiencia", [
                "Llegue al menos 45 minutos antes: hay revisión de seguridad.",
                "Apague o silencie los celulares. Algunas cortes limitan su uso.",
                "Pida un intérprete si lo necesita.",
                "Responda con la verdad. Si no entiende una pregunta, dígalo.",
                "Si el menor no tiene abogado, use el texto de la pestaña Mi Corte para pedir más tiempo.",
                "Antes de salir, anote la fecha de la próxima audiencia y pregunte lo que no entendió.",
            ]),
        ],
    },
    "en": {
        "kid": [
            ("🌙 Before your court date", [
                "Ask your trusted adult: when and where is my court date?",
                "Ask them to help you find a free lawyer (see the Resources tab). 💛",
                "Write your trusted adult's phone number on a piece of paper.",
                "Tell them what scares you. It is normal to have questions.",
            ]),
            ("🎒 The night before", [
                "Pick out clean, comfortable clothes.",
                "Put your pocket card and the papers you were given in your backpack.",
                "Eat something yummy and rest. You can hug your stuffed animal. 🧸",
            ]),
            ("🏛️ On the day", [
                "Arrive early with your adult. There is a security check at the door.",
                "Put your phone on silent.",
                "If you don't understand something, say: “I didn't understand, please.” Nobody gets mad.",
                "Ask for an interpreter if you need one.",
                "Tell the truth calmly and take deep breaths.",
                "Before you leave, ask: when is my next court date?",
            ]),
        ],
        "adult": [
            ("📄 Before the hearing", [
                "Review the hearing notice: court date, time, and address.",
                "Confirm case information at acis.eoir.justice.gov or by calling 1-800-898-7180.",
                "Contact a free legal organization today to look for a lawyer (Resources tab).",
                "If you moved, notify the immigration court of your new address (Form EOIR-33) within 5 days.",
                "Gather documents: hearing notice, IDs, birth certificates, case papers, and the lawyer's information.",
                "Write down the sponsor's and the lawyer's phone numbers on paper.",
            ]),
            ("🎒 The day before", [
                "Plan transportation and request time off from work or school.",
                "Prepare clean, comfortable clothes for the minor.",
                "Print or save the pocket card.",
            ]),
            ("🏛️ On the day of the hearing", [
                "Arrive at least 45 minutes early: there is a security screening.",
                "Turn phones off or to silent. Some courts restrict their use.",
                "Ask for an interpreter if you need one.",
                "Answer truthfully. If you don't understand a question, say so.",
                "If the minor has no lawyer, use the script on the My Court tab to ask for more time.",
                "Before leaving, write down the next hearing date and ask about anything you did not understand.",
            ]),
        ],
    },
}


# ------------------------------------------------------------------
# 3D ISOMETRIC AVATARS (pure HTML/CSS, one per role)
# ------------------------------------------------------------------
CUBE_FACES = (
    '<div class="face f-right"></div><div class="face f-left"></div>'
    '<div class="face f-back"></div><div class="face f-top"></div><div class="face f-bottom"></div>'
)
FACE_FEATURES = (
    '<div class="hair"></div><div class="eye l"></div><div class="eye r"></div><div class="smile"></div>'
)


def avatar_html(role: str) -> str:
    title = ROLES[role]["title"]
    if role == "judge":
        stage = "stage-judge"
        scene = (
            '<div class="iso-floor floor-judge"></div>'
            '<div class="cube judge-bench"><div class="face f-front"><div class="plate"></div></div>'
            + CUBE_FACES +
            '</div>'
            '<div class="fig fig-judge"><div class="robe"></div><div class="jabot"></div>'
            '<div class="head wig">' + FACE_FEATURES + '</div><div class="gavel"></div></div>'
        )
    elif role == "fiscal":
        stage = "stage-fiscal"
        scene = (
            '<div class="iso-floor floor-fiscal"></div>'
            '<div class="cube suit-block"><div class="face f-front">'
            '<div class="collar"></div><div class="tie"></div>'
            '<div class="case"><div class="case-handle"></div><div class="case-clasp"></div></div>'
            '</div>'
            + CUBE_FACES +
            '</div>'
            '<div class="fig fig-fiscal"><div class="neck"></div>'
            '<div class="head">' + FACE_FEATURES + '</div></div>'
        )
    else:
        stage = "stage-interp"
        scene = (
            '<div class="iso-shadow"></div>'
            '<div class="iv-circle"><div class="iv-body"></div><div class="iv-collar"></div><div class="iv-neck"></div>'
            '<div class="head iv-head">' + FACE_FEATURES + '</div>'
            '<div class="hs-band"></div><div class="hs-cup l"></div><div class="hs-cup r"></div>'
            '<div class="hs-boom"></div><div class="hs-dot"></div></div>'
        )
    return f'<div class="avatar-stage {stage}">{scene}<div class="avatar-tag">{title}</div></div>'


# ==================================================================
# TAB 1: MI CORTE
# ==================================================================
with tab1:
    md(X("### 🗺️ El mapa de la sala", "### 🗺️ The courtroom map"))
    st.write(S(
        "Así se ve un salón de la corte. Toca a una persona para saber quién es. ¡Nada de esto muerde! 😊",
        "Distribución típica de una sala de inmigración. Toque cada rol para ver su función.",
        "This is what a courtroom looks like. Tap a person to find out who they are. Nobody here bites! 😊",
        "Typical layout of an immigration courtroom. Tap each role to see what they do.",
    ))

    sel = st.session_state.role

    def cls(name):
        return "active" if sel == name else ""

    html(f"""
    <div class="court-wrap">
    <div class="court-floor">
    <div class="block judge {cls('judge')}">{ROLES['judge']['title']}</div>
    <div class="court-row">
    <div class="block fiscal {cls('fiscal')}">{ROLES['fiscal']['title'].replace('The Government Lawyer', 'Gov. Lawyer')}</div>
    <div class="block interp {cls('interprete')}">{ROLES['interprete']['title']}</div>
    </div>
    <div class="block you">{X("👤 Tu lugar", "👤 Your spot")}</div>
    </div>
    </div>
    """)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(X("⚖️ El Juez", "⚖️ Judge"), key="b_judge"):
            st.session_state.role = "judge"
            st.rerun()
    with c2:
        if st.button(X("💼 El Fiscal", "💼 Gov. Lawyer"), key="b_fiscal"):
            st.session_state.role = "fiscal"
            st.rerun()
    with c3:
        if st.button(X("🗣️ El Intérprete", "🗣️ Interpreter"), key="b_interp"):
            st.session_state.role = "interprete"
            st.rerun()

    if sel:
        r = ROLES[sel]
        html(avatar_html(sel))
        html(f"""
        <div class="info-card {r['css']}">
        <h4>{r['title']}</h4>
        <p>{r['text']}</p>
        </div>
        """)
    else:
        html(f'<p class="hint">{X("👆 Toca un botón para ver quién es cada persona.", "👆 Tap a button to see who each person is.")}</p>')

    md(X("### 🚨 Qué decir si estás solo", "### 🚨 What to say if you're alone"))
    st.write(S(
        "Si el juez te llama y no tienes abogado, no te preocupes. Puedes leer estas palabras en voz alta, o mostrarle tu pantalla. Ya están escritas para ti. 💛",
        "Si el menor comparece sin abogado, puede leer este texto al juez o mostrarlo en pantalla. Pedir tiempo para conseguir representación es una petición común y legítima.",
        "If the judge calls you and you don't have a lawyer, don't worry. You can read these words out loud, or show your screen. They are already written for you. 💛",
        "If the minor appears without a lawyer, they can read this text to the judge or show it on screen. Asking for time to find representation is a common and legitimate request.",
    ))

    if lang == "es":
        emerg_sub = (
            f"<b>En español:</b> <em>«Hola, Su Señoría. Mi nombre es {BLANK}. Soy menor de edad. "
            "Hoy no tengo abogado. Solicito respetuosamente un aplazamiento para poder conseguir "
            "representación legal gratuita.»</em>"
        )
    else:
        emerg_sub = (
            "<b>Tip:</b> say it in English. If you need an interpreter, ask for one first: "
            "<em>“I need a Spanish interpreter, please.”</em>"
        )

    html(f"""
    <div class="emergency-box">
    <p style="font-size:14px; margin:0; text-transform:uppercase; font-weight:800; opacity:.95;">🇺🇸 READ THIS ALOUD TO THE JUDGE / LEE ESTO AL JUEZ</p>
    <p style="font-size:21px; font-weight:800; line-height:1.4; margin:8px 0 0 0;">"Hello, Your Honor. My name is {BLANK}. I am a minor. I do not have a lawyer today. I respectfully request a continuance so I can secure free legal representation."</p>
    <p class="emerg-sub">{emerg_sub}</p>
    </div>
    """)

    # How a continuance works
    html(f"""
    <div class="tip-box">
    {X(
        "💡 <b>¿Cómo funciona esto?</b> Al decir esta frase, le estás pidiendo formalmente al juez un 'aplazamiento' (continuación) para posponer tu cita. "
        "El juez es quien decide, pero cuando una persona no tiene abogado, normalmente pausa el caso y le da tiempo adicional, con frecuencia entre 30 y 90 días, "
        "para que pueda buscar un abogado gratuito. No es automático ni está garantizado: nunca faltes a tu cita.",
        "💡 <b>How does this work?</b> By saying this phrase, you are formally asking the judge for a 'continuance' to extend your court date. "
        "The judge decides, but when someone has no lawyer, the judge will typically pause the case and grant extra time, often 30 to 90 days, "
        "to secure a free lawyer. It is not automatic or guaranteed: never skip a hearing.",
    )}
    </div>
    """)

    st.info(S(
        "💡 Recuerda: ir a la corte no significa que hiciste algo malo. No tienes que pasar por esto sin apoyo.",
        "💡 El gobierno no proporciona abogado pagado en los casos de inmigración, pero sí se puede pedir tiempo para conseguir uno. Contacte organizaciones gratuitas lo antes posible (pestaña Recursos) y no falte a ninguna audiencia.",
        "💡 Remember: going to court does not mean you did something wrong. You don't have to go through this without support.",
        "💡 The government does not provide a paid lawyer in immigration cases, but you can ask for time to find one. Contact free organizations as soon as possible (Resources tab) and do not miss any hearing.",
    ))

# ==================================================================
# TAB 2: HABLA POR MÍ
# ==================================================================
with tab2:
    md(X("### 📣 Tarjetas de emergencia", "### 📣 Emergency cards"))
    st.write(S(
        "Si un oficial te hace preguntas y sientes miedo, respira despacio. Puedes mostrar estas tarjetas sin decir nada más. 💙",
        "Si un agente le detiene, mantenga la calma y muestre estas tarjetas. Hable lo mínimo. No mienta ni muestre documentos falsos.",
        "If an officer asks you questions and you feel scared, breathe slowly. You can show these cards without saying anything else. 💙",
        "If an agent stops you, stay calm and show these cards. Say as little as possible. Do not lie or show false documents.",
    ))

    for c in CARDS:
        html(f"""
        <div class="rights-card {c['css']}">
        <p class="icon">{c['icon']}</p>
        <p class="tag">{c['tag']}</p>
        <p class="big">"{c['big']}"</p>
        </div>
        """)
        html(f'<p class="card-note">{c["note"]}</p>')

# ==================================================================
# TAB 3: MI AUDIENCIA (checklist)
# ==================================================================
with tab3:
    md(X("### 📋 Lista para el día de tu audiencia", "### 📋 Day-of-your-hearing checklist"))
    st.write(S(
        "Toca cada casilla cuando termines un paso. ¡Vas muy bien! 🌟",
        "Marque cada casilla al completar un paso. Las casillas solo se ven en su pantalla y no se guardan.",
        "Tap each box when you finish a step. You're doing great! 🌟",
        "Check each box as you complete a step. The boxes only appear on your screen and are not saved.",
    ))

    html(f"""
    <div class="warn-box">
    <b>{X("⚠️ Muy importante:", "⚠️ Very important:")}</b>
    {S(
        "Es muy importante ir a todas tus citas en la corte. Si no vas, el juez puede decidir sin escucharte. Si no puedes ir, díselo YA a tu adulto de confianza o a tu abogado.",
        "Es fundamental asistir a todas las audiencias. Si no se presenta, el juez puede ordenar la deportación sin escucharle (orden «en ausencia»). Si no puede asistir, contacte a su abogado de inmediato.",
        "It is very important to go to every court date. If you don't go, the judge can decide without hearing you. If you can't go, tell your trusted adult or your lawyer RIGHT AWAY.",
        "Attending every hearing is essential. If you do not appear, the judge can order removal without hearing you (an “in absentia” order). If you cannot attend, contact your lawyer immediately.",
    )}
    </div>
    """)

    for i, (section, items) in enumerate(CHECKLIST[lang][mode]):
        html(f'<div class="check-head">{section}</div>')
        for j, item in enumerate(items):
            st.checkbox(clean(item), key=f"chk_{lang}_{mode}_{i}_{j}")

    st.info(S(
        "💙 Sentir nervios es normal. Respira hondo: inhala contando hasta 4 y suelta el aire contando hasta 4.",
        "💡 Esta lista es una guía general. Cada tribunal puede tener reglas distintas: revise su aviso de audiencia y consulte con su abogado.",
        "💙 Feeling nervous is normal. Take a deep breath: breathe in counting to 4, then breathe out counting to 4.",
        "💡 This checklist is a general guide. Each court may have different rules: review your hearing notice and talk to your lawyer.",
    ))

# ==================================================================
# TAB 4: TARJETA DE BOLSILLO (strict black & white, print-ready, no emoji)
# ==================================================================
with tab4:
    md(X("### 🖨️ Respaldo físico imprimible", "### 🖨️ Printable backup"))
    st.write(X(
        "Toma una captura de pantalla (screenshot) de este cuadro o usa el menú de tu navegador para imprimir esta página. Guarda el papel doblado en tu bolsillo por si te confiscan el celular:",
        "Take a screenshot of this box or use your browser menu to print this page. Keep the folded paper in your pocket in case your phone is taken:",
    ))

    html(f"""
    <div class="wallet-card-border">
    <p style="text-align:center; font-weight:900; font-size:18px; margin:0;">AMIGO DE LA CORTE · TARJETA DE BOLSILLO</p>
    <hr>
    <p style="font-size:15px; font-weight:900; margin:0 0 4px 0;">COURT SCRIPT / SCRIPT PARA LA CORTE:</p>
    <p style="font-size:14px; font-style:italic; margin:0;">"Hello, Your Honor. My name is {BLANK}. I am a minor. I do not have a lawyer today. I respectfully request a continuance so I can secure free legal representation."</p>
    <hr>
    <p style="font-size:15px; font-weight:900; margin:0 0 4px 0;">FIELD ENCOUNTERS / PARA ENCUENTROS CON ICE:</p>
    <p style="font-size:14px; font-style:italic; margin:0 0 4px 0;">1. "I am exercising my right to remain silent until I speak to a lawyer."</p>
    <p style="font-size:14px; font-style:italic; margin:0 0 4px 0;">2. "I require a Spanish interpreter. I do not understand English well."</p>
    <p style="font-size:14px; font-style:italic; margin:0;">3. "Please allow me to call my adult sponsor immediately."</p>
    <hr>
    <p style="font-size:15px; font-weight:900; margin:0 0 4px 0;">MI CONTACTO / MY CONTACT:</p>
    <p style="font-size:14px; margin:0;">Nombre / Name: {BLANK}</p>
    <p style="font-size:14px; margin:6px 0 0 0;">Tel: {BLANK}</p>
    <p style="font-size:14px; margin:6px 0 0 0;">Abogado / Lawyer: {BLANK}</p>
    <p style="font-size:14px; margin:6px 0 0 0;">Próxima audiencia / Next hearing: {BLANK}</p>
    </div>
    """)
    st.caption(X(
        "Escribe tus datos a mano en la versión impresa. Esta app no te pide ni guarda ninguna información.",
        "Write your information by hand on the printed copy. This app does not ask for or save any information.",
    ))

# ==================================================================
# TAB 5: RECURSOS
# ==================================================================
with tab5:
    md(X("### 🤝 Directorio de ayuda gratuita en Houston, TX", "### 🤝 Free help directory in Houston, TX"))
    st.write(S(
        "Hay personas buenas cuyo trabajo es ayudar a niños y jóvenes como tú. Pídele a un adulto de confianza que te ayude a llamar. 💛",
        "Presione los botones para llamar directamente. Confirme disponibilidad y requisitos al llamar.",
        "There are good people whose job is to help kids and teens like you. Ask a trusted adult to help you call. 💛",
        "Press the buttons to call directly. Confirm availability and eligibility when you call.",
    ))

    md("#### ⚖️ KIND Houston")
    st.link_button(X("📞 Llamar a KIND (832-779-4340)", "📞 Call KIND (832-779-4340)"), "tel:8327794340", use_container_width=True)
    st.caption(X(
        "Especialistas en proveer abogados gratuitos para niños no acompañados frente a audiencias migratorias.",
        "Specialists in providing free lawyers for unaccompanied children facing immigration hearings.",
    ))

    md("#### ✊ FIEL Houston")
    st.link_button(X("📞 Llamar a FIEL (713-364-3435)", "📞 Call FIEL (713-364-3435)"), "tel:7133643435", use_container_width=True)
    st.caption(X(
        "Organización comunitaria liderada por inmigrantes dedicada a la orientación familiar y defensa de derechos.",
        "Immigrant-led community organization focused on family guidance and rights advocacy.",
    ))

    md("#### 🛡️ RAICES Texas")
    st.link_button(X("📞 Llamar a RAICES (210-222-0960)", "📞 Call RAICES (210-222-0960)"), "tel:2102220960", use_container_width=True)
    st.caption(X(
        "Servicios legales gratuitos y de representación migratoria en todo el territorio de Texas.",
        "Free legal services and immigration representation across Texas.",
    ))

    # What to say when you call
    html(f"""
    <div class="call-guide">
    <p class="cg-title">{X("📝 Qué decir cuando llames para pedir ayuda", "📝 What to say when you call")}</p>
    <ul>
    <li>{X("Diga su nombre completo y edad exacta.", "State your full legal name and exact age.")}</li>
    <li>{X(
        "Tenga listo su 'Número A' (Número de Registro de Extranjero). Es un número de 9 dígitos que empieza con la letra A y aparece en todos sus papeles de inmigración.",
        "Have your 9-digit 'A-Number' (Alien Registration Number) ready from your paperwork. It starts with the letter A and appears on your immigration papers.",
    )}</li>
    <li>{X(
        "Mencione la fecha, la hora y la ciudad donde está programada su próxima audiencia de corte.",
        "State the date, time, and city of your next scheduled court hearing.",
    )}</li>
    <li>{X(
        "Diga claramente: 'Soy un menor de edad y no tengo dinero para pagar un abogado privado, necesito defensa gratuita'.",
        "Clearly state: 'I am a minor without a lawyer, and I need free legal representation.'",
    )}</li>
    </ul>
    </div>
    """)

    md(X("#### 🔎 Más ayuda", "#### 🔎 More help"))
    st.link_button(X("Directorio nacional de servicios legales (busca por Houston)", "National legal services directory (search for Houston)"),
                   "https://www.immigrationadvocates.org/legaldirectory/", use_container_width=True)
    st.link_button(X("Lista oficial de abogados pro bono (EOIR)", "Official pro bono attorney list (EOIR)"),
                   "https://www.justice.gov/eoir/list-pro-bono-legal-service-providers", use_container_width=True)
    st.link_button(X("Info de tu caso de inmigración · 1-800-898-7180", "Immigration case information · 1-800-898-7180"),
                   "tel:18008987180", use_container_width=True)
    st.link_button(X("Línea contra la trata de personas · 1-888-373-7888", "Human trafficking hotline · 1-888-373-7888"),
                   "tel:18883737888", use_container_width=True)
    st.link_button(X("Emergencia · 911", "Emergency · 911"), "tel:911", use_container_width=True)

    if mode == "kid":
        st.info(X(
            "💡 Siempre es buena idea guardar estos números en un papel. ¡No estás solo ni sola! 🌟",
            "💡 It's always a good idea to keep these numbers on paper. You are not alone! 🌟",
        ))

# ==================================================================
# FOOTER: PRIVACY PROFILE
# ==================================================================
st.markdown("---")
st.caption(clean("""
🔒 Perfil de Privacidad / Data Privacy:
Esta plataforma es estrictamente informativa. No tiene formularios ni campos de texto, no usa cuentas, no tiene análisis (analytics) ni publicidad, y no guarda tu nombre ni ninguna información personal.
Como cualquier sitio web, el servicio que lo hospeda (Streamlit Community Cloud) puede registrar datos técnicos básicos de conexión; esta app no los ve ni los usa.

This app is educational and does not constitute legal advice or create an attorney-client relationship. It has no forms, accounts, or analytics, and it does not collect or store any personal information.
Cada caso es diferente: habla con un abogado o una organización de ayuda legal lo antes posible. / Every case is different: talk to a lawyer or legal aid organization as soon as possible.
"""))
