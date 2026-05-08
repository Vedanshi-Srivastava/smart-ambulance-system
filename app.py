import streamlit as st

# Optional speech recognition
try:
    import speech_recognition as sr
    voice_enabled = True
except:
    voice_enabled = False

from triage import classify_severity
from dispatch import assign_ambulance, suggest_hospital

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Smart Ambulance System", page_icon="🚑", layout="wide")

# -------------------- CUSTOM UI --------------------
st.markdown("""
<style>

/* Full app background */
[data-testid="stAppViewContainer"] {
    background: 
        linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.75)),
        url("https://images.unsplash.com/photo-1576765608535-5f04d1e3f289");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Remove default background */
[data-testid="stHeader"], [data-testid="stToolbar"] {
    background: transparent;
}

/* Text color fix */
h1, h2, h3, h4, h5, h6, p, label {
    color: white !important;
}

/* Card styling */
.card {
    background: rgba(255, 255, 255, 0.08);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}

/* Button styling */
.stButton>button {
    background: linear-gradient(to right, #ff416c, #ff4b2b);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.title("🚑 Smart AI Ambulance System")
st.write("AI-powered emergency response with voice support")

# 🎤 Voice Input Function
def get_voice_input():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening... Speak now")
            audio = recognizer.listen(source)

        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        return "❌ Could not understand audio"
    except sr.RequestError:
        return "❌ Speech service not available"
    except:
        return "❌ Microphone error"


st.subheader("📝 Enter Emergency Details")

text_input = st.text_area("Type Emergency")

# ---------------- VOICE INPUT ----------------

if voice_enabled:

    st.markdown("### 🎤 Voice Input (Optional)")

    audio_file = st.file_uploader(
        "Upload your recording",
        type=["wav"]
    )

    if audio_file is not None:

        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        try:
            text_input = recognizer.recognize_google(audio)
            st.success(f"You said: {text_input}")

        except:
            st.error("❌ Could not understand audio")

else:
    st.info("🎤 Voice recognition unavailable in cloud deployment")

analyze = st.button("🚀 Analyze")

# 🔍 Processing
if analyze and text_input:
    severity = classify_severity(text_input)
    ambulance = assign_ambulance(severity)
    hospital = suggest_hospital(severity)

    st.subheader("🚨 Emergency Analysis")

    # Severity Display
    if severity.startswith("🔴"):
        st.error(f"Severity Level: {severity}")
    elif severity.startswith("🟠"):
        st.warning(f"Severity Level: {severity}")
    else:
        st.info(f"Severity Level: {severity}")

    # 🚑 Ambulance Section
    st.subheader("🚑 Assigned Ambulance")

    if isinstance(ambulance, dict):
        st.write(f"**Type:** {ambulance['type']}")
        st.write(f"**Location:** {ambulance['location']}")
        st.write(f"**ETA:** {ambulance['eta_minutes']} minutes")

        # Explanation
        if severity.startswith("🔴"):
            st.caption("Chosen: ALS ambulance for critical condition")
        elif severity.startswith("🟠"):
            st.caption("Chosen: Preferred ALS for urgent case")
        else:
            st.caption("Chosen: Fastest available ambulance")

    else:
        st.error(ambulance)

    # 🏥 Hospital Section
    st.subheader("🏥 Recommended Hospital")

    if isinstance(hospital, dict):
        st.write(f"**Name:** {hospital['name']}")
        st.write(f"**Specialization:** {hospital['specialization']}")
        st.write(f"**Available Beds:** {hospital['available_beds']}")

        # Explanation
        if severity.startswith("🔴"):
            st.caption("Selected: Trauma/Emergency hospital for critical case")
        else:
            st.caption("Selected: Best available hospital with capacity")

    else:
        st.error(hospital)

elif analyze:
    st.warning("⚠️ Please enter or speak emergency details")