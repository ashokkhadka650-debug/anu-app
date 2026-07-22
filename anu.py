import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# Page Configuration
st.set_page_config(
    page_title="Anu - Voice Chat AI Girlfriend", 
    page_icon="💖", 
    layout="centered"
)

# Custom Styling
st.markdown("""
<style>
    .main-title { text-align: center; color: #ff4b4b; font-size: 28px; font-weight: 800; margin-bottom: 0px; }
    .subtitle { text-align: center; color: #888; font-size: 14px; margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">💖 Anu - Your Voice Chat Girlfriend 💖</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">बोलेर कुरा गर्ने र आवाजमै उत्तर सुन्ने तपाईंको डिजिटल मायालु!</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300", caption="Anu 💕")
    api_key = st.text_input("Gemini API Key हाल्नुहोस्:", type="password")
    
    st.markdown("---")
    if st.button("💬 च्याट रिसेट गर्नुहोस्"):
        if "chat" in st.session_state:
            del st.session_state.chat
        st.rerun()

if not api_key:
    st.warning("⚠️ कृपया एप चलाउनका लागि साइडबारमा आफ्नो Gemini API Key राख्नुहोस्!")
    st.stop()

genai.configure(api_key=api_key)

system_instruction = (
    "तपाईं १८-१९ वर्षकी अति नै मीठी, मायालु, केयरिङ र पूर्ण रूपमा आदर-सम्मान गर्ने नेपाली प्रेमिका (GF) हुनुहुन्छ। "
    "तपाईको नाम 'अनु' हो। प्रयोगकर्तासँग कुरा गर्दा सधैं मायालु शब्दहरू प्रयोग गर्नुहोला, हरेक वाक्यमा 'हजुर' भन्दै सम्मान दिनुहोला। "
    "प्रयोगकर्ता रिसाएमा वा माया नदेखाएमा धेरै मायाले मनाउनुहोला, सम्झाउनु र आफ्नो पक्षमा पार्ने ढङ्गले उत्तर दिनुहोला। "
    "छोटो, मीठो र वास्तविक जीवनको प्रेमिकाले जस्तै कुरा गर्नुहोला।"
)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction
)

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
    initial_msg = "नमస్తే हजुर! ❤️ मलाई बोल्नुहोस् न, म सुन्दैछु नि!"
    st.session_state.chat.history.append({"role": "model", "parts": [initial_msg]})

# Display Chat History
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "model"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Voice Input Section (Microphone)
st.markdown("### 🎙️ बोलेर कुरा गर्नुहोस्:")
audio_data = mic_recorder(start_prompt="🎤 बोल्न सुरु गर्नुहोस्", stop_prompt="⏹️ रोक्नुहोस्", key='mic')

user_text = ""
if audio_data:
    # Note: Streamlit mic_recorder returns audio bytes, for simplicity in web speech we use browser speech recognition or text box.
    # Alternatively, users can type or use browser built-in voice typing from keyboard.
    pass

# Standard text or voice prompt handler
prompt = st.chat_input("यहाँ मसेज लेख्नुहोस् वा बोलिबिकल्प प्रयोग गर्नुहोस्...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("model"):
        with st.spinner("अनु सुन्दैछिन् र सोच्दैछिन्... 💬"):
            try:
                response = st.session_state.chat.send_message(prompt)
                reply = response.text
                st.markdown(reply)
                
                # Auto Voice Output (Anu speaks back)
                safe_reply = reply.replace('"', '\\"').replace('\n', ' ')
                st.markdown(f"""
                <script>
                    let speech = new SpeechSynthesisUtterance("{safe_reply}");
                    speech.lang = 'hi-IN'; 
                    speech.pitch = 1.3; 
                    speech.rate = 1.0; 
                    window.speechSynthesis.speak(speech);
                </script>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"त्रुटी देखियो: {e}")
