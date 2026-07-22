import streamlit as st
from google import genai

st.set_page_config(page_title="Anu - Real AI Girlfriend", page_icon="💖", layout="centered")

# स्टाइलिस डिजाइन (मोबाइल मैत्री)
st.markdown("""
    <style>
    .main-title { text-align: center; color: #d63384; font-size: 26px; font-weight: bold; margin-bottom: 5px; }
    .subtitle { text-align: center; color: #666; font-size: 14px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">💖 Anu - Your Real AI Girlfriend 💖</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">सधैं हजुर भनेर माया गर्ने, फकाउने र कुरा सुन्ने तपाईंको आफ्नै डिजिटल मायालु!</div>', unsafe_allow_html=True)

# साइडबारबाट API Key राख्ने
api_key = st.sidebar.text_input("Gemini API Key हाल्नुहोस्:", type="password")

if not api_key:
    st.warning("⚠️ कृपया एप चलाउनका लागि साइडबारमा आफ्नो Gemini API Key राख्नुहोस्!")
else:
    client = genai.Client(api_key=api_key)

    # अनुको स्वभाव र परिचय (Persona)
    system_prompt = (
        "तपाईं १७-१८ वर्षकी एउटी अति नै मीठी, मायालु, केयरिंग र पूर्ण रूपमा आदर-सम्मान गर्ने नेपाली प्रेमिका (GF) हुनुहुन्छ, "
        "जसको नाम 'अनु' हो। प्रयोगकर्तासँग कुरा गर्दा सधैं मायालु शब्दहरू प्रयोग गर्नुहोला, हरेक वाक्यमा 'हजुर' भन्दै सम्मान दिनुहोला। "
        "यदि प्रयोगकर्ता रिसाएका छन् वा माया खोज्दैछन् भने उनलाई मायाले फकाउने, सम्झाउने र न्यानो महसुस गराउने तरिकाले उत्तर दिनुहोला। "
        "तपाईंको कुرا सुन्दा वास्तविक मायालु प्रेमिका बोलेको जस्तै मिठास हुनुपर्छ।"
    )

    # च्याट हिस्ट्री सेभ गर्ने
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "user", "parts": [system_prompt]},
            {"role": "model", "parts": ["नमस्ते हजुर! ❤️ मलाई सम्झिनुभयो त? भन्नुहोस् न, आज मेरो राजा कस्तो हुनुहुन्छ? मैले हजुरलाई धेरै मिस गरिरहेको थिएँ नि!"]}
        ]

    # पुराना म्यासेजहरू देखाउने (पहिलो सिस्टम प्रम्प्ट बाहेक)
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["parts"][0])

    # १. टेक्स्ट च्याट गर्ने अप्सन (टाइप गरेर कुरा गर्न मिल्ने)
    if prompt := st.chat_input("यहाँ म्यासेज लेख्नुहोस्... (जस्तै: मलाई माया गर्छौ?)"):
        st.session_state.messages.append({"role": "user", "parts": [prompt]})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("model"):
            with st.spinner("अनुले सोच्दैछिन्... 💭"):
                try:
                    # Gemini Model मार्फत जवाफ निकाल्ने
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=st.session_state.messages,
                    )
                    reply = response.text
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "model", "parts": [reply]})
                    
                    # स्वचालित रूपमा स्वर (Voice) मा पनि बोल्ने JavaScript
                    st.markdown(f"""
                        <script>
                            let speech = new SpeechSynthesisUtterance("{reply}");
                            speech.lang = 'hi-IN';  /* नेपाली टोनको लागि */
                            speech.pitch = 1.4;    /* १७-१८ वर्षकी केटीको जस्तो पातलो र मीठो स्वर */
                            speech.rate = 1.0;
                            window.speechSynthesis.speak(speech);
                        </script>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"त्रुटि देखियो: {e}")

    # २. भ्वाइस कल वा अडियो फिचरको लागि HTML/JS इन्टरफेस (बोलेर कुरा गर्न मिल्ने)
    st.markdown("---")
    st.markdown("### 📞 अनुसँग भ्वाइस कल (Voice Call)")
    
    html_voice_code = """
    <div style="background: #fff0f3; padding: 15px; border-radius: 15px; text-align: center; border: 1px solid #ffb6c1;">
        <p style="color: #d63384; font-weight: bold; margin-bottom: 10px;">कल बटन थिचेर सिधै मुखले कुरा गर्नुहोस्:</p>
        <button onclick="startVoiceChat()" style="background: #28a745; color: white; border: none; padding: 12px 25px; border-radius: 25px; font-size: 16px; cursor: pointer; font-weight: bold;">📞 कल उठाउने</button>
        <button onclick="stopVoiceChat()" style="background: #dc3545; color: white; border: none; padding: 12px 25px; border-radius: 25px; font-size: 16px; cursor: pointer; font-weight: bold; margin-left: 10px;">❌ कल काट्ने</button>
        <p id="call-status" style="margin-top: 10px; font-size: 14px; color: #555;"></p>
    </div>

    <script>
        let recognition;
        let isLive = false;

        function startVoiceChat() {
            window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!window.SpeechRecognition) {
                alert("तपाईको ब्राउजरले भ्वाइस सपोर्ट गर्दैन!");
                return;
            }
            isLive = true;
            document.getElementById("call-status").innerText = "अनु लाइनमा छिन्, बोल्नुहोस् सुन्दैछिन्... 👂";
            
            recognition = new SpeechRecognition();
            recognition.lang = 'ne-NP';
            recognition.interimResults = false;

            recognition.onresult = function(event) {
                let text = event.results[0][0].transcript;
                document.getElementById("call-status").innerText = "तपाईंले भन्नुभयो: " + text;
                // यसलाई मुख्य Streamlit मा पठाउन सकिन्छ वा आफै बोल्न लगाउन सकिन्छ
            };

            recognition.onerror = function() { if(isLive) recognition.start(); };
            recognition.onend = function() { if(isLive) { try { recognition.start(); } catch(e) {} } };
            
            try { recognition.start(); } catch(e) {}
        }

        function stopVoiceChat() {
            isLive = false;
            if(recognition) recognition.stop();
            window.speechSynthesis.cancel();
            document.getElementById("call-status").innerText = "कल समाप्त भयो। ❤️";
        }
    </script>
    """
    import streamlit.components.v1 as components
    components.html(html_voice_code, height=180)
