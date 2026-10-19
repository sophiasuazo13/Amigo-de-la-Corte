import streamlit as st

# Set up mobile-responsive page configuration
st.set_page_config(
    page_title="Amigo de la Corte",
    page_icon="🏛️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS styling to make elements larger and highly accessible on mobile screens
st.markdown("""
    <style>
    /* Make headers and text larger for readability under stress */
    .big-font { font-size:24px !important; font-weight: bold; }
    .emergency-box {
        background-color: #FF4B4B;
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .rights-card-red {
        background-color: #D32F2F;
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .rights-card-blue {
        background-color: #1976D2;
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .rights-card-green {
        background-color: #388E3C;
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .wallet-card-border {
        border: 3px dashed #000000;
        padding: 20px;
        background-color: #FFFFFF;
        color: #000000;
        border-radius: 5px;
    }
    </style>
    """, unsafe_markdown=True)

# Main Application Title
st.title("🏛️ Amigo de la Corte")
st.subheader("Guía de derechos y preparación legal para menores de edad")

# Setup Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏛️ Mi Corte", "📣 Habla Por Mí", "🖨️ Tarjeta", "🤝 Recursos"])

# ==========================================
# TAB 1: MI CORTE (Courtroom Walkthrough)
# ==========================================
with tab1:
    st.markdown("### 🏛️ ¿Quién es quién en la Corte?")
    st.write("Toca cada sección para entender el papel de cada persona en la sala del tribunal:")
    
    with st.expander("⚖️ El Juez (The Judge)"):
        st.write("**Español:** Es la persona que toma las decisiones sobre tu caso. Debes hablarle con respeto y llamarle 'Su Señoría' o 'Your Honor'.")
        st.write("**English:** The person who makes decisions about your case. Speak respectfully and address them as 'Your Honor'.")
        
    with st.expander("💼 El Fiscal / Abogado del Gobierno (The Government Prosecutor)"):
        st.write("**Español:** Es el abogado que representa al gobierno de EE.UU. Su trabajo es argumentar las leyes de inmigración. No es tu abogado personal y no debes tener miedo de mantener tu derecho a buscar defensa.")
        st.write("**English:** The attorney representing the US government. They argue immigration law. They are not your personal lawyer.")
        
    with st.expander("🗣️ El Intérprete (The Interpreter)"):
        st.write("**Español:** Es tu puente de comunicación. Traduce todo lo que dices al inglés, y todo lo que dice el juez al español. Si no entiendes al intérprete, díselo al juez inmediatamente.")
        st.write("**English:** Your communication bridge. Translates your words to English, and the judge's words to Spanish. If you don't understand them, tell the judge.")

    st.markdown("---")
    st.markdown("### 🚨 Frase de Emergencia para el Juez")
    st.write("Si no tienes un abogado el día de tu audiencia, muestra esta pantalla o lee esta frase en voz alta inmediatamente cuando el juez te hable:")
    
    st.markdown("""
    <div class="emergency-box">
        <p style="font-size:20px; font-weight:bold; margin-bottom:5px;">🇺🇸 READ THIS TO THE JUDGE / LEE ESTO AL JUEZ:</p>
        <p style="font-size:22px; font-weight:bold; line-height:1.4;">
        "Hello Your Honor. My name is [Your Name]. I am a minor, I do not have a lawyer today, and I respectfully request a continuance so I can secure free legal representation."
        </p>
    </div>
    """, unsafe_markdown=True)
    
    st.markdown("**Significado en Español:** *'Hola Su Señoría. Mi nombre es [Tu Nombre]. Soy menor de edad, no tengo un abogado hoy, y solicito respetuosamente un aplazamiento para poder conseguir representación legal gratuita.'*")

# ==========================================
# TAB 2: HABLA POR MÍ (Field Rights Flashcards)
# ==========================================
with tab2:
    st.markdown("### 📣 Tarjetas de Derechos Visuales")
    st.write("Si te encuentras con oficiales de ICE o de inmigración, puedes mostrar estas tarjetas directamente en la pantalla de tu teléfono:")
    
    st.markdown("""
    <div class="rights-card-red">
        <p style="font-size:16px; margin:0; text-transform:uppercase;">🔴 Muestra esto para guardar silencio:</p>
        <p style="font-size:24px; margin:5px 0 0 0;">"I am exercising my right to remain silent until I speak to a lawyer."</p>
    </div>
    """, unsafe_markdown=True)
    
    st.markdown("""
    <div class="rights-card-blue">
        <p style="font-size:16px; margin:0; text-transform:uppercase;">🔵 Muestra esto si necesitas traducción:</p>
        <p style="font-size:24px; margin:5px 0 0 0;">"I require a Spanish interpreter. I do not understand English well enough."</p>
    </div>
    """, unsafe_markdown=True)
    
    st.markdown("""
    <div class="rights-card-green">
        <p style="font-size:16px; margin:0; text-transform:uppercase;">🟢 Muestra esto para llamar a tu tutor:</p>
        <p style="font-size:24px; margin:5px 0 0 0;">"Please allow me to call my adult sponsor immediately."</p>
    </div>
    """, unsafe_markdown=True)

# ==========================================
# TAB 3: TARJETA DE BOLSILLO (Printable Card)
# ==========================================
with tab3:
    st.markdown("### 🖨️ Tu Tarjeta Física de Respaldo")
    st.write("Toma una captura de pantalla (screenshot) de este cuadro o imprime esta sección. Si los oficiales te quitan el teléfono, mantén este papel guardado en tu bolsillo:")
    
    st.markdown("""
    <div class="wallet-card-border">
        <p style="text-align:center; font-weight:bold; font-size:18px; margin-top:0;">AMIGO DE LA CORTE - TARGETA DE DERECHOS</p>
        <hr style="border-top:1px solid black; margin:10px 0;">
        <p style="font-size:15px; font-weight:bold; margin-bottom:2px;">🏛️ FOR THE JUDGE / PARA EL JUEZ:</p>
        <p style="font-size:14px; font-style:italic; margin-top:0;">"Hello Your Honor. My name is a minor. I do not have a lawyer today, and I respectfully request a continuance so I can secure free legal representation."</p>
        <hr style="border-top:1px dashed gray; margin:10px 0;">
        <p style="font-size:15px; font-weight:bold; margin-bottom:2px;">🚨 FOR ICE / PARA ENCUENTROS CON ICE:</p>
        <p style="font-size:14px; font-style:italic; margin-top:0; margin-bottom:4px;">1. "I am exercising my right to remain silent until I speak to a lawyer."</p>
        <p style="font-size:14px; font-style:italic; margin-top:0; margin-bottom:4px;">2. "I require a Spanish interpreter. I do not understand English well."</p>
        <p style="font-size:14px; font-style:italic; margin-top:0;">3. "Please allow me to call my adult sponsor immediately."</p>
    </div>
    """, unsafe_markdown=True)

# ==========================================
# TAB 4: RECURSOS (Houston Directory Links)
# ==========================================
with tab4:
    st.markdown("### 🤝 Ayuda Legal Gratuita en Houston")
    st.write("Toca los botones para llamar directamente desde tu teléfono celular:")
    
    st.markdown("#### ⚖️ Defensa Legal de Menores")
    st.link_button("📞 Llamar a KIND Houston (832-779-4340)", "tel:8327794340")
    st.write("*Organización especializada en la representación gratuita de niños no acompañados ante la corte.*")
    
    st.markdown("#### ✊ Apoyo Comunitario y Juvenil")
    st.link_button("📞 Llamar a FIEL Houston (713-364-3435)", "tel:7133643435")
    st.write("*Movimiento liderado por jóvenes inmigrantes enfocado en la organización, orientación y recursos familiares.*")
    
    st.markdown("#### 🛡️ Servicios Integrales de Inmigración")
    st.link_button("📞 Llamar a RAICES Texas (210-222-0960)", "tel:2102220960")
    st.write("*Defensa legal gratuita y de bajo costo para niños, familias y refugiados en todo el estado de Texas.*")

# ==========================================
# FOOTER: PRIVACY & LEGAL DISCLAIMER
# ==========================================
st.markdown("---")
st.caption("""
🔒 **Seguridad y Privacidad Absoluta / Data Privacy Profile:** 
Esta aplicación es una herramienta puramente informativa y educativa. NO recopila, NO almacena y NO transmite ningún tipo de información personal, cookies, nombres ni ubicaciones de los usuarios. Todo lo que ves se ejecuta de forma totalmente privada dentro de la memoria de tu teléfono.

This application is an educational tool and does not constitute formal legal advice. It collects ABSOLUTELY ZERO user data, names, or server-side logs to protect vulnerable communities.
""")
