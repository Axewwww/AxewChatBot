
import streamlit as st
import time
from google import genai
from supabase import create_client

st.set_page_config(
    page_title="Axew AI",
    page_icon="🤖",
    layout="centered"
)
st.markdown("""
<style>

/* Axew mascot animation */
@keyframes axew-float {
    0%, 100% {
        transform: translateY(0);
        filter: drop-shadow(0 0 8px rgba(0, 210, 255, 0.25));
    }
    50% {
        transform: translateY(-8px);
        filter: drop-shadow(0 0 18px rgba(0, 210, 255, 0.65));
    }
}

/* Normal, relaxed Axew */
.axew-mascot {
    display: inline-block;
    animation: axew-float 3s ease-in-out infinite;
    transform-origin: center;
    transition: filter 0.3s ease;
}

/* Axew is thinking */
.axew-mascot.axew-thinking {
    animation: axew-float 0.8s ease-in-out infinite;
    filter: drop-shadow(0 0 16px rgba(0, 210, 255, 0.9));
}

/* Axew is replying */
.axew-mascot.axew-replying {
    animation: axew-float 1.4s ease-in-out infinite;
    filter: drop-shadow(0 0 22px rgba(0, 210, 255, 0.9));
}

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0b0b14 0%, #121225 55%, #171329 100%);
    color: #f4f4ff;
}

/* Hide Streamlit's default header decoration */
[data-testid="stHeader"] {
    background: transparent;
}

/* Main content width and spacing */
.block-container {
    max-width: 1000px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* Main title */
h1 {
    color: #ffffff !important;
    font-size: 2.7rem !important;
    font-weight: 800 !important;
    letter-spacing: -1.5px;
}

/* Subtitle and regular text */
.stApp p {
    color: #c5c5d9;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #151522;
    border-right: 1px solid #292940;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff;
}

/* Buttons */
.stButton > button {
    border: 1px solid #393455;
    border-radius: 12px;
    background: #242239;
    color: #f5f3ff;
    padding: 0.65rem 1rem;
    transition: all 0.2s ease;
}
.stButton > button {
    box-shadow: 0 0 0 rgba(112, 72, 232, 0);
    font-weight: 600;
}

.stButton > button:hover {
    box-shadow: 0 0 18px rgba(112, 72, 232, 0.28);
    transform: translateY(-1px);
}

.stButton > button:active {
    transform: translateY(0);
}
.stButton > button:hover {
    background: #7048e8;
    border-color: #a78bfa;
    color: white;
}

/* Premium AI Gradient chat bubbles */
[data-testid="stChatMessage"] {
    background: #18243A !important;
    border: 1px solid #344763 !important;
    border-radius: 16px;
    padding: 0.85rem 1rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 2px 10px rgba(12, 18, 35, 0.12);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

/* Axew's messages — blue/cyan */
[data-testid="stChatMessage"]:has(img[src*="axew.png"]) {
    background: linear-gradient(135deg, #102D43, #18364A) !important;
    border-color: rgba(0, 210, 255, 0.7) !important;
}

/* Your messages — violet */
[data-testid="stChatMessage"]:has(img[alt="🧑"]),
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #29213F, #38294F) !important;
    border-color: rgba(155, 105, 255, 0.75) !important;
}

/* Gentle glow on hover */
[data-testid="stChatMessage"]:hover {
    box-shadow: 0 3px 14px rgba(69, 107, 159, 0.16);
}

/* Chat input */
[data-testid="stChatInput"] {
    border: 1px solid #6550a8;
    border-radius: 16px;
    background: #1c1b2b;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="stChatInput"]:hover {
    border-color: #8b5cf6;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #a78bfa;
    box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.16);
}
[data-testid="stChatInput"] button,
[data-testid="stChatInput"] button[kind="primary"] {
    background: #7048e8 !important;
    color: #ffffff !important;
    border: 1px solid #8b5cf6 !important;
    border-radius: 10px !important;
    transition: background 0.2s ease, box-shadow 0.2s ease !important;
}

[data-testid="stChatInput"] button:hover,
[data-testid="stChatInput"] button[kind="primary"]:hover {
    background: #06b6d4 !important;
    color: #ffffff !important;
    border-color: #67e8f9 !important;
    box-shadow: 0 0 14px rgba(6, 182, 212, 0.4) !important;
}
/* Text fields */
.stTextInput input,
.stTextInput input:focus {
    background: #1c1b2b;
    color: #ffffff;
    border: 1px solid #393455;
    border-radius: 10px;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: #c5c5d9;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #c4b5fd;
    border-bottom-color: #8b5cf6;
}

/* Dividers */
hr {
    border-color: #302d45;
}

/* Links */
a {
    color: #b9a5ff !important;
}

/* Mobile-friendly title */
@media (max-width: 640px) {
    h1 {
        font-size: 2rem !important;
    }

    .block-container {
        padding: 1.2rem 1rem 2rem;
    }
}

/* Axew's glowing thinking effect */
@keyframes axew-thinking-glow {
    0%, 100% {
        filter: drop-shadow(0 0 4px #00d9ff);
        transform: translateY(0) scale(1);
    }
    50% {
        filter: drop-shadow(0 0 18px #00d9ff);
        transform: translateY(-5px) scale(1.04);
    }
}

.axew-thinking {
    animation: axew-thinking-glow 1.2s ease-in-out infinite;
    transform-origin: center;
}
.axew-mascot.axew-replying {
    animation: axew-thinking-glow 0.6s ease-in-out infinite alternate;
    transform-origin: center;
}

@keyframes axew-replying-glow {
    from {
        filter: drop-shadow(0 0 4px #00d9ff);
        transform: translateY(0) scale(1);
    }
    to {
        filter: drop-shadow(0 0 18px #00d9ff);
        transform: translateY(-5px) scale(1.04);
    }
}
.axew-mascot img {
    animation: axew-thinking-glow 1.2s ease-in-out infinite;
    filter: drop-shadow(0 0 8px #00d9ff);
    transition: filter 0.3s ease;
}
</style>
""", unsafe_allow_html=True)

