import json
import re

import streamlit as st
import streamlit.components.v1 as components

# ------------------------------------------------------------------
# AMIGO DE LA CORTE  (Soft 3D clay edition)
# Zero-PII design: no text inputs, no databases, no analytics, no accounts,
# no cookies set by this app. The only state is which language / mode / page /
# card / checkbox is selected, kept in memory for the current browser session.
# Requires Streamlit >= 1.39 (uses st.container(key=...)).
# ------------------------------------------------------------------
APP_NAME = "Amigo de la Corte"  # change to "Amiga de la Corte" here if you prefer

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🏛️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.session_state.setdefault("lang", "es")
st.session_state.setdefault("mode", "kid")
st.session_state.setdefault("page", "home")
st.session_state.setdefault("role", None)
st.session_state.setdefault("htype", "inperson")

lang = st.session_state["lang"]
mode = st.session_state["mode"]

BLANK = "_" * 20


def X(es, en):
    """Pick text by language."""
    return es if lang == "es" else en


def S(es_kid, es_adult, en_kid, en_adult):
    """Pick text by language AND reading level."""
    if lang == "es":
        return es_kid if mode == "kid" else es_adult
    return en_kid if mode == "kid" else en_adult


def html(block: str):
    """Render HTML safely: strip indentation and blank lines so Markdown never makes a code block."""
    cleaned = "\n".join(l.strip() for l in block.strip().splitlines() if l.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


def go(page: str):
    st.session_state.page = page


def set_role(r: str):
    st.session_state.role = r


# ------------------------------------------------------------------
# STYLES  (soft 3D claymorphism)
# ------------------------------------------------------------------
html("""
<style>
:root {
  --bg:#F5F6FF; --ink:#1E2038; --muted:#5B5F7E;
  --ind1:#7B61FF; --ind2:#9B8AFB; --mint1:#5CE1E6; --mint2:#38B2AC; --coral:#FF9F68;
  --clay: 0 18px 34px rgba(123,97,255,0.16), 0 6px 12px rgba(30,32,56,0.07), inset 0 2px 4px rgba(255,255,255,0.6), inset 0 -4px 8px rgba(123,97,255,0.06);
}
#MainMenu, footer, header {visibility: hidden;}
.stApp {background: var(--bg); font-family: ui-rounded, "SF Pro Rounded", "Segoe UI", system-ui, -apple-system, sans-serif;}
.stApp, .stApp p, .stApp li, .stApp label, .stApp span, .stApp div {color: var(--ink);}

.block-container, [data-testid="stMainBlockContainer"] {
  width: 100% !important; max-width: 480px !important; margin: 0 auto !important;
  padding: 1rem 1rem 9.5rem 1rem !important; box-sizing: border-box !important;
}
@media (max-width: 600px) {
  .block-container, [data-testid="stMainBlockContainer"] {padding-left: 0.85rem !important; padding-right: 0.85rem !important;}
}
h1, h2, h3, h4 {color: var(--ink) !important;}

/* ---------- native boxes ---------- */
[data-testid="stAlert"], div[role="alert"] {
  background:#ffffff !important; border:none !important; border-radius:24px !important; box-shadow: var(--clay) !important;
}
[data-testid="stAlert"] *, div[role="alert"] * {color: var(--ink) !important;}
[data-testid="stExpander"] details {
  background:#ffffff; border:none !important; border-radius:24px !important; box-shadow: var(--clay); margin: 10px 0; overflow: hidden;
}
[data-testid="stExpander"] summary {padding: 14px 16px !important;}
[data-testid="stExpander"] summary p {font-weight: 800; font-size: 16px; margin: 0;}
[data-testid="stCheckbox"] label p {font-size: 15px; line-height: 1.4;}
.stCaption, [data-testid="stCaptionContainer"] {color: var(--muted) !important;}

/* ---------- header ---------- */
.app-top {display:flex; align-items:center; justify-content:space-between; gap:8px; margin: 2px 0 10px 0;}
.app-title {font-size: 24px; font-weight: 900; color: var(--ink); margin: 0; letter-spacing: -0.4px;}
.badge {
  background:#ffffff; border-radius: 999px; padding: 5px 11px; font-size: 11px; font-weight: 800; color: var(--ind1);
  box-shadow: 0 6px 12px rgba(123,97,255,0.16), inset 0 2px 3px rgba(255,255,255,0.8); white-space: nowrap;
}

/* ---------- pill toggles (radio) ---------- */
div[role="radiogroup"] {gap: 8px; flex-wrap: wrap;}
div[role="radiogroup"] > label {
  background:#ffffff; border:none; border-radius:999px; padding: 7px 16px; cursor:pointer;
  box-shadow: 0 6px 12px rgba(123,97,255,0.14), inset 0 2px 3px rgba(255,255,255,0.9), inset 0 -3px 5px rgba(123,97,255,0.08);
}
div[role="radiogroup"] > label > div:first-child {display:none;}
div[role="radiogroup"] > label:has(input:checked) {
  background: linear-gradient(135deg, var(--ind1), var(--ind2));
  box-shadow: 0 8px 16px rgba(123,97,255,0.38), inset 0 2px 4px rgba(255,255,255,0.45);
}
div[role="radiogroup"] > label:has(input:checked) p {color:#ffffff !important;}
div[role="radiogroup"] p {font-weight: 800; font-size: 13.5px; margin: 0; white-space: nowrap;}

/* ---------- clay buttons ---------- */
.stButton > button {
  width:100%; border-radius: 20px; padding: 12px 6px; font-weight: 800; font-size: 14px; border: none;
  background: #ffffff; color: var(--ind1); box-shadow: var(--clay); transition: all .12s ease;
}
.stButton > button:hover {color: #5b43e6; transform: translateY(-1px);}
.stButton > button:active {transform: translateY(2px);}
.stLinkButton a {
  border-radius: 20px !important; font-weight: 800 !important; padding: 12px !important; border: none !important;
  color: var(--ind1) !important; background:#ffffff !important; box-shadow: var(--clay) !important;
}
.stLinkButton a p {color: var(--ind1) !important;}

/* ---------- cards ---------- */
.hero {
  background: linear-gradient(135deg, var(--ind1), var(--ind2)); border-radius: 28px; padding: 24px 20px; margin: 8px 0 14px 0;
  box-shadow: 0 22px 40px rgba(123,97,255,0.38), inset 0 3px 6px rgba(255,255,255,0.45), inset 0 -6px 12px rgba(60,40,180,0.25);
}
.hero * {color:#ffffff !important;}
.hero .h1 {font-size: 25px; font-weight: 900; line-height: 1.2; margin: 0 0 6px 0;}
.hero .h2 {font-size: 15.5px; line-height: 1.5; margin: 0; opacity: .95;}
.clay {background:#ffffff; border-radius: 24px; padding: 18px; margin: 12px 0; box-shadow: var(--clay);}
.clay h4 {margin: 0 0 6px 0; font-size: 18px; color: var(--ink);}
.clay p {margin: 0; font-size: 15.5px; line-height: 1.55; color: var(--ink);}
.clay.ind {border-top: 6px solid var(--ind1);}
.clay.mint {border-top: 6px solid var(--mint2);}
.clay.coral {border-top: 6px solid var(--coral);}
.banner {
  background: linear-gradient(135deg, #FFF3E8, #FFE4D1); border-radius: 24px; padding: 14px 16px; margin: 12px 0;
  box-shadow: 0 12px 24px rgba(255,159,104,0.28), inset 0 2px 4px rgba(255,255,255,0.8);
  font-size: 14.5px; line-height: 1.5; color: var(--ink);
}
.banner * {color: var(--ink) !important;}
.banner.teal {background: linear-gradient(135deg, #E3FBFB, #C8F4F4); box-shadow: 0 12px 24px rgba(56,178,172,0.25), inset 0 2px 4px rgba(255,255,255,0.8);}
.hint {text-align:center; color: var(--muted); font-size: 14.5px; margin: 10px 0;}
.sec {font-size: 19px; font-weight: 900; margin: 22px 0 6px 0; color: var(--ink);}

.steps {display:grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 12px 0;}
.tile {
  background:#ffffff; border-radius: 24px; padding: 16px 12px; text-align: center; box-shadow: var(--clay);
}
.tile .ic {font-size: 34px; margin: 0 0 4px 0;}
.tile .tt {font-size: 14.5px; font-weight: 800; margin: 0 0 4px 0;}
.tile .tx {font-size: 13px; line-height: 1.4; margin: 0; color: var(--muted);}

/* gradient phrase cards */
.phrase {border-radius: 26px; padding: 22px 18px; margin: 14px 0 6px 0; text-align:center;
  box-shadow: 0 20px 36px rgba(60,40,180,0.25), inset 0 3px 6px rgba(255,255,255,0.4), inset 0 -6px 10px rgba(0,0,0,0.12);}
.phrase * {color:#ffffff !important;}
.phrase .tag {font-size: 12px; text-transform: uppercase; letter-spacing: 1px; font-weight: 800; margin: 0; opacity: .95;}
.phrase .icon {font-size: 38px; margin: 4px 0 0 0;}
.phrase .big {font-size: 21px; font-weight: 800; line-height: 1.35; margin: 8px 0 0 0;}
.g-ind {background: linear-gradient(135deg, #7B61FF, #9B8AFB);}
.g-mint {background: linear-gradient(135deg, #38B2AC, #5CE1E6);}
.g-coral {background: linear-gradient(135deg, #FF8A50, #FFB78A);}
.g-plum {background: linear-gradient(135deg, #6A4DE0, #B07CF5);}
.phon {background:#ffffff; border-radius: 18px; padding: 10px 14px; margin: 8px 0 4px 0; font-size: 14px; line-height: 1.45;
  box-shadow: inset 0 2px 5px rgba(123,97,255,0.15), 0 4px 10px rgba(123,97,255,0.08);}
.phon b {color: var(--ind1);}
.note {text-align:center; font-size: 14px; color: var(--muted); margin: 4px 4px 16px 4px;}

.qa-ok {display:inline-block; background: #D9F7F5; color:#12706b !important; font-weight:800; font-size:12px; border-radius:999px; padding:3px 10px; margin-bottom:8px;}

/* ---------- pocket card (print, black & white) ---------- */
.wallet {border: 4px dashed #000000; padding: 18px; background:#ffffff; color:#000000; border-radius: 6px; margin-top: 10px;}
.wallet p, .wallet hr {color:#000000 !important;}
.wallet hr {border:none; border-top: 2px solid #000000; margin: 10px 0;}

/* ---------- courtroom map + 3D clay characters ---------- */
.court-wrap {perspective: 900px; padding: 8px 0 18px 0;}
.court-floor {
  background: linear-gradient(160deg, #E4E1FF, #CFCBFF); border-radius: 28px; padding: 24px 14px 28px 14px; text-align:center;
  transform: rotateX(12deg); transform-origin: center bottom; box-shadow: 0 24px 40px rgba(123,97,255,0.25), inset 0 3px 6px rgba(255,255,255,0.7);
}
.block {color:#ffffff !important; font-weight: 800; border-radius: 18px; transition: all .25s ease; opacity: .85;}
.block * {color:#ffffff !important;}
.block.active {opacity: 1; transform: translateY(-6px) scale(1.04); outline: 3px solid #ffffff; filter: brightness(1.08);}
.judge {background: linear-gradient(135deg, #7B61FF, #5B43E6); width: 74%; margin: 0 auto 20px auto; padding: 15px 10px; font-size: 16px;
  box-shadow: 0 9px 0 #3E2BB0, 0 16px 20px rgba(60,40,180,0.35);}
.court-row {display:flex; gap: 12px; justify-content:center; margin-bottom: 20px;}
.fiscal {background: linear-gradient(135deg, #FF9F68, #F2733A); flex:1; padding: 13px 6px; font-size: 13.5px; box-shadow: 0 8px 0 #B24E1C, 0 14px 18px rgba(200,90,30,0.3);}
.interp {background: linear-gradient(135deg, #5CE1E6, #38B2AC); flex:1; padding: 13px 6px; font-size: 13.5px; box-shadow: 0 8px 0 #1F7C77, 0 14px 18px rgba(30,120,115,0.3);}
.you {background: linear-gradient(135deg, #B9AEFF, #9B8AFB); width: 46%; margin: 0 auto; padding: 11px 6px; font-size: 13.5px; border: 2px dashed #ffffff; box-shadow: 0 8px 0 #6E58D8; opacity:1;}

@keyframes popin {from {opacity:0; transform: translateY(8px) scale(.97);} to {opacity:1; transform:none;}}
.avatar-stage {
  position: relative; height: 290px; margin: 14px 0 6px 0; border-radius: 28px; overflow: hidden;
  background: radial-gradient(ellipse at 50% 28%, #ffffff 0%, #E9E6FF 60%, #D6D1FF 100%);
  box-shadow: var(--clay); animation: popin .35s ease;
}
.avatar-tag {position:absolute; left:50%; bottom:10px; transform: translateX(-50%); z-index:5;
  background: rgba(30,32,56,0.88); color:#ffffff !important; padding: 5px 16px; border-radius: 999px; font-weight: 800; font-size: 14px; white-space: nowrap;}
.stage-judge {--cy: 175px;}
.stage-fiscal {--cy: 170px;}
.iso-floor {
  position:absolute; z-index:1; left:50%; top: var(--fy); width: var(--s); height: var(--s);
  margin-left: calc(var(--s) / -2); margin-top: calc(var(--s) / -2);
  background: linear-gradient(135deg, #ffffff, #D9D4FF); border: 3px solid rgba(255,255,255,0.9); border-radius: 22px;
  box-shadow: 0 0 0 2px #B9B1F5, 10px 14px 22px rgba(123,97,255,0.25); transform: rotateX(54.7356deg) rotateZ(45deg);
}
.floor-judge {--s: 190px; --fy: 204px;}
.floor-fiscal {--s: 150px; --fy: 207px;}
.cube {position:absolute; z-index:2; width: var(--w); height: var(--h); left: calc(50% - var(--w) / 2); top: calc(var(--cy) - var(--h) / 2);
  transform-style: preserve-3d; transform: rotateX(-35.264deg) rotateY(-45deg);}
.cube .face {position:absolute; backface-visibility: hidden; box-sizing: border-box; border-radius: 14px;}
.cube .f-front  {width: var(--w); height: var(--h); left:0; top:0; background: var(--c-front); transform: translateZ(calc(var(--d) / 2));}
.cube .f-back   {width: var(--w); height: var(--h); left:0; top:0; background: var(--c-left); transform: rotateY(180deg) translateZ(calc(var(--d) / 2));}
.cube .f-right  {width: var(--d); height: var(--h); left: calc((var(--w) - var(--d)) / 2); top:0; background: var(--c-right); transform: rotateY(90deg) translateZ(calc(var(--w) / 2));}
.cube .f-left   {width: var(--d); height: var(--h); left: calc((var(--w) - var(--d)) / 2); top:0; background: var(--c-left); transform: rotateY(-90deg) translateZ(calc(var(--w) / 2));}
.cube .f-top    {width: var(--w); height: var(--d); left:0; top: calc((var(--h) - var(--d)) / 2); background: var(--c-top); transform: rotateX(90deg) translateZ(calc(var(--h) / 2));}
.cube .f-bottom {width: var(--w); height: var(--d); left:0; top: calc((var(--h) - var(--d)) / 2); background: var(--c-bottom); transform: rotateX(-90deg) translateZ(calc(var(--h) / 2));}

.cube.judge-bench {--w:170px; --h:70px; --d:70px;
  --c-front: linear-gradient(180deg, #8A72FF, #6A4DE0); --c-right: linear-gradient(180deg, #5B43E6, #4A33C8);
  --c-left: #4A33C8; --c-top: linear-gradient(135deg, #B9AEFF, #9B8AFB); --c-bottom: #3A28A8;}
.judge-bench .f-front {border-top: 5px solid #FFD27A;}
.judge-bench .plate {position:absolute; left:50%; top:50%; width:46px; height:14px; margin:-4px 0 0 -23px; background: linear-gradient(#FFE9A8, #F2B544); border-radius: 7px;}
.cube.suit-block {--w:110px; --h:90px; --d:70px;
  --c-front: linear-gradient(180deg, #FFAE7C, #FF8A50); --c-right: linear-gradient(180deg, #F2733A, #D95F28);
  --c-left: #D95F28; --c-top: linear-gradient(135deg, #FFD0B0, #FFB78A); --c-bottom: #A8481A;}
.suit-block .collar {position:absolute; left:50%; top:4px; width:34px; height:24px; margin-left:-17px; background:#ffffff; clip-path: polygon(0 0, 100% 0, 50% 100%);}
.suit-block .tie {position:absolute; left:50%; top:10px; width:9px; height:22px; margin-left:-4.5px; background: #3E2BB0; clip-path: polygon(25% 0, 75% 0, 100% 80%, 50% 100%, 0 80%);}
.suit-block .case {position:absolute; left:50%; bottom:8px; width:56px; height:34px; margin-left:-28px; background: linear-gradient(#FFE0C8, #FFC9A3); border: 2px solid #D95F28; border-radius: 10px; box-sizing: border-box;}
.suit-block .case-handle {position:absolute; left:50%; top:-12px; width:22px; height:12px; margin-left:-11px; border:3px solid #D95F28; border-bottom:none; border-radius: 8px 8px 0 0; box-sizing: border-box;}
.suit-block .case-clasp {position:absolute; left:50%; top:9px; width:12px; height:8px; margin-left:-6px; background:#ffffff; border-radius: 4px;}

.fig {position:absolute; left:50%; z-index:3; filter: drop-shadow(0 6px 5px rgba(60,40,180,0.3));}
.head {position:absolute; width:48px; height:52px; border-radius: 50%; background: linear-gradient(#FFE3C8, #F7C39B); box-shadow: inset 0 3px 5px rgba(255,255,255,0.7), inset 0 -4px 6px rgba(200,120,70,0.25);}
.head .hair {position:absolute; left:-2px; top:-5px; width:52px; height:26px; border-radius: 26px 26px 8px 8px; background:#4A3A8C;}
.head.wig .hair {background:#F1EFFF; height: 30px; box-shadow: inset 0 -3px 5px rgba(123,97,255,0.2);}
.head .eye {position:absolute; top:27px; width:6px; height:7px; border-radius:50%; background:#1E2038;}
.head .eye.l {left:14px;} .head .eye.r {left:29px;}
.head .smile {position:absolute; left:16px; top:38px; width:16px; height:7px; border-bottom: 3px solid #D9703A; border-radius: 0 0 12px 12px;}
.fig-judge {width:80px; height:100px; margin-left:-40px; bottom:144px;}
.fig-judge .robe {position:absolute; left:0; top:44px; width:80px; height:56px; border-radius: 40px 40px 10px 10px; background: linear-gradient(90deg, #3E2BB0, #5B43E6 50%, #3E2BB0);}
.fig-judge .jabot {position:absolute; left:27px; top:46px; width:26px; height:22px; background:#ffffff; clip-path: polygon(0 0, 100% 0, 50% 100%);}
.fig-judge .head {left:16px; top:0;}
.fig-judge .gavel {position:absolute; left:66px; top:72px; width:34px; height:8px; background:#F2B544; border-radius:4px; transform: rotate(-30deg); transform-origin:left center;}
.fig-judge .gavel::after {content:""; position:absolute; right:-4px; top:-5px; width:10px; height:18px; background:#E09A2A; border-radius:5px;}
.fig-fiscal {width:48px; height:60px; margin-left:-24px; bottom:157px;}
.fig-fiscal .neck {position:absolute; left:16px; top:46px; width:16px; height:14px; background:#F2BC92;}
.fig-fiscal .head {left:0; top:0;}
.iso-shadow {position:absolute; z-index:1; left:50%; top:206px; width:200px; height:46px; margin-left:-100px; border-radius:50%; background: radial-gradient(ellipse, rgba(123,97,255,0.35), transparent 70%);}
.iv-circle {position:absolute; z-index:2; left:50%; top:52px; width:150px; height:150px; margin-left:-75px; border-radius:50%; overflow:hidden; box-sizing:border-box;
  background: radial-gradient(circle at 32% 26%, #9BF1F4 0%, #5CE1E6 45%, #38B2AC 100%); border: 3px solid #ffffff;
  box-shadow: 0 0 20px 4px rgba(92,225,230,0.55), 0 10px 0 #1F7C77, 0 16px 18px rgba(30,120,115,0.35), inset 0 4px 8px rgba(255,255,255,0.6);}
.iv-circle .iv-body {position:absolute; left:23px; top:98px; width:100px; height:70px; border-radius: 50px 50px 0 0; background: linear-gradient(#6A4DE0, #5B43E6);}
.iv-circle .iv-collar {position:absolute; left:60px; top:98px; width:26px; height:24px; background:#ffffff; clip-path: polygon(0 0, 100% 0, 50% 100%);}
.iv-circle .iv-neck {position:absolute; left:64px; top:82px; width:18px; height:20px; background:#F2BC92;}
.iv-circle .iv-head {left:49px; top:32px;}
.iv-circle .hs-band {position:absolute; left:44px; top:22px; width:58px; height:44px; box-sizing:border-box; border:5px solid #3E2BB0; border-bottom:none; border-radius: 30px 30px 0 0;}
.iv-circle .hs-cup {position:absolute; top:46px; width:12px; height:24px; border-radius:6px; background:#FF9F68; border:2px solid #3E2BB0; box-sizing:border-box;}
.iv-circle .hs-cup.l {left:38px;} .iv-circle .hs-cup.r {left:96px;}
.iv-circle .hs-boom {position:absolute; left:42px; top:68px; width:26px; height:16px; box-sizing:border-box; border-left:3px solid #3E2BB0; border-bottom:3px solid #3E2BB0; border-radius: 0 0 0 14px;}
.iv-circle .hs-dot {position:absolute; left:64px; top:80px; width:8px; height:8px; border-radius:50%; background:#FF9F68;}

/* ---------- floating bottom dock ---------- */
.st-key-dock {
  position: fixed; bottom: 10px; left: 50%; transform: translateX(-50%); z-index: 9999;
  width: min(480px, calc(100% - 16px)); box-sizing: border-box; padding: 8px 6px 8px 6px;
  background: linear-gradient(135deg, #9B8AFB, #6A4DE0 70%, #5B43E6); border-radius: 30px;
  box-shadow: 0 -4px 24px rgba(123,97,255,0.25), 0 18px 36px rgba(91,67,230,0.45), inset 0 3px 5px rgba(255,255,255,0.45), inset 0 -5px 8px rgba(40,20,140,0.35);
  backdrop-filter: blur(10px); overflow: visible !important;
}
@media (max-width: 600px) {
  .st-key-dock {bottom: 0; width: 100%; border-radius: 26px 26px 0 0; padding-bottom: calc(8px + env(safe-area-inset-bottom));}
}
.st-key-dock [data-testid="stHorizontalBlock"] {flex-wrap: nowrap !important; gap: 0.1rem !important; align-items: center !important; overflow: visible !important;}
.st-key-dock [data-testid="stColumn"], .st-key-dock [data-testid="column"] {min-width: 0 !important; flex: 1 1 0 !important; width: auto !important; overflow: visible !important;}
.st-key-dock .stButton {display:flex; justify-content:center;}
.st-key-dock .stButton > button {
  background: transparent !important; border: none !important; box-shadow: none !important; color:#ffffff !important;
  padding: 5px 2px !important; min-height: 0 !important; border-radius: 18px !important; font-size: 10.5px; line-height: 1.15; width: 100%;
}
.st-key-dock .stButton > button p {margin: 0 !important; color:#ffffff !important; font-weight: 800; white-space: nowrap;}
.st-key-dock .stButton > button p:first-child {font-size: 21px; line-height: 1.2;}
.st-key-dock .stButton > button:hover {transform:none; background: rgba(255,255,255,0.12) !important;}
.st-key-nav_center .stButton > button {
  width: 62px !important; height: 62px !important; border-radius: 50% !important; margin-top: -34px !important; padding: 0 !important;
  background: linear-gradient(135deg, #5CE1E6, #38B2AC) !important;
  box-shadow: 0 0 0 6px rgba(92,225,230,0.28), 0 12px 24px rgba(56,178,172,0.6), inset 0 3px 6px rgba(255,255,255,0.75), inset 0 -4px 8px rgba(0,0,0,0.14) !important;
}
.st-key-nav_center .stButton > button p:first-child {font-size: 28px;}

@media print {
  .st-key-dock, [data-testid="stRadio"], .app-top {display:none !important;}
}
</style>
""")

# highlight the active dock tab
_active = st.session_state.page
if _active == "script":
    html("<style>.st-key-nav_center .stButton > button {box-shadow: 0 0 0 7px rgba(255,255,255,0.55), 0 12px 24px rgba(56,178,172,0.7), inset 0 3px 6px rgba(255,255,255,0.75) !important;}</style>")
else:
    html(f"<style>.st-key-nav_{_active} .stButton > button {{background: rgba(255,255,255,0.25) !important;}}</style>")

# ------------------------------------------------------------------
# HEADER + TOGGLES
# ------------------------------------------------------------------
html(f"""
<div class="app-top">
<p class="app-title">🏛️ {APP_NAME}</p>
<span class="badge">{X("📘 Solo educativo · No es asesoría legal", "📘 Educational only · Not legal advice")}</span>
</div>
""")

st.radio(
    "Idioma / Language",
    ["es", "en"],
    format_func=lambda v: "Español" if v == "es" else "English",
    horizontal=True, label_visibility="collapsed", key="lang",
)
lang = st.session_state["lang"]
st.radio(
    "Modo / Mode",
    ["kid", "adult"],
    format_func=lambda m: (
        ("🧒 Modo Niño" if m == "kid" else "🧑 Modo Adulto") if lang == "es"
        else ("🧒 Child Mode" if m == "kid" else "🧑 Parent Mode")
    ),
    horizontal=True, label_visibility="collapsed", key="mode",
)
mode = st.session_state["mode"]

# ------------------------------------------------------------------
# SHARED TEXT
# ------------------------------------------------------------------
DISCLAIMER_BANNER = X(
    f"<b>⚠️ Aviso importante:</b> {APP_NAME} ofrece <b>solo información educativa general</b>. "
    "<b>No es asesoría legal</b> y <b>no crea una relación abogado-cliente</b>. Cada caso es diferente: "
    "hable con un abogado o una organización de ayuda legal lo antes posible.",
    f"<b>⚠️ Important notice:</b> {APP_NAME} provides <b>general educational information only</b>. "
    "It is <b>not legal advice</b> and <b>does not create an attorney-client relationship</b>. Every case is different: "
    "talk to a lawyer or legal aid organization as soon as possible.",
)
DISC_SHORT = S(
    "Esto es solo para ayudarte a aprender. No es asesoría legal. Un abogado puede ayudarte con tu caso.",
    "Aviso educativo: información general solamente. No es asesoría legal ni crea una relación abogado-cliente. "
    "Solo un abogado puede decirle cómo aplica la ley a su caso. Hable con un abogado lo antes posible.",
    "This is only to help you learn. It is not legal advice. A lawyer can help you with your own case.",
    "Educational notice: general information only. Not legal advice and no attorney-client relationship. "
    "Only a lawyer can tell you how the law applies to your case. Talk to a lawyer as soon as you can.",
)


def banner():
    html(f'<div class="banner">{DISCLAIMER_BANNER}</div>')


# ------------------------------------------------------------------
# AUDIO COACH (browser SpeechSynthesis, 0.75x) + PHONETIC SPELLING
# ------------------------------------------------------------------
def audio_coach(text_en: str, phonetic_es: str):
    """Phonetic chip + 'Listen Slowly' / 'Normal' buttons. Runs fully in the browser; nothing is sent or stored."""
    html(f'<div class="phon"><b>{X("🗣️ Se pronuncia:", "🗣️ Say it like this (Spanish spelling):")}</b><br>{phonetic_es}</div>')
    msg_nospeech = "Tu navegador no tiene audio / Your browser has no speech audio"
    components.html(
        f"""
<style>
 body {{margin:0; font-family: ui-rounded, system-ui, sans-serif;}}
 .row {{display:flex; gap:10px;}}
 button {{flex:1; border:none; cursor:pointer; border-radius:20px; padding:12px 6px; font-weight:800; font-size:14px;
   box-shadow: 0 10px 18px rgba(123,97,255,0.18), inset 0 2px 4px rgba(255,255,255,0.7);}}
 #slow {{background: linear-gradient(135deg,#5CE1E6,#38B2AC); color:#fff; flex:1.6;}}
 #norm {{background:#fff; color:#7B61FF;}}
 button:active {{transform: translateY(2px);}}
 #m {{font-size:12px; color:#5B5F7E; margin:6px 2px 0 2px;}}
</style>
<div class="row">
 <button id="slow">🐢 Escuchar Despacio / Listen Slowly</button>
 <button id="norm">🔊 Normal</button>
</div>
<div id="m"></div>
<script>
 const T = {json.dumps(text_en)};
 function say(rate) {{
   if (!('speechSynthesis' in window)) {{ document.getElementById('m').textContent = {json.dumps(msg_nospeech)}; return; }}
   window.speechSynthesis.cancel();
   const u = new SpeechSynthesisUtterance(T);
   u.lang = 'en-US'; u.rate = rate;
   const v = window.speechSynthesis.getVoices().find(x => x.lang && x.lang.startsWith('en-US'));
   if (v) u.voice = v;
   window.speechSynthesis.speak(u);
 }}
 document.getElementById('slow').onclick = () => say(0.75);
 document.getElementById('norm').onclick = () => say(1.0);
</script>
""",
        height=78,
    )


# ------------------------------------------------------------------
# CONTENT: roles, phrases, checklist, relief, Q&A bank
# ------------------------------------------------------------------
ROLES = {
    "judge": {
        "css": "ind",
        "title": X("⚖️ El Juez", "⚖️ The Judge"),
        "text": S(
            "El juez es una persona que escucha con atención para decidir qué es lo mejor. No es tu enemigo y no está ahí para asustarte. "
            "Si no entiendes algo, puedes decir: «No entendí, ¿me lo puede explicar otra vez?». Dile «Su Señoría» y cuéntale la verdad con calma. 💙",
            "El juez de inmigración decide si la persona puede permanecer legalmente en Estados Unidos. Trabaja para el Departamento de Justicia (EOIR), no para ICE. "
            "Diríjase a él como «Su Señoría» (Your Honor), responda con la verdad y pida aclaración si no entiende una pregunta.",
            "The judge is a person who listens carefully to decide what is best. They are not your enemy and they are not there to scare you. "
            "If you don't understand something, you can say: “I didn't understand. Can you explain it again, please?” Say “Your Honor” and tell the truth calmly. 💙",
            "The immigration judge decides whether a person may legally remain in the United States. The judge works for the Department of Justice (EOIR), not for ICE. "
            "Address the judge as “Your Honor,” answer truthfully, and ask for clarification if you do not understand a question.",
        ),
    },
    "fiscal": {
        "css": "coral",
        "title": X("💼 El Fiscal", "💼 The Government Lawyer"),
        "text": S(
            "El fiscal es un abogado que trabaja para el gobierno. Habla con el juez sobre las reglas de inmigración. No es tu abogado, solo hace su trabajo. "
            "No tienes que contestar sola o solo si te da miedo; puedes decir que quieres un abogado. 🌟",
            "El fiscal (abogado del gobierno, de la oficina legal de ICE) representa al gobierno en el caso. No es su abogado ni lo defiende. "
            "Puede hacer preguntas, y usted puede pedir hablar con un abogado antes de contestar preguntas importantes.",
            "The government lawyer works for the government and talks to the judge about immigration rules. They are not your lawyer; they are just doing their job. "
            "You don't have to answer alone if you feel scared. You can say you want a lawyer. 🌟",
            "The government attorney (a trial attorney with ICE's legal office) represents the government in the case. They are not your lawyer and do not defend you. "
            "They may ask questions, and you may ask to talk to a lawyer before answering important questions.",
        ),
    },
    "interprete": {
        "css": "mint",
        "title": X("🗣️ El Intérprete", "🗣️ The Interpreter"),
        "text": S(
            "El intérprete es un ayudante que cambia las palabras de inglés a español y de español a inglés, para que entiendas todo y el juez te entienda a ti. "
            "Si no entiendes una palabra, levanta la mano y dilo. Nadie se va a enojar. 🤗",
            "El intérprete traduce al español todo lo que se dice en la audiencia y al inglés lo que usted dice. Si no comprende la traducción o el dialecto, "
            "avise al juez de inmediato.",
            "The interpreter is a helper who changes the words from English to Spanish and from Spanish to English, so you understand everything and the judge understands you. "
            "If you don't understand a word, raise your hand and say so. Nobody will be upset. 🤗",
            "The interpreter translates everything said in the hearing into Spanish and translates what you say into English. "
            "If you do not understand the interpretation or the dialect, tell the judge right away.",
        ),
    },
}

# Courtroom phrases. English is intentional: it is meant to be said to an official.
PHRASES = [
    {
        "g": "g-coral", "icon": "🤫",
        "tag": X("DERECHO A GUARDAR SILENCIO", "RIGHT TO SILENCE"),
        "en": "I am exercising my constitutional right to remain silent until I speak to a lawyer.",
        "phon": "Ai am ék-ser-sai-sing mai kons-ti-tú-shio-nal rait tu ri-méin sái-lent ón-til ai spik tu a ló-ier.",
        "note": S(
            "Significa: «Quiero quedarme callado o callada hasta hablar con un abogado». Respira hondo. 💙",
            "Puede negarse a contestar preguntas y pedir un abogado. No firme ningún documento sin antes hablar con un abogado. Nunca presente documentos falsos.",
            "This means: “I want to stay quiet until I talk to a lawyer.” Take a deep breath. 💙",
            "You may decline to answer questions and ask for a lawyer. Do not sign any document before speaking with a lawyer. Never present false documents.",
        ),
    },
    {
        "g": "g-mint", "icon": "🗣️",
        "tag": X("PEDIR INTÉRPRETE", "INTERPRETER REQUEST"),
        "en": "I require a Spanish interpreter. I do not understand English well enough.",
        "phon": "Ai ri-cuái-er a Spá-nish in-tér-pre-ter. Ai du not an-der-stánd Ín-glish uel i-nóf.",
        "note": S(
            "Significa: «Necesito a alguien que hable español para entender». Está bien pedir ayuda. 🌈",
            "Solicite un intérprete antes de responder preguntas o firmar algo. Si no entiende, es mejor decirlo que adivinar.",
            "This means: “I need someone who speaks Spanish so I can understand.” It is okay to ask for help. 🌈",
            "Ask for an interpreter before answering questions or signing anything. If you don't understand, it is better to say so than to guess.",
        ),
    },
    {
        "g": "g-ind", "icon": "🙋",
        "tag": X("SI NO ENTIENDES", "IF YOU DON'T UNDERSTAND"),
        "en": "I did not understand. Can you explain it again, please?",
        "phon": "Ai did not an-der-stánd. Kan yu ex-pléin it a-guén, plis?",
        "note": S(
            "Significa: «No entendí. ¿Me lo puede explicar otra vez, por favor?». Nadie se enoja. 🤗",
            "Pedir que se repita o se aclare una pregunta es siempre apropiado en una audiencia.",
            "This means: “I didn't understand. Can you say it again, please?” Nobody gets mad. 🤗",
            "Asking for a question to be repeated or clarified is always appropriate in a hearing.",
        ),
    },
    {
        "g": "g-plum", "icon": "📞",
        "tag": X("LLAMAR A MI ADULTO DE CONFIANZA", "CALL MY TRUSTED ADULT"),
        "en": "Please allow me to call my adult sponsor immediately.",
        "phon": "Plis a-láu mi tu col mai á-dolt spón-sor i-mí-diat-li.",
        "note": S(
            "Significa: «Por favor, déjeme llamar a mi adulto de confianza». Tu familia o patrocinador quiere ayudarte. 🏡",
            "Pida comunicarse con el patrocinador o tutor. Lleve los números importantes anotados en papel, por si le quitan el celular.",
            "This means: “Please let me call my trusted adult.” Your family or sponsor wants to help you. 🏡",
            "Ask to contact the sponsor or guardian. Carry important numbers written on paper in case the phone is taken.",
        ),
    },
    {
        "g": "g-ind", "icon": "🚪",
        "tag": X("EN LA PUERTA", "AT THE DOOR"),
        "en": "I do not consent to entry unless you have a warrant signed by a judge.",
        "phon": "Ai du not kon-sént tu én-tri an-lés yu jav a uó-rant saind bai a yadch.",
        "note": S(
            "Si tocan a la puerta y estás con un adulto, deja que el adulto hable. No tienes que abrir tú solo o sola. 🧸",
            "Una orden administrativa de ICE (formularios I-200 o I-205) no autoriza a entrar a su casa. Solo una orden firmada por un juez lo permite. Puede pedir que se la muestren sin abrir la puerta.",
            "If someone knocks and you are with an adult, let the adult do the talking. You don't have to open the door alone. 🧸",
            "An ICE administrative warrant (forms I-200 or I-205) does not authorize entry into your home. Only a warrant signed by a judge does. You may ask them to show it without opening the door.",
        ),
    },
]

CONT_EN = "Your Honor, I am a minor and I respectfully ask for a continuance so I can find a lawyer."
CONT_ES = "Su Señoría, soy menor de edad y respetuosamente solicito una prórroga («continuance») para poder encontrar un abogado."
CONT_PHON = "Yor Ó-nor, ai am a mái-nor and ai ris-péct-ful-li ask for a kon-tí-niu-ans sou ai kan faind a ló-ier."

CHECKLIST = {
    "es": {
        "kid": [
            ("🌙 Antes de tu cita", [
                "Pregunta a tu adulto de confianza: ¿cuándo y dónde es mi cita?",
                "Pídele que te ayude a buscar un abogado (mira la pestaña Ayuda). 💛",
                "Escribe en un papel el número de tu adulto de confianza.",
                "Dile lo que te da miedo. Es normal tener preguntas.",
            ]),
            ("🎒 La noche anterior", [
                "Alista ropa limpia y cómoda.",
                "Guarda tu tarjeta de bolsillo y tus papeles en la mochila.",
                "Descansa. Puedes abrazar tu peluche. 🧸",
            ]),
            ("🏛️ El día de la cita", [
                "Llega temprano con tu adulto. Hay una revisión de seguridad.",
                "Pon tu celular en silencio.",
                "Si no entiendes algo, di: «No entendí, por favor».",
                "Pide un intérprete si lo necesitas.",
                "Antes de irte, pregunta: ¿cuándo es mi próxima cita?",
            ]),
        ],
        "adult": [
            ("📄 Antes de la audiencia", [
                "Revise su aviso: fecha, hora, dirección o instrucciones para la audiencia en línea.",
                "Confirme su caso en acis.eoir.justice.gov o al 1-800-898-7180.",
                "Contacte hoy a organizaciones de ayuda legal (pestaña Ayuda); las listas de espera se llenan rápido.",
                "Si se mudó, presente el formulario EOIR-33 (cambio de domicilio) dentro de 5 días hábiles.",
                "Reúna documentos: aviso de audiencia, identificaciones, actas de nacimiento y datos de contacto.",
                "Anote en papel los teléfonos del patrocinador y de la organización legal.",
            ]),
            ("🎒 El día anterior", [
                "Planifique el transporte (o pruebe la conexión si es en línea) y pida permiso en el trabajo o la escuela.",
                "Prepare ropa limpia y presentable.",
                "Imprima o guarde la tarjeta de bolsillo.",
            ]),
            ("🏛️ El día de la audiencia", [
                "Llegue con tiempo: hay revisión de seguridad. Si es en línea, entre a tiempo.",
                "Silencie los celulares.",
                "Pida un intérprete si lo necesita.",
                "Responda con la verdad. Si no entiende una pregunta, dígalo.",
                "Si el menor no tiene abogado, use el Guión de Corte (botón central) para pedir más tiempo.",
                "Antes de salir, anote la fecha de la próxima audiencia.",
            ]),
        ],
    },
    "en": {
        "kid": [
            ("🌙 Before your court date", [
                "Ask your trusted adult: when and where is my court date?",
                "Ask them to help you find a lawyer (see the Legal Aid tab). 💛",
                "Write your trusted adult's phone number on paper.",
                "Tell them what scares you. It is normal to have questions.",
            ]),
            ("🎒 The night before", [
                "Pick out clean, comfortable clothes.",
                "Put your pocket card and papers in your backpack.",
                "Rest. You can hug your stuffed animal. 🧸",
            ]),
            ("🏛️ On the day", [
                "Arrive early with your adult. There is a security check.",
                "Put your phone on silent.",
                "If you don't understand, say: “I didn't understand, please.”",
                "Ask for an interpreter if you need one.",
                "Before you leave, ask: when is my next court date?",
            ]),
        ],
        "adult": [
            ("📄 Before the hearing", [
                "Review the notice: date, time, address or online-hearing instructions.",
                "Confirm case information at acis.eoir.justice.gov or 1-800-898-7180.",
                "Contact legal aid organizations today (Legal Aid tab); waitlists fill quickly.",
                "If you moved, file Form EOIR-33 (Change of Address) within 5 working days.",
                "Gather documents: hearing notice, IDs, birth certificates, and contact information.",
                "Write down the sponsor's and the legal organization's phone numbers on paper.",
            ]),
            ("🎒 The day before", [
                "Plan transportation (or test your connection if online) and request time off from work or school.",
                "Prepare clean, neat clothes.",
                "Print or save the pocket card.",
            ]),
            ("🏛️ On the day of the hearing", [
                "Arrive with time to spare: there is a security screening. If online, join on time.",
                "Silence phones.",
                "Ask for an interpreter if you need one.",
                "Answer truthfully. If you don't understand a question, say so.",
                "If the minor has no lawyer, use the Court Script (center button) to ask for more time.",
                "Before leaving, write down the next hearing date.",
            ]),
        ],
    },
}

# Relief cards: strict "may qualify" hedging.
RELIEF = [
    {
        "icon": "🛡️", "name": X("Asilo", "Asylum"),
        "one": X("Es posible que califiques si tienes miedo de volver a tu país de origen por peligro o persecución.",
                 "You may qualify if you are afraid to return to your home country due to danger or persecution."),
        "more": S(
            "El asilo es protección para personas que tienen miedo de volver a su país porque podrían ser lastimadas gravemente. "
            "Algunos ejemplos son violencia en la familia, o ser lastimado por quién eres. Es posible que califiques. Puede tener riesgos, así que habla con un abogado primero.",
            "El asilo puede ser una opción para quien tiene un temor fundado de persecución por parte del gobierno o de un grupo que el gobierno no puede o no quiere controlar, "
            "por raza, religión, nacionalidad, opinión política o pertenencia a un grupo social. La violencia doméstica puede ser una base. "
            "El proceso implica riesgos: consulte con un abogado.",
            "Asylum is protection for people who are afraid to go back to their country because they could be seriously hurt. "
            "Some examples are violence in the family, or being hurt because of who you are. You may qualify. It can involve risk, so talk to a lawyer first.",
            "Asylum may be an option for someone with a well-founded fear of persecution by the government, or by a group the government cannot or will not control, "
            "because of race, religion, nationality, political opinion, or membership in a social group. Domestic violence may qualify as a basis. "
            "The process involves risk: consult a lawyer.",
        ),
    },
    {
        "icon": "👨‍👩‍👧", "name": X("Menor Inmigrante Especial (S.I.J.)", "Special Immigrant Juvenile Status (SIJ)"),
        "one": X("Es posible que califiques si tienes menos de 21 años, no estás casado/a y no puedes vivir con uno o ambos padres biológicos por maltrato, negligencia o abandono (incluye un padre desaparecido o fallecido).",
                 "You may qualify if you are under 21, unmarried, and cannot live with one or both biological parents due to abuse, neglect, or abandonment (including a missing or deceased parent)."),
        "more": S(
            "S.I.J. es una forma de conseguir papeles legales para vivir en EE. UU. Es posible que califiques si no puedes vivir con uno o ambos padres porque te lastimaron, te dejaron o no te cuidaron. "
            "También cuenta si un padre está desaparecido, no aparece en tu acta de nacimiento o falleció. Un juez de EE. UU. también participa. Las reglas de edad son muy importantes: un abogado debe revisarlas.",
            "S.I.J. puede llevar a la residencia permanente. Por lo general se piden estos requisitos: menor de 21 años y soltero/a; un tribunal de menores de EE. UU. lo declaró dependiente o lo puso bajo custodia de una agencia estatal o persona designada; "
            "la reunificación con uno o ambos padres no es viable por maltrato, negligencia, abandono o motivo similar; y no es lo mejor para el menor volver a su país. "
            "Los límites de edad dependen de cada situación: solo un abogado puede decirle cómo aplican.",
            "SIJ is a way to get legal papers to live in the U.S. You may qualify if you can't live with one or both parents because they hurt you, left you, or didn't take care of you. "
            "It also counts if a parent is missing, is not on your birth certificate, or has died. A U.S. judge is also part of this. Age rules are very important: a lawyer must check them.",
            "SIJ may lead to lawful permanent residence. The basic requirements are generally: under 21 and unmarried; declared dependent on a U.S. juvenile court, or placed in the custody of a State agency or court-appointed person; "
            "reunification with one or both parents is not viable due to abuse, neglect, abandonment, or a similar basis; and it is not in the minor's best interest to return to the home country. "
            "Age limits depend on each situation: only a lawyer can tell you how they apply.",
        ),
    },
    {
        "icon": "🧩", "name": X("Visa U", "U-Visa"),
        "one": X("Es posible que califiques si tú (o un padre/hermano) fue víctima de un delito grave en EE. UU. y sufrió daño físico o mental.",
                 "You may qualify if you (or a parent/sibling) were the victim of a serious crime in the U.S. and suffered physical or mental harm."),
        "more": S(
            "La visa U es para víctimas de ciertos delitos graves en EE. UU. Es posible que califiques si tú, tu mamá o papá, o tu hermano/a fue lastimado por un delito grave. "
            "Esto puede incluir violencia en el hogar. La policía u otra autoridad tiene que decir que estás ayudando con el caso. Un abogado puede decirte más.",
            "La visa U es para víctimas de ciertos delitos que sufrieron abuso físico o mental sustancial. Se necesita una certificación de una autoridad federal, estatal o local que indique que la persona ha sido, es o puede ser útil en la investigación o el procesamiento del delito. "
            "Un menor puede calificar si él, su padre/madre o su hermano/a fue víctima de un delito grave en EE. UU., incluida la violencia doméstica. Consulte con un abogado.",
            "The U visa is for victims of certain serious crimes in the U.S. You may qualify if you, your mom or dad, or your brother or sister was hurt by a serious crime. "
            "This can include violence at home. A police or other official has to say you are helping with the case. A lawyer can tell you more.",
            "The U visa is for victims of certain crimes who suffered substantial physical or mental abuse. A certification from a federal, state, or local law enforcement official is needed saying the person is being, has been, or is likely to be helpful to the investigation or prosecution. "
            "A minor may qualify if they, their parent, or their sibling was a victim of a serious crime in the U.S., including domestic violence. Consult a lawyer.",
        ),
    },
    {
        "icon": "🕊️", "name": X("Visa T", "T-Visa"),
        "one": X("Es posible que califiques si te obligaron o engañaron para trabajar, o si fuiste víctima de trata en EE. UU.",
                 "You may qualify if you were forced or tricked into working, or were trafficked, in the U.S."),
        "more": S(
            "La visa T es para víctimas de trata de personas. Es posible que califiques si te trajeron a EE. UU. para trabajar o servir con fuerza, mentiras o presión. "
            "Por ejemplo, si te trajeron para trabajar para un familiar o para pagar una deuda. Si estás en peligro, llama a la línea contra la trata: 1-888-373-7888.",
            "La visa T es para víctimas de una forma grave de trata de personas que están en EE. UU. por causa de la trata o su investigación y que sufrirían daño grave si fueran removidas. "
            "Un menor que haya participado en actos sexuales comerciales también es víctima de trata. Un menor reclutado, albergado o transportado a EE. UU. para trabajo o servicio mediante fuerza, fraude o coacción puede calificar. Consulte con un abogado.",
            "The T visa is for victims of trafficking. You may qualify if you were brought to the U.S. to work or serve through force, lies, or pressure. "
            "For example, being brought to work for a family member or to pay a debt. If you are in danger, call the trafficking hotline: 1-888-373-7888.",
            "The T visa is for victims of a severe form of trafficking who are in the U.S. because of the trafficking or its investigation and who would suffer severe harm if removed. "
            "Any minor who has engaged in commercial sex acts is also a victim of trafficking. A minor recruited, harbored, or transported to the U.S. for labor or service through force, fraud, or coercion may qualify. Consult a lawyer.",
        ),
    },
]

# ---- Locked Q&A bank: 10 curated questions, each with 4 answer variants (kid/adult x es/en) ----
QA_BANK = [
    {
        "q": ("¿Cómo pido más tiempo para encontrar un abogado?", "How do I ask for more time to find a lawyer?"),
        "kid": ("Puedes pedirle al juez más tiempo para encontrar un abogado. En inglés se dice «continuance». Puede ser de 10 a 28 días, como 2 semanas, y el juez decide. Pídelo con respeto y llama a ayuda legal ese mismo día.",
                "You can ask the judge for more time to find a lawyer. In English this is called a “continuance.” It may be 10 to 28 days, about 2 weeks, and the judge decides. Ask politely and call legal aid the same day."),
        "adult": ("Puede pedirle al juez una prórroga («continuance») para buscar abogado. En la práctica actual suele ser de 10 a 28 días (unas 2 semanas), y la decisión es del juez; no está garantizada. Pídala con respeto, comuníquese con una organización de ayuda legal ese mismo día y no falte a la audiencia.",
                  "You may ask the judge for a continuance to find a lawyer. Under current practice it is often 10 to 28 days (about 2 weeks), and the judge decides; it is not guaranteed. Ask respectfully, contact a legal aid organization the same day, and do not miss the hearing."),
    },
    {
        "q": ("¿Qué pasa si mi familia se muda a una nueva dirección?", "What if my family moves to a new address?"),
        "kid": ("Si tu familia se muda, hay que avisar a la corte la nueva dirección. Se usa un papel llamado Formulario EOIR-33. Se hace dentro de 5 días hábiles para no perder las cartas de la corte. Un abogado puede ayudarte con esto.",
                "If your family moves, the court must be told the new address. This uses a paper called Form EOIR-33. It is done within 5 working days so you don't miss letters from the court. A lawyer can help with this."),
        "adult": ("Cuando una persona se muda, se debe informar la nueva dirección a la corte de inmigración con el Formulario EOIR-33 (cambio de domicilio), dentro de 5 días hábiles, para no perder la correspondencia de la corte. Un abogado puede orientarle sobre su caso.",
                  "When a person moves, the immigration court must be told the new address using Form EOIR-33 (Change of Address) within 5 working days so court mail is not missed. A lawyer can talk with you about your own case."),
    },
    {
        "q": ("¿Hay un límite de edad para estas protecciones?", "Is there an age limit for these protections?"),
        "kid": ("Un tipo de protección se llama S.I.J. Puede ser para personas menores de 21 años que no están casadas. Las reglas de edad son muy importantes y cambian según cada persona. Solo un abogado puede revisar cómo se aplican a ti. Habla con un abogado lo antes posible.",
                "One kind of protection is called SIJ. It may be for people who are under 21 and not married. Age rules are very important and are different for each person. Only a lawyer can check how they apply to you. Talk to a lawyer as soon as you can."),
        "adult": ("Una protección es el Estatus de Menor Inmigrante Especial (S.I.J.). La regla básica es ser menor de 21 años y soltero/a. Los límites de edad pueden depender de los detalles de cada situación, y solo un abogado puede decirle cómo se aplican a usted. Hable con un abogado lo antes posible.",
                  "One protection is Special Immigrant Juvenile status (SIJ). The basic rule is being under 21 and unmarried. Age limits can depend on the details of each person's situation, and only a lawyer can tell you how they apply to you. Talk to a lawyer as soon as you can."),
    },
    {
        "q": ("¿Qué es la petición juvenil (S.I.J.)?", "What is Special Immigrant Juvenile (SIJ) status?"),
        "kid": ("S.I.J. es una forma de conseguir papeles legales para vivir en EE. UU. Es posible que una persona califique si es menor de 21 años, no está casada y no puede vivir con uno o ambos padres porque la lastimaron, la dejaron o no la cuidaron. Un juez de EE. UU. también participa. Un abogado puede decirte si te podría aplicar.",
                "SIJ is a way to get legal papers to live in the U.S. A young person may qualify if they are under 21, not married, and cannot live with one or both parents because a parent hurt them, left them, or did not take care of them. A U.S. judge is also part of this. A lawyer can tell you if it may apply to you."),
        "adult": ("S.I.J. es una vía por la cual un joven puede llegar a obtener la residencia permanente. Es posible que califique si: es menor de 21 años y soltero/a; un tribunal de menores de EE. UU. lo declaró dependiente o lo puso bajo custodia de una agencia estatal o de alguien designado; no es viable vivir con uno o ambos padres por maltrato, abandono, negligencia o motivo similar; y volver a su país no le conviene. Solo un abogado puede decirle si califica.",
                  "SIJ is a way a young person may be able to get lawful permanent residence. A young person may qualify if: they are under 21 and unmarried; a U.S. juvenile court declared them dependent or placed them in the custody of a State agency or someone appointed by a court; living with one or both parents is not viable due to abuse, neglect, abandonment, or something similar; and returning to the home country is not in their best interest. Only a lawyer can tell you whether you qualify."),
    },
    {
        "q": ("¿Qué pasa si uno de mis padres está desaparecido, no aparece en mi certificado de nacimiento o falleció?", "What if one of my parents is missing, is not on my birth certificate, or has died?"),
        "kid": ("Si uno de tus padres está desaparecido, no aparece en tu acta de nacimiento o falleció, habla con un abogado sobre S.I.J. Si un padre te lastimó, te dejó o no te cuidó, es posible que califiques. Un abogado puede decirte.",
                "If one of your parents is missing, is not on your birth certificate, or has died, talk to a lawyer about SIJ. If a parent hurt you, left you, or did not take care of you, you may qualify. A lawyer can tell you."),
        "adult": ("Un padre desaparecido, un padre que no aparece en el acta de nacimiento o un padre fallecido son ejemplos de situaciones en las que S.I.J. podría aplicar. Si un menor fue maltratado, abandonado o descuidado por uno de los padres, en EE. UU. o en su país, es posible que califique. Solo un abogado puede decirle si aplica a su situación.",
                  "A missing parent, a father not listed on the birth certificate, or a deceased parent are examples of situations where SIJ may apply. If a child was abused, abandoned, or neglected by one parent, in the U.S. or in the home country, the child may qualify. Only a lawyer can tell you if it applies to your situation."),
    },
    {
        "q": ("¿Qué es VAWA?", "What is VAWA?"),
        "kid": ("VAWA es una protección para un niño o niña que fue lastimado por un padre o madre que es ciudadano o residente permanente de EE. UU. También puede aplicar si el otro padre o un hermano fue lastimado por esa persona. Algunas reglas son complicadas, así que un abogado debe revisar si te aplica.",
                "VAWA is a protection for a child who was hurt by a parent who is a U.S. citizen or lawful permanent resident. It may also apply if the child's other parent or a brother or sister was hurt by that parent. Some rules are complicated, so a lawyer must check if it applies to you."),
        "adult": ("VAWA es una protección para personas maltratadas por un cónyuge o padre/madre que es ciudadano de EE. UU. o residente permanente; el maltrato puede ser hacia usted o hacia su hijo. Un menor puede calificar si él, su padre/madre o su hermano fue maltratado por el padre/madre que es ciudadano o residente. Se piden otros requisitos, como buen carácter moral, y una interpretación reciente de las autoridades podría no permitir la autopetición si la persona entró ilegalmente a EE. UU. Un abogado debe revisar su situación.",
                  "VAWA is a protection for people abused by a U.S. citizen or lawful permanent resident spouse or parent; the abuse can be to you or to your child. A minor may qualify if the minor, the minor's parent, or sibling was abused by the minor's parent who is a U.S. citizen or lawful permanent resident. Other requirements apply, such as good moral character, and a recent interpretation by immigration authorities may not allow a self-petition if the person entered the U.S. illegally. A lawyer must check your situation."),
    },
    {
        "q": ("¿Qué es una visa U?", "What is a U visa?"),
        "kid": ("La visa U es para víctimas de ciertos delitos graves. Es posible que un niño califique si él, su mamá o papá, o su hermano/a fue víctima de un delito grave en EE. UU., incluida la violencia en el hogar. Una autoridad tiene que decir que la persona está ayudando con el caso. Un abogado puede decirte si te podría aplicar.",
                "A U visa is for victims of certain serious crimes. A child may qualify if the child, the child's mom or dad, or the child's brother or sister was a victim of a serious crime in the U.S., including violence at home. An official has to say the person is helping with the case. A lawyer can tell you if it may apply to you."),
        "adult": ("La visa U es para víctimas de ciertos delitos que sufrieron abuso físico o mental sustancial. También se necesita una certificación de una autoridad federal, estatal o local que indique que la persona es, ha sido o puede ser útil en la investigación o el procesamiento del delito. Un menor puede calificar si él, su padre/madre o su hermano fue víctima de un delito grave en EE. UU., incluida la violencia doméstica. Solo un abogado puede decirle si califica.",
                  "A U visa is for victims of certain crimes who suffered substantial physical or mental abuse. A certification is also needed from a federal, state, or local law enforcement official saying the person is being, has been, or is likely to be helpful to the investigation or prosecution. A minor may qualify if the minor, the minor's parent, or sibling was a victim of a serious crime in the U.S., including domestic violence. Only a lawyer can tell you if you qualify."),
    },
    {
        "q": ("¿Qué es una visa T?", "What is a T visa?"),
        "kid": ("La visa T es para víctimas de trata de personas. Es posible que un niño califique si lo trajeron a EE. UU. para trabajar o servir con fuerza, mentiras o presión; por ejemplo, para trabajar para un familiar o pagar una deuda. Un abogado puede decirte si te podría aplicar.",
                "A T visa is for victims of trafficking. A child may qualify if they were brought to the U.S. to work or serve through force, lies, or pressure, for example to work for a family member or pay a debt. A lawyer can tell you if it may apply to you."),
        "adult": ("La visa T es para víctimas de una forma grave de trata de personas. La persona debe estar en EE. UU. por causa de la trata o de su investigación y sufriría daño grave si fuera removida. Un menor que haya participado en actos sexuales comerciales también es víctima de trata. Un menor reclutado, albergado o transportado a EE. UU. para trabajo o servicio mediante fuerza, fraude o coacción puede calificar. Solo un abogado puede decirle si califica.",
                  "A T visa is for victims of a severe form of trafficking. The person must be in the U.S. because of the trafficking or its investigation and would suffer severe harm if removed. Any minor who has engaged in commercial sex acts is also a victim of trafficking. A minor recruited, harbored, or transported to the U.S. for labor or service through force, fraud, or coercion may qualify. Only a lawyer can tell you if you qualify."),
    },
    {
        "q": ("¿Qué es el asilo?", "What is asylum?"),
        "kid": ("El asilo es protección para una persona que tiene miedo de volver a su país porque podría ser lastimada gravemente. Si tienes miedo de volver, es posible que califiques. Puede tener riesgos, así que habla con un abogado.",
                "Asylum is protection for a person who is afraid to go back to their country because they could be seriously harmed. If you are afraid to go back, you may qualify. It can involve risk, so talk to a lawyer."),
        "adult": ("El asilo es protección para una persona con un temor fundado de persecución por parte del gobierno o de un grupo que el gobierno no puede o no quiere controlar, por raza, religión, nacionalidad, opinión política o pertenencia a un grupo social. La violencia doméstica puede ser una base. Un menor con miedo de volver a su país podría calificar. El proceso implica riesgos: consulte con un abogado.",
                  "Asylum is protection for a person with a well-founded fear of persecution by the government, or by a group the government cannot or will not control, because of race, religion, nationality, political opinion, or membership in a social group. Domestic violence may qualify as a basis. A minor afraid to return to their country may qualify. The process involves risk: consult a lawyer."),
    },
    {
        "q": ("¿Qué pasa si fui víctima de un delito, me obligaron a trabajar o tengo miedo de volver a mi país?", "What if I was a victim of a crime, forced to work, or I am afraid to go back to my country?"),
        "kid": ("Puede ser buena idea hablar con un abogado si te lastimó un delito en EE. UU., si alguien te obligó a trabajar con fuerza, mentiras o presión, o si tienes miedo de volver a tu país. Un abogado puede decirte qué protecciones te podrían aplicar.",
                "It can be a good idea to talk to a lawyer if you were hurt by a crime in the U.S., if someone forced you to work through force, lies, or pressure, or if you are afraid to go back to your country. A lawyer can tell you which protections may apply to you."),
        "adult": ("Puede ser útil hablar con un abogado si fue víctima de un delito en EE. UU. y sufrió daño grave; si fue obligado a trabajar o a la industria del sexo mediante fuerza, engaño o presión; o si llegó recientemente y teme persecución en su país. Un abogado puede decirle qué protecciones podrían aplicarle.",
                  "It may help to talk to a lawyer if you were a victim of a crime in the U.S. and suffered serious harm; if you were forced into labor or the sex industry through force, fraud, or coercion; or if you recently arrived and fear persecution in your home country. A lawyer can tell you which protections may apply."),
    },
]

# ---- Guardrail verification: every Q&A answer must pass BEFORE it is displayed ----
BANNED_PATTERNS = [
    r"\bguarantee", r"\bdefinitely\b", r"\bfor sure\b", r"\byou will (win|lose|get|be approved|be deported)\b",
    r"\byou are eligible\b", r"\byou should (file|apply|sign|leave|stay|lie)\b", r"\byou must (file|apply|sign)\b",
    r"\bi recommend\b", r"\bwe recommend\b", r"\bfree (lawyer|attorney)\b",
    r"garantiz", r"\bseguro que\b", r"definitivamente", r"\bser[aá] (aprobad|deportad)", r"\bdebe(s)? (presentar|solicitar|firmar)\b",
    r"\bte recomiendo\b", r"\bse recomienda\b", r"\babogado (gratis|gratuito)\b",
]
LAWYER_RE = re.compile(r"lawyer|attorney|legal aid|abogad|ayuda legal", re.I)
SAFE_FALLBACK = X(
    "Esta respuesta no pasó la verificación de seguridad, así que no se muestra. Hable con un abogado o una organización de ayuda legal.",
    "This answer did not pass the safety check, so it is not shown. Please talk to a lawyer or a legal aid organization.",
)


def verify_answer(answer: str, disclaimer: str):
    """Return (passed, text_to_show). Blocks legal advice / promises; requires lawyer referral + disclaimer."""
    low = answer.lower()
    for pat in BANNED_PATTERNS:
        if re.search(pat, low):
            return False, SAFE_FALLBACK
    if not LAWYER_RE.search(answer):
        return False, SAFE_FALLBACK
    final = f"{answer}\n\n{disclaimer}"
    if disclaimer not in final:
        return False, SAFE_FALLBACK
    return True, final


# ------------------------------------------------------------------
# AVATARS (3D clay characters)
# ------------------------------------------------------------------
CUBE_FACES = (
    '<div class="face f-right"></div><div class="face f-left"></div>'
    '<div class="face f-back"></div><div class="face f-top"></div><div class="face f-bottom"></div>'
)
FACE_FEATURES = '<div class="hair"></div><div class="eye l"></div><div class="eye r"></div><div class="smile"></div>'


def avatar_html(role: str) -> str:
    title = ROLES[role]["title"]
    if role == "judge":
        stage = "stage-judge"
        scene = (
            '<div class="iso-floor floor-judge"></div>'
            '<div class="cube judge-bench"><div class="face f-front"><div class="plate"></div></div>' + CUBE_FACES + '</div>'
            '<div class="fig fig-judge"><div class="robe"></div><div class="jabot"></div>'
            '<div class="head wig">' + FACE_FEATURES + '</div><div class="gavel"></div></div>'
        )
    elif role == "fiscal":
        stage = "stage-fiscal"
        scene = (
            '<div class="iso-floor floor-fiscal"></div>'
            '<div class="cube suit-block"><div class="face f-front"><div class="collar"></div><div class="tie"></div>'
            '<div class="case"><div class="case-handle"></div><div class="case-clasp"></div></div></div>' + CUBE_FACES + '</div>'
            '<div class="fig fig-fiscal"><div class="neck"></div><div class="head">' + FACE_FEATURES + '</div></div>'
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
# PAGE: HOME
# ==================================================================
def page_home():
    html(f"""
    <div class="hero">
    <p class="h1">{S("¡Hola! Vamos a prepararnos juntos 💙", "Prepárese para la audiencia de inmigración", "Hi! Let's get ready together 💙", "Get ready for immigration court")}</p>
    <p class="h2">{S("Aquí aprendes quién es quién, qué decir y a dónde pedir ayuda. No te pedimos tu nombre ni guardamos nada tuyo.",
                     "Guía de preparación y derechos para niños, jóvenes y sus familias. Esta herramienta no tiene formularios ni campos de texto y no guarda información personal.",
                     "Here you learn who is who, what to say, and where to ask for help. We don't ask for your name and we don't save anything about you.",
                     "A preparation and rights guide for children, teens, and their families. This tool has no forms or text fields and does not save personal information.")}</p>
    </div>
    """)
    banner()

    # 5-working-day EOIR-33 callout
    html(f"""
    <div class="clay coral">
    <h4>📮 {X("Si te mudas, avisa a la corte", "If you move, tell the court")}</h4>
    <p>{S("Si tú o tu familia se mudan, avisa la nueva dirección a la corte con un papel llamado <b>Formulario EOIR-33</b> (Cambio de dirección). Hazlo dentro de <b>5 días hábiles</b> para no perder las cartas de la corte.",
          "Si usted es un joven sin abogado y se muda, presente el <b>Formulario EOIR-33 (Cambio de domicilio)</b> dentro de <b>5 días hábiles</b> para no perder nunca la correspondencia de la corte.",
          "If you or your family move, tell the court your new address with a paper called <b>Form EOIR-33</b> (Change of Address). Do it within <b>5 working days</b> so you don't miss letters from the court.",
          "If you are a young person without a lawyer and you move, file <b>Form EOIR-33 (Change of Address)</b> within <b>5 working days</b> so you never miss court mail.")}</p>
    </div>
    """)

    html(f'<p class="sec">{X("🏛️ Mi audiencia", "🏛️ My hearing")}</p>')
    st.radio(
        "Tipo de audiencia / Hearing type",
        ["inperson", "virtual"],
        format_func=lambda v: (("🏛️ En persona" if v == "inperson" else "💻 En línea (Webex)") if lang == "es"
                               else ("🏛️ In person" if v == "inperson" else "💻 Online (Webex)")),
        horizontal=True, label_visibility="collapsed", key="htype",
    )

    if st.session_state.htype == "inperson":
        st.write(S(
            "Así se ve un salón de la corte. Toca a una persona para saber quién es. ¡Nada de esto muerde! 😊",
            "Distribución típica de una sala de inmigración. Toque cada rol para ver su función.",
            "This is what a courtroom looks like. Tap a person to find out who they are. Nobody here bites! 😊",
            "Typical layout of an immigration courtroom. Tap each role to see what they do.",
        ))
        sel = st.session_state.role

        def cls(n):
            return "active" if sel == n else ""

        gov = ROLES["fiscal"]["title"].replace("The Government Lawyer", "Gov. Lawyer")
        html(f"""
        <div class="court-wrap"><div class="court-floor">
        <div class="block judge {cls('judge')}">{ROLES['judge']['title']}</div>
        <div class="court-row">
        <div class="block fiscal {cls('fiscal')}">{gov}</div>
        <div class="block interp {cls('interprete')}">{ROLES['interprete']['title']}</div>
        </div>
        <div class="block you">{X("👤 Tu lugar", "👤 Your spot")}</div>
        </div></div>
        """)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.button(X("⚖️ Juez", "⚖️ Judge"), key="b_judge", on_click=set_role, args=("judge",))
        with c2:
            st.button(X("💼 Fiscal", "💼 Gov. Lawyer"), key="b_fiscal", on_click=set_role, args=("fiscal",))
        with c3:
            st.button(X("🗣️ Intérprete", "🗣️ Interpreter"), key="b_interp", on_click=set_role, args=("interprete",))
        if sel:
            r = ROLES[sel]
            html(avatar_html(sel))
            html(f'<div class="clay {r["css"]}"><h4>{r["title"]}</h4><p>{r["text"]}</p></div>')
        else:
            html(f'<p class="hint">{X("👆 Toca un botón para ver quién es cada persona.", "👆 Tap a button to see who each person is.")}</p>')
    else:
        # Virtual / Webex guide
        st.write(S(
            "Algunas citas son en línea, por computadora o celular. Estas son las reglas para sentirte listo o lista. 💻",
            "Cada vez más audiencias son en línea, por Webex. Estas son las reglas básicas para una audiencia virtual.",
            "Some court dates are online, on a computer or phone. Here are the rules so you feel ready. 💻",
            "More and more hearings are held online through Webex. These are the basic rules for a virtual hearing.",
        ))
        html(f"""
        <div class="steps">
        <div class="tile"><p class="ic">⏰</p><p class="tt">{X("Entra a tiempo", "Join on time")}</p>
        <p class="tx">{S("Conéctate con tu adulto antes de que empiece.", "Ingrese a la sala virtual a tiempo, antes de la hora de inicio.", "Log in with your adult before it starts.", "Enter the virtual room on time, before the start time.")}</p></div>
        <div class="tile"><p class="ic">📷</p><p class="tt">{X("Cámara encendida", "Camera on")}</p>
        <p class="tx">{S("Deja tu cámara prendida para que el juez te vea.", "Mantenga la cámara encendida durante toda la audiencia.", "Keep your camera on so the judge can see you.", "Keep your camera on for the whole hearing.")}</p></div>
        <div class="tile"><p class="ic">🔇</p><p class="tt">{X("Micrófono en silencio", "Stay muted")}</p>
        <p class="tx">{S("Silencia tu micrófono hasta que digan tu nombre.", "Mantenga el micrófono silenciado hasta que llamen su nombre.", "Mute your microphone until your name is called.", "Stay muted until your name is called.")}</p></div>
        <div class="tile"><p class="ic">👔</p><p class="tt">{X("Vístete bien", "Dress neatly")}</p>
        <p class="tx">{S("Ponte ropa limpia y ordenada, como para ir a la corte.", "Use ropa limpia y presentable, como si fuera en persona.", "Wear clean, neat clothes, like you're going to court.", "Wear clean, presentable clothes, as if appearing in person.")}</p></div>
        </div>
        """)
        html(f"""
        <div class="banner teal">💡 {X(
            "Para saber cómo conectarte, revisa tu aviso de audiencia o pregunta a tu abogado u organización de ayuda legal. Si no entiendes algo, pide un intérprete. Las audiencias en línea pueden cambiar rápido: revisa tu información seguido.",
            "Para saber cómo conectarse, revise su aviso de audiencia o consulte a su abogado u organización de ayuda legal. Si no entiende algo, pida un intérprete. Las audiencias en línea pueden cambiar rápidamente: revise su información con frecuencia.") if mode == "adult" or lang == "en" else ""}
        {"" if (mode == "adult" or lang == "en") else ""}</div>
        """ if False else "")
        tip = S(
            "Para saber cómo conectarte, mira tu aviso de la corte o pregunta a tu adulto de confianza. Si no entiendes algo, pide un intérprete. 💛",
            "Para saber cómo conectarse, revise su aviso de audiencia o consulte a su abogado u organización de ayuda legal. Si no entiende algo, pida un intérprete. Las audiencias en línea pueden cambiar con rapidez: revise su información con frecuencia.",
            "To find out how to connect, look at your court notice or ask your trusted adult. If you don't understand something, ask for an interpreter. 💛",
            "To find out how to connect, review your hearing notice or ask your lawyer or legal aid organization. If you don't understand something, ask for an interpreter. Online hearings can change quickly: check your information often.",
        )
        html(f'<div class="banner teal">💡 {tip}</div>')

    # No lawyer? point to the script
    html(f"""
    <div class="clay mint">
    <h4>🗣️ {X("¿No tienes abogado?", "No lawyer yet?")}</h4>
    <p>{S("Toca el botón redondo de abajo para ver las palabras que puedes decirle al juez. Ya están escritas para ti. 💛",
          "Si el menor comparece sin abogado, el botón central (Guión de Corte) tiene el texto para pedir más tiempo, con audio y pronunciación.",
          "Tap the round button below to see the words you can say to the judge. They are already written for you. 💛",
          "If the minor appears without a lawyer, the center button (Court Script) has the text to ask for more time, with audio and pronunciation.")}</p>
    </div>
    """)

    # Checklist
    with st.expander(X("📋 Mi lista para el día de la audiencia", "📋 My day-of-hearing checklist"), expanded=False):
        st.caption(S(
            "Toca cada casilla cuando termines un paso. ¡Vas muy bien! 🌟",
            "Marque cada casilla al completar un paso. Las casillas solo se ven en su pantalla y no se guardan.",
            "Tap each box when you finish a step. You're doing great! 🌟",
            "Check each box as you complete a step. The boxes only appear on your screen and are not saved.",
        ))
        html(f"""
        <div class="banner">⚠️ <b>{X("Muy importante:", "Very important:")}</b>
        {S("Es muy importante ir a todas tus citas. Si no vas, el juez puede decidir sin escucharte. Si no puedes ir, díselo YA a tu adulto de confianza o a tu abogado.",
           "Es fundamental asistir a todas las audiencias. Si no se presenta, el juez puede ordenar la deportación sin escucharle (orden «en ausencia»). Si no puede asistir, contacte a su abogado de inmediato.",
           "It is very important to go to every court date. If you don't go, the judge can decide without hearing you. If you can't go, tell your trusted adult or your lawyer RIGHT AWAY.",
           "Attending every hearing is essential. If you do not appear, the judge can order removal without hearing you (an “in absentia” order). If you cannot attend, contact your lawyer immediately.")}</div>
        """)
        for i, (section, items) in enumerate(CHECKLIST[lang][mode]):
            html(f'<p class="sec" style="font-size:16px;margin-top:12px;">{section}</p>')
            for j, item in enumerate(items):
                st.checkbox(item, key=f"chk_{lang}_{mode}_{i}_{j}")


# ==================================================================
# PAGE: Q&A (locked, guardrailed)
# ==================================================================
def page_qa():
    html(f"""
    <div class="hero">
    <p class="h1">💬 {X("Preguntas comunes", "Common questions")}</p>
    <p class="h2">{X("10 preguntas escritas y revisadas con anticipación. Aquí no hay chat abierto: nada se inventa en el momento y no hay cuadros para escribir.",
                     "10 pre-written, pre-reviewed questions. There is no open chat here: nothing is made up on the spot and there are no boxes to type in.")}</p>
    </div>
    """)
    banner()
    html(f'<div class="banner teal">🔒 {X("Cada respuesta pasa una verificación automática antes de mostrarse: sin consejos legales ni promesas, con referencia a un abogado y con aviso educativo.", "Every answer passes an automatic check before it is shown: no legal advice or promises, a referral to a lawyer, and an educational notice.")}</div>')

    passed_count = 0
    for n, item in enumerate(QA_BANK, start=1):
        i_lang = 0 if lang == "es" else 1
        answer = item[mode][i_lang]
        ok, shown = verify_answer(answer, DISC_SHORT)
        passed_count += int(ok)
        with st.expander(f"{n}. {item['q'][i_lang]}"):
            if ok:
                html(f'<span class="qa-ok">✔ {X("Verificada", "Verified")}</span>')
            st.write(shown)
    st.caption(X(f"{passed_count} de {len(QA_BANK)} respuestas pasaron la verificación.", f"{passed_count} of {len(QA_BANK)} answers passed the check."))


# ==================================================================
# PAGE: RELIEF
# ==================================================================
def page_relief():
    html(f"""
    <div class="hero">
    <p class="h1">🌱 {X("Opciones de alivio comunes", "Common relief options")}</p>
    <p class="h2">{S("Hay protecciones que a veces ayudan a niños y jóvenes. Toca una tarjeta para leer más. Un abogado puede decirte si alguna te podría servir.",
                     "Estas son algunas protecciones comunes. Cada una tiene más requisitos y excepciones. Esta información no es asesoría legal: solo un abogado puede evaluar su caso.",
                     "There are protections that sometimes help kids and teens. Tap a card to read more. A lawyer can tell you if one may fit you.",
                     "These are some common protections. Each has more requirements and exceptions. This information is not legal advice: only a lawyer can evaluate your case.")}</p>
    </div>
    """)
    banner()
    for r in RELIEF:
        with st.expander(f"{r['icon']}  {r['name']}"):
            html(f'<div class="banner teal"><b>{X("Es posible que califiques:", "You may qualify:")}</b><br>{r["one"]}</div>')
            st.write(r["more"])
    html(f"""
    <div class="clay ind">
    <h4>👩‍⚖️ {X("Habla con un abogado", "Talk to a lawyer")}</h4>
    <p>{X("Las reglas de edad y los requisitos dependen de cada persona. Llama a ayuda legal el mismo día; las listas de espera se llenan rápido.",
          "Age rules and requirements depend on each person. Call legal aid the same day; waitlists fill quickly.")}</p>
    </div>
    """)
    st.button(X("📞 Ver organizaciones de ayuda", "📞 See legal aid organizations"), key="relief_to_aid", on_click=go, args=("aid",))


# ==================================================================
# PAGE: LEGAL AID DIRECTORY
# ==================================================================
def page_aid():
    html(f"""
    <div class="hero">
    <p class="h1">🤝 {X("Ayuda legal en Texas", "Texas legal aid")}</p>
    <p class="h2">{S("Hay personas buenas cuyo trabajo es ayudar a niños y jóvenes como tú. Pídele a un adulto de confianza que te ayude a llamar. 💛",
                     "Presione los botones para llamar directamente. Confirme disponibilidad y requisitos al llamar.",
                     "There are good people whose job is to help kids and teens like you. Ask a trusted adult to help you call. 💛",
                     "Press the buttons to call directly. Confirm availability and eligibility when you call.")}</p>
    </div>
    """)
    html(f"""
    <div class="banner">⏳ <b>{X("Aviso de capacidad:", "Capacity warning:")}</b>
    {X("Las listas de espera de las organizaciones sin fines de lucro se llenan rápido por falta de fondos, y algunas han tenido que dejar de representar a menores. Llame hoy, llame a más de una organización y siga intentando. No espere: también puede pedirle más tiempo al juez en su audiencia.",
       "Nonprofit waitlists fill quickly because of funding limits, and some organizations have had to stop representing minors. Call today, call more than one organization, and keep trying. Don't wait: you can also ask the judge for more time at your hearing.")}</div>
    """)
    banner()

    html('<p class="sec">📍 Lobos Immigration Project</p>')
    st.link_button(X("📞 Llamar a Lobos (512-409-5263)", "📞 Call Lobos (512-409-5263)"), "tel:5124095263")
    st.caption(X("Recurso en Texas para jóvenes migrantes. Llame para saber si puede ayudarle con su caso.",
                 "Texas resource for young migrants. Call to find out if they may be able to help with your case."))

    html('<p class="sec">⚖️ KIND</p>')
    st.link_button(X("📞 Llamar a KIND (832-779-4340)", "📞 Call KIND (832-779-4340)"), "tel:8327794340")
    st.caption(X("Ayuda legal para niños no acompañados con casos de inmigración.", "Legal help for unaccompanied children with immigration cases."))

    html('<p class="sec">✊ FIEL Houston</p>')
    st.link_button(X("📞 Llamar a FIEL (713-364-3435)", "📞 Call FIEL (713-364-3435)"), "tel:7133643435")
    st.caption(X("Organización comunitaria liderada por inmigrantes: orientación familiar y defensa de derechos.",
                 "Immigrant-led community organization: family guidance and rights advocacy."))

    html('<p class="sec">🛡️ RAICES Texas</p>')
    st.link_button(X("📞 Llamar a RAICES (210-222-0960)", "📞 Call RAICES (210-222-0960)"), "tel:2102220960")
    st.caption(X("Servicios legales y de representación migratoria en Texas.", "Legal services and immigration representation across Texas."))

    html(f"""
    <div class="clay ind">
    <h4>📝 {X("Qué decir cuando llames", "What to say when you call")}</h4>
    <p>• {X("Tu nombre completo y tu edad exacta.", "Your full name and exact age.")}<br>
    • {X("Tu «Número A» (9 dígitos, empieza con A) si lo tienes en tus papeles.", "Your 9-digit “A-Number” (starts with A) if it's on your papers.")}<br>
    • {X("La fecha, la hora y la ciudad de tu próxima audiencia.", "The date, time, and city of your next hearing.")}<br>
    • {X("«Soy menor de edad, no tengo abogado y necesito ayuda legal.»", "“I am a minor, I don't have a lawyer, and I need legal help.”")}</p>
    </div>
    """)

    html('<p class="sec">🔎 ' + X("Más ayuda", "More help") + '</p>')
    st.link_button(X("Directorio nacional de servicios legales", "National legal services directory"), "https://www.immigrationadvocates.org/legaldirectory/")
    st.link_button(X("Lista oficial de abogados pro bono (EOIR)", "Official pro bono legal service providers (EOIR)"), "https://www.justice.gov/eoir/list-pro-bono-legal-service-providers")
    st.link_button(X("Info de tu caso · 1-800-898-7180", "Case information · 1-800-898-7180"), "tel:18008987180")
    st.link_button(X("Línea contra la trata · 1-888-373-7888", "Human trafficking hotline · 1-888-373-7888"), "tel:18883737888")
    st.link_button(X("Emergencia · 911", "Emergency · 911"), "tel:911")


# ==================================================================
# PAGE: COURT SCRIPT + AUDIO COACH + POCKET CARD
# ==================================================================
def page_script():
    html(f"""
    <div class="hero">
    <p class="h1">🗣️ {X("Guión de Corte", "Court Script")}</p>
    <p class="h2">{S("Si el juez te llama y no tienes abogado, puedes leer estas palabras en voz alta. Practica con el audio. 💛",
                     "Si el menor comparece sin abogado, puede leer este texto al juez o mostrarlo en pantalla. Pedir tiempo para conseguir representación es una petición común.",
                     "If the judge calls you and you don't have a lawyer, you can read these words out loud. Practice with the audio. 💛",
                     "If the minor appears without a lawyer, they can read this text to the judge or show it on screen. Asking for time to find representation is a common request.")}</p>
    </div>
    """)
    banner()

    html(f"""
    <div class="phrase g-ind">
    <p class="icon">⏳</p>
    <p class="tag">🇺🇸 {X("LEE ESTO AL JUEZ", "READ THIS ALOUD TO THE JUDGE")}</p>
    <p class="big">“{CONT_EN}”</p>
    </div>
    """)
    html(f'<p class="note"><b>{X("En español:", "In Spanish:")}</b> {CONT_ES}</p>')
    audio_coach(CONT_EN, CONT_PHON)

    html(f"""
    <div class="clay coral">
    <h4>⏱️ {X("¿Cuánto tiempo me pueden dar?", "How much time might I get?")}</h4>
    <p>{S("El juez decide. Muchas veces dan de <b>10 a 28 días</b>, como 2 semanas. No es seguro. Por eso, <b>llama a ayuda legal el mismo día</b> y nunca faltes a tu cita.",
          "Con la práctica actual, un aplazamiento suele ser de <b>10 a 28 días</b> (unas 2 semanas). La decisión es del juez y no está garantizada. <b>Llame a ayuda legal ese mismo día</b> y no falte a ninguna audiencia.",
          "The judge decides. Often it is <b>10 to 28 days</b>, about 2 weeks. It is not certain. So <b>call legal aid the very same day</b> and never skip your court date.",
          "Under current practice, a continuance is often <b>10 to 28 days</b> (about 2 weeks). The judge decides and it is not guaranteed. <b>Call legal aid the very same day</b> and do not miss any hearing.")}</p>
    </div>
    """)
    st.button(X("📞 Ir a ayuda legal", "📞 Go to legal aid"), key="script_to_aid", on_click=go, args=("aid",))

    html(f'<p class="sec">📣 {X("Otras frases importantes", "Other important phrases")}</p>')
    html(f'<p class="note">{S("Si un oficial te hace preguntas y tienes miedo, respira despacio. Puedes mostrar estas tarjetas sin decir nada más. 💙", "Si un agente le detiene, mantenga la calma y muestre estas tarjetas. Hable lo mínimo. No mienta ni muestre documentos falsos.", "If an officer asks you questions and you feel scared, breathe slowly. You can show these cards without saying anything else. 💙", "If an agent stops you, stay calm and show these cards. Say as little as possible. Do not lie or show false documents.")}</p>')
    for p in PHRASES:
        html(f"""
        <div class="phrase {p['g']}">
        <p class="icon">{p['icon']}</p>
        <p class="tag">{p['tag']}</p>
        <p class="big">“{p['en']}”</p>
        </div>
        """)
        audio_coach(p["en"], p["phon"])
        html(f'<p class="note">{p["note"]}</p>')

    # Pocket card (print / screenshot)
    html(f'<p class="sec">🖨️ {X("Tarjeta de bolsillo", "Pocket card")}</p>')
    st.write(X("Toma una captura de pantalla de esta tarjeta o imprime esta página. Guarda el papel en tu bolsillo por si te quitan el celular:",
               "Take a screenshot of this card or print this page. Keep the paper in your pocket in case your phone is taken:"))
    banner()
    html(f"""
    <div class="wallet">
    <p style="text-align:center; font-weight:900; font-size:17px; margin:0;">{APP_NAME.upper()} · TARJETA DE BOLSILLO / POCKET CARD</p>
    <p style="font-size:11.5px; text-align:center; margin:6px 0 0 0;">GENERAL EDUCATIONAL INFORMATION ONLY. NOT LEGAL ADVICE. NO ATTORNEY-CLIENT RELATIONSHIP. / SOLO INFORMACIÓN EDUCATIVA. NO ES ASESORÍA LEGAL. NO CREA RELACIÓN ABOGADO-CLIENTE.</p>
    <hr>
    <p style="font-size:14px; font-weight:900; margin:0 0 4px 0;">COURT SCRIPT / GUIÓN PARA LA CORTE:</p>
    <p style="font-size:14px; font-style:italic; margin:0;">"{CONT_EN}"</p>
    <p style="font-size:12.5px; margin:4px 0 0 0;">{CONT_ES}</p>
    <hr>
    <p style="font-size:14px; font-weight:900; margin:0 0 4px 0;">FIELD ENCOUNTERS / ENCUENTROS CON AGENTES:</p>
    <p style="font-size:13.5px; font-style:italic; margin:0 0 4px 0;">1. "I am exercising my right to remain silent until I speak to a lawyer."</p>
    <p style="font-size:13.5px; font-style:italic; margin:0 0 4px 0;">2. "I require a Spanish interpreter. I do not understand English well."</p>
    <p style="font-size:13.5px; font-style:italic; margin:0;">3. "Please allow me to call my adult sponsor immediately."</p>
    <hr>
    <p style="font-size:14px; font-weight:900; margin:0 0 4px 0;">MI CONTACTO / MY CONTACT:</p>
    <p style="font-size:13.5px; margin:0;">Nombre / Name: {BLANK}</p>
    <p style="font-size:13.5px; margin:6px 0 0 0;">Tel: {BLANK}</p>
    <p style="font-size:13.5px; margin:6px 0 0 0;">Abogado / Lawyer: {BLANK}</p>
    <p style="font-size:13.5px; margin:6px 0 0 0;">Próxima audiencia / Next hearing: {BLANK}</p>
    <p style="font-size:13.5px; margin:6px 0 0 0;">Nueva dirección → EOIR-33 (5 días hábiles / 5 working days)</p>
    </div>
    """)
    st.caption(X("Escribe tus datos a mano en la versión impresa. Esta app no te pide ni guarda ninguna información.",
                 "Write your information by hand on the printed copy. This app does not ask for or save any information."))


# ------------------------------------------------------------------
# ROUTER
# ------------------------------------------------------------------
PAGES = {"home": page_home, "qa": page_qa, "relief": page_relief, "aid": page_aid, "script": page_script}
PAGES.get(st.session_state.page, page_home)()

html(f"""
<hr style="border:none;border-top:1px solid #DAD8F5;margin:26px 0 8px 0;">
<p style="font-size:12px;color:#5B5F7E;line-height:1.5;">🔒 {X(
    "Privacidad: esta app no tiene formularios, cuentas, cookies propias ni análisis, y no guarda tu nombre ni información personal. Como cualquier sitio web, el servicio de hospedaje puede registrar datos técnicos básicos de conexión; esta app no los ve ni los usa. El audio usa la voz de tu propio navegador.",
    "Privacy: this app has no forms, accounts, cookies of its own, or analytics, and it does not store your name or personal information. Like any website, the hosting service may log basic technical connection data; this app does not see or use it. Audio uses your own browser's voice.")}
<br>{DISCLAIMER_BANNER}</p>
""")

# ------------------------------------------------------------------
# FLOATING BOTTOM DOCK (app-style tab bar)
# ------------------------------------------------------------------
with st.container(key="dock"):
    cols = st.columns([1, 1, 1.15, 1, 1])
    with cols[0]:
        st.button(f"🏠\n\n{X('Inicio', 'Home')}", key="nav_home", on_click=go, args=("home",))
    with cols[1]:
        st.button(f"💬\n\n{X('Preguntas', 'Q&A')}", key="nav_qa", on_click=go, args=("qa",))
    with cols[2]:
        st.button("🗣️", key="nav_center", on_click=go, args=("script",),
                  help=X("Guión de Corte y audio", "Court Script & audio coach"))
    with cols[3]:
        st.button(f"🌱\n\n{X('Alivio', 'Relief')}", key="nav_relief", on_click=go, args=("relief",))
    with cols[4]:
        st.button(f"🤝\n\n{X('Ayuda', 'Legal Aid')}", key="nav_aid", on_click=go, args=("aid",))
