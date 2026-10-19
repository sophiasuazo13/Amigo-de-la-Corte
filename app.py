import streamlit as st

# Set up mobile-responsive page configuration
st.set_page_config(
    page_title="Amigo de la Corte",
    page_icon="🏛️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS styling for premium mobile UI and the interactive court layout
st.markdown("""
    <style>
    /* Styling for mobile-friendly navigation tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 20px;
        padding: 8px 16px;
        font-weight: bold;
        color: #1e293b;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e3a8a !important;
        color: white !important;
    }
    
    /* Interactive Courtroom Map Styling */
    .court-container {
        background-color: #0f172a;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    .court-bench {
        background-color: #854d0e;
        color: white;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 18px;
        margin: 0 auto 15px auto;
        width: 80%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .court-middle {
        display: flex;
        justify-content: space-around;
        margin-bottom: 15px;
        gap: 10px;
    }
    .court-box {
        color: white;
        padding: 12px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 14px;
        flex: 1;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .prosecutor { background-color: #b91c1c; }
    .interpreter { background-color: #1d4ed8; }
    .child-podium {
        background-color: #1e293b;
        color: #38bdf8;
        border: 2px dashed #38bdf8;
        padding: 12px;
        border-radius: 8px;
        font-weight: bold;
        width: 50%;
        margin: 0 auto;
    }

    /* Fixed Emergency Script Box */
    .emergency-box {
        background-color: #ea580c;
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin-top: 15px;
        box-shadow: 0 4px 10px rgba(234,88,12,0.3);
    }

    /* Premium Flashcards for Tab 2 */
    .rights-card {
        padding: 25px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 15px;
        font-weight: bold;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .card-red { background: linear-gradient(135deg, #ef4444, #b91c1c); }
    .card-blue { background: linear-gradient(135deg, #3b82f6, #1d4ed8); }
    .card-green { background: linear-gradient(135deg, #22c55e, #15803d); }
    
    /* Wallet Card Border */
    .wallet-card-border {
        border: 3px dashed #0f172a;
        padding: 20px;
        background-color: #ffffff;
        color: #0f172a;
        border-radius: 8px;
    }
    </style>
    """, unsafe_markdown=True)

# Application Header
st.title("🏛️ Amigo de la Corte")
st.markdown("<p style='font-size:16px; color:#64748b; margin-top:-15px;'>Guía interactiva de preparación legal y derechos para menores de edad</p>", unsafe_markdown=True)

# Set up optimized layout tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏛️ Mi Corte", "📣 Habla Por Mí", "🖨️ Tarjeta de Bolsillo", "🤝 Recursos"])

# ==========================================
# TAB 1: MI CORTE (Interactive Walkthrough)
# ==========================================
with tab1:
    st.markdown("### 🗺️ El Mapa de la Sala del Tribunal")
    st.write("Presiona los botones de abajo para ver quién se sienta en cada lugar y qué hacen:")
    
    # Rendered Flat-Design Court Layout Map
    st.markdown("""
    <div class="court-container">
        <div class="court-bench">⚖️ El Juez de Inmigración (Frontal)</div>
        <div class="court-middle">
            <div class="court-box prosecutor">💼 El Fiscal (Gobierno)</div>
            <div class="court-box interpreter">🗣️ El Intérprete</div>
        </div>
        <div class="child-podium">👤 Tu Lugar (Podio)</div>
    </div>
    """, unsafe_markdown=True)
    
    # Interactive selection controls
    role = st.radio("Selecciona una persona para aprender más:", ["⚖️ El Juez", "💼 El Fiscal / Abogado del Gobierno", "🗣️ El Intérprete"], horizontal=True)
    
    if role == "⚖️ El Juez":
        st.info("**El Juez de Inmigración:** Es la persona encargada de decidir si puedes quedarte legalmente en los Estados Unidos. No trabaja para ICE y no es tu enemigo. Debes hablarle con total honestidad y llamarle **'Su Señoría'** o **'Your Honor'**.")
    elif role == "💼 El Fiscal / Abogado del Gobierno":
        st.error("**El Fiscal del Gobierno:** Es un abogado que representa los intereses del departamento de inmigración. Su tarea es presentar los argumentos legales ante las leyes de deportación. **No es tu defensor personal** y no tienes que responder preguntas difíciles sin asesoría.")
    elif role == "🗣️ El Intérprete":
        st.blueprint = st.success("**El Intérprete de la Corte:** Su único trabajo es traducir con absoluta precisión todo lo que dices al inglés, y todo lo que el juez dice al español. Si no entiendes alguna palabra o dialecto de tu intérprete, tienes el derecho de decírselo al juez de inmediato.")

    st.markdown("### 🚨 Frase de Defensa si estás solo")
    st.write("Si llegas al podio frente al juez y no tienes un abogado que te represente, muestra tu pantalla o lee este texto en voz alta palabra por palabra:")
    
    st.markdown("""
    <div class="emergency-box">
        <p style="font-size:16px; margin:0; text-transform:uppercase; opacity:0.9; font-weight:bold;">🇺🇸 READ THIS ALOUD TO THE JUDGE / LEE ESTO AL JUEZ:</p>
        <p style="font-size:22px; font-weight:bold; line-height:1.4; margin-top:5px;">
        "Hello Your Honor. My name is [Your Name]. I am a minor, I do not have a lawyer today, and I respectfully request a continuance so I can secure free legal representation."
        </p>
    </div>
    """, unsafe_markdown=True)
    st.markdown("**Traducción al Español:** *'Hola Su Señoría. Mi nombre es [Tu Nombre]. Soy menor de edad, no cuento con un abogado hoy, y solicito respetuosamente un aplazamiento para poder conseguir representación legal gratuita.'*")

# ==========================================
# TAB 2: HABLA POR MÍ (Premium Flashcards)
# ==========================================
with tab2:
    st.markdown("### 📣 Tarjetas de Derechos de Emergencia")
    st.write("Si te interceptan agentes de ICE o la policía migratoria en la calle, mantén la calma y muestra estas tarjetas directamente en tu pantalla:")
    
    st.markdown("""
    <div class="rights-card card-red">
        <p style="font-size:14px; margin:0; text-transform:uppercase; opacity:0.8;">🔴 DERECHO A GUARDAR SILENCIO / RIGHT TO SILENCE</p>
        <p style="font-size:24px; margin:8px 0 0 0; line-height:1.3;">"I am exercising my constitutional right to remain silent until I speak to a lawyer."</p>
    </div>
    """, unsafe_markdown=True)
    
    st.markdown("""
    <div class="rights-card card-blue">
        <p style="font-size:14px; margin:0; text-transform:uppercase; opacity:0.8;">🔵 DERECHO A TRADUCCIÓN / INTERPRETER REQUEST</p>
        <p style="font-size:24px; margin:8px 0 0 0; line-height:1.3;">"I require a Spanish interpreter. I do not understand English well enough."</p>
    </div>
    """, unsafe_markdown=True)
    
    st.markdown("""
    <div class="rights-card card-green">
        <p style="font-size:14px; margin:0; text-transform:uppercase; opacity:0.8;">🟢 CONTACTAR UN TUTOR / ADULT SPONSOR</p>
        <p style="font-size:24px; margin:8px 0 0 0; line-height:1.3;">"Please allow me to call my adult sponsor immediately."</p>
    </div>
    """, unsafe_markdown=True)

# ==========================================
# TAB 3: TARJETA DE BOLSILLO (Backup Copy)
# ==========================================
with tab3:
    st.markdown("### 🖨️ Respaldo Físico Imprimible")
    st.write("Toma una captura de pantalla (screenshot) de este cuadro o usa el menú de tu navegador para imprimir esta página. Guarda el papel doblado en tu bolsillo por si te confiscan el celular:")
    
    st.markdown("""
    <div class="wallet-card-border">
        <p style="text-align:center; font-weight:bold; font-size:16px; margin-top:0; color:#0f172a;">AMIGO DE LA CORTE - TARJETA DE BOLSILLO</p>
        <hr style="border-top:2px solid #0f172a; margin:10px 0;">
        <p style="font-size:14px; font-weight:bold; margin-bottom:2px; color:#0f172a;">🏛️ COURT SCRIPT / SCRIPT PARA LA CORTE:</p>
        <p style="font-size:13px; font-style:italic; margin-top:0; color:#1e293b;">"Hello Your Honor. My name is a minor. I do not have a lawyer today, and I respectfully request a continuance so I can secure free legal representation."</p>
        <hr style="border-top:1px dashed #64748b; margin:10px 0;">
        <p style="font-size:14px; font-weight:bold; margin-bottom:2px; color:#0f172a;">🚨 FIELD ENCOUNTERS / PARA ENCUENTROS CON ICE:</p>
        <p style="font-size:13px; font-style:italic; margin-top:0; margin-bottom:4px; color:#1e293b;">1. "I am exercising my right to remain silent until I speak to a lawyer."</p>
        <p style="font-size:13px; font-style:italic; margin-top:0; margin-bottom:4px; color:#1e293b;">2. "I require a Spanish interpreter. I do not understand English well."</p>
        <p style="font-size:13px; font-style:italic; margin-top:0; color:#1e293b;">3. "Please allow me to call my adult sponsor immediately."</p>
    </div>
    """, unsafe_markdown=True)

# ==========================================
# TAB 4: RECURSOS (Houston Direct Dial Links)
# ==========================================
with tab4:
    st.markdown("### 🤝 Directorio de Ayuda Gratuita en Houston, TX")
    st.write("Presiona los botones inferiores para llamar directamente de forma gratuita:")
    
    st.markdown("#### ⚖️ KIND Houston")
    st.link_button("📞 Llamar a KIND (832-779-4340)", "tel:8327794340")
    st.caption("Especialistas en proveer abogados gratuitos para niños no acompañados frente a audiencias migratorias.")
    st.markdown("#### ✊ FIEL Houston")
    st.link_button("📞 Llamar a FIEL (713-364-3435)", "tel:7133643435")
    st.caption("Organización comunitaria liderada por jóvenes inmigrantes dedicada a la orientación familiar y defensa de derechos.")
    st.markdown("#### 🛡️ RAICES Texas")
    st.link_button("📞 Llamar a RAICES (210-222-0960)", "tel:2102220960")
    st.caption("Servicios legales gratuitos y de representación migratoria holística en todo el territorio de Texas.")


==========================================


FOOTER: PRIVACY PROFILE


==========================================

st.markdown("---")
st.caption("""
🔒 Perfil de Privacidad Absoluta / Data Privacy Shield:
Esta plataforma es estrictamente informativa. NO recopila direcciones IP, NO almacena cookies, NO guarda nombres ni envía datos a servidores externos. Todo el código se procesa localmente en la memoria del navegador de tu teléfono.
This app is an educational system and does not constitute formal legal advice. It tracks and stores ABSOLUTELY ZERO client metrics, ensuring safety for the community.
""")