# Axew's current visual mood
axew_mood = "axew-idle"
# Axew AI welcome header
header_left, header_right = st.columns([1, 4])

import base64
from pathlib import Path

with header_left:
    image_path = Path("assets/axew.png")
    image_data = base64.b64encode(
        image_path.read_bytes()
    ).decode("utf-8")

    st.markdown(
        f"""
        <div class="axew-mascot {axew_mood}" style="display:inline-block;">
            <img
                src="data:image/png;base64,{image_data}"
                width="125" style="display:block;"
                alt="Axew robot"
            />
        </div>
        """,
        unsafe_allow_html=True
    )


with header_right:
    st.markdown(
        """
        <div style="padding-top: 18px;">
            <h1 style="margin-bottom: 4px;">
                Axew <span style="color:#19cfff;">AI</span>
            </h1>
            <p style="color:#aab8d8; margin-top:0;">
                Your personal AI best friend 💙
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Connect to Gemini
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# Connect to Supabase
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

SYSTEM_PROMPT = """
You are Axew, a friendly male AI best friend.
Speak naturally, warmly, and casually.
Be supportive, helpful, and honest.
Use simple language and occasional emojis.
Remember the conversation context provided to you.
"""


def get_user_supabase():
    """Create a database client authenticated as the logged-in user."""
    token = st.session_state.get("access_token")

    if not token:
        raise Exception("Your session expired. Please log in again.")

    db = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

    db.postgrest.auth(token)
    return db


def load_messages(db, conversation_id):
    result = (
        db.table("messages")
        .select("role, content")
        .eq("conversation_id", conversation_id)
        .order("created_at")
        .execute()
    )
    return result.data or []


def save_message(db, conversation_id, user_id, role, content):
    db.table("messages").insert({
        "conversation_id": conversation_id,
        "user_id": user_id,
        "role": role,
        "content": content
    }).execute()


def load_conversations(db, user_id):
    result = (
        db.table("conversations")
        .select("id, title, created_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return result.data or []


# Session state
if "user" not in st.session_state:
    st.session_state.user = None

if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = None

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- AUTHENTICATION ----------------

if st.session_state.user is None:
    login_tab, signup_tab = st.tabs(
        ["Log in", "Create account"]
    )

    with login_tab:
        st.subheader("Welcome back")

        login_email = st.text_input(
            "Email",
            key="login_email"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Log in", use_container_width=True):
            try:
                result = supabase.auth.sign_in_with_password({
                    "email": login_email,
                    "password": login_password
                })

                if not result.user or not result.session:
                    st.error("Login failed. Please try again.")
                else:
                    st.session_state.user = result.user
                    st.session_state.access_token = (
                        result.session.access_token
                    )
                    st.session_state.refresh_token = (
                        result.session.refresh_token
                    )
                    st.session_state.messages = []
                    st.session_state.conversation_id = None
                    st.rerun()

            except Exception as e:
                st.error(f"Login failed: {e}")

    with signup_tab:
        st.subheader("Create your Axew account")

        signup_email = st.text_input(
            "Email",
            key="signup_email"
        )

        signup_password = st.text_input(
            "Create password",
            type="password",
            key="signup_password"
        )

        if st.button("Create account", use_container_width=True):
            if len(signup_password) < 6:
                st.warning(
                    "Please use a password with at least 6 characters."
                )
            else:
                try:
                    result = supabase.auth.sign_up({
                        "email": signup_email,
                        "password": signup_password
                    })

                    if result.user and result.session:
                        st.session_state.user = result.user
                        st.session_state.access_token = (
                            result.session.access_token
                        )
                        st.session_state.refresh_token = (
                            result.session.refresh_token
                        )
                        st.session_state.messages = []
                        st.session_state.conversation_id = None
                        st.success("Account created!")
                        st.rerun()
                    else:
                        st.success(
                            "Account created! Check your email to confirm "
                            "it, then log in."
                        )

                except Exception as e:
                    st.error(f"Account creation failed: {e}")


# ---------------- CHAT APPLICATION ----------------

else:
    user = st.session_state.user
    user_id = str(user.id)

    try:
        db = get_user_supabase()
    except Exception as e:
        st.error(str(e))
        st.stop()

    with st.sidebar:
        st.write(f"Signed in as {user.email}")

        if st.button("➕ New chat", use_container_width=True):
            st.session_state.conversation_id = None
            st.session_state.messages = []
            st.rerun()

        st.divider()
        st.subheader("Your previous chats")

        try:
            chats = load_conversations(db, user_id)

            for chat in chats:
                title = chat.get("title") or "New chat"

                if st.button(
                    title[:45],
                    key=f"chat_{chat['id']}",
                    use_container_width=True
                ):
                    st.session_state.conversation_id = chat["id"]
                    st.session_state.messages = load_messages(
                        db, chat["id"]
                    )
                    st.rerun()

        except Exception as e:
            st.error(f"Could not load chats: {e}")

        st.divider()

        if st.button("Log out", use_container_width=True):
            try:
                supabase.auth.sign_out()
            except Exception:
                pass

            st.session_state.user = None
            st.session_state.access_token = None
            st.session_state.refresh_token = None
            st.session_state.conversation_id = None
            st.session_state.messages = []
            st.rerun()

   
    # Show chat history
    for message in st.session_state.messages:
        with st.chat_message(
            message["role"],
            avatar=(
                "assets/axew.png"
                if message["role"] == "assistant"
                else "🧑"
            )
        ):
            st.markdown(message["content"])

    # User input
    prompt = st.chat_input("Message Axew...")

    if prompt:
        try:
            # Create conversation if this is a new chat
            if st.session_state.conversation_id is None:
                created = (
                    db.table("conversations")
                    .insert({
                        "user_id": user_id,
                        "title": prompt[:60]
                    })
                    .execute()
                )

                if not created.data:
                    raise Exception(
                        "Could not create a new conversation."
                    )

                st.session_state.conversation_id = (
                    created.data[0]["id"]
                )

            conversation_id = st.session_state.conversation_id

            # Save user message
            save_message(
                db, conversation_id, user_id, "user", prompt
            )

            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })

            with st.chat_message("user", avatar="🧑"):
                st.markdown(prompt)

            # Send the current conversation to Gemini
            history = [
                {
                    "role": "user",
                    "parts": [{"text": SYSTEM_PROMPT}]
                },
                {
                    "role": "model",
                    "parts": [{"text": "Understood. I am Axew."}]
                }
            ]

            for msg in st.session_state.messages:
                history.append({
                    "role": (
                        "user" if msg["role"] == "user"
                        else "model"
                    ),
                    "parts": [{"text": msg["content"]}]
                })



        
            with st.chat_message("assistant", avatar="assets/axew.png"):
                axew_mood = "axew-thinking"

                with st.spinner("Axew is thinking... 💭"):
                    reply = None
                    last_error = None

                    for attempt in range(3):
                        try:
                            response = client.models.generate_content(
                                model="gemini-3.5-flash",
                                contents=history
                            )
                            reply = response.text

                            if reply:
                                break

                            last_error = "Empty response from Gemini."

                        except Exception as e:
                            last_error = str(e)
                            error_text = last_error.lower()

                            retryable = any(term in error_text for term in [
                                "503", "unavailable", "429",
                                "resource_exhausted", "500", "timeout"
                            ])

                            if not retryable or attempt == 2:
                                break

                        if attempt < 2:
                            time.sleep(1)

                    if not reply:
                        reply = (
                            "Bro, Google's AI service is busy right now 😅 "
                            "Please try sending your message again shortly."
                        )

                    axew_mood = "axew-replying"
                    st.markdown(reply)
    

            # Save assistant response
            save_message(
                db, conversation_id, user_id, "assistant", reply
            )

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })


        except Exception as e:
            st.error(f"Something went wrong: {e}")
