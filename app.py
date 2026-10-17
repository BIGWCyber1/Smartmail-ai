import streamlit as st

st.set_page_config(
    page_title="SmartMail AI",
    page_icon="📩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #07111f, #101d38);
    color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

h1, h2, h3, p, label {
    color: #f8fafc !important;
}

.hero {
    padding: 55px 15px 35px 15px;
    text-align: center;
}

.badge {
    display: inline-block;
    padding: 8px 15px;
    border-radius: 30px;
    background: #172c50;
    color: #93c5fd;
    border: 1px solid #31558b;
    font-size: 14px;
}

.hero-title {
    font-size: clamp(38px, 6vw, 66px);
    font-weight: 800;
    line-height: 1.1;
    margin-top: 25px;
}

.hero-text {
    color: #bdc9dc !important;
    font-size: 18px;
    line-height: 1.8;
    max-width: 650px;
    margin: 20px auto;
}

.feature {
    background: #111f37;
    border: 1px solid #263b5c;
    border-radius: 16px;
    padding: 24px;
    min-height: 170px;
    margin-bottom: 12px;
}

div.stButton > button {
    border-radius: 10px;
    min-height: 48px;
    font-weight: 700;
}

.footer {
    text-align: center;
    color: #94a3b8;
    padding: 30px 0;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# Navigation
left, right = st.columns([3, 1])

with left:
    st.markdown("## 📩 SmartMail AI")

with right:
    if st.button("Create Account", use_container_width=True):
        st.session_state["page"] = "signup"

if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Welcome page
if st.session_state["page"] == "home":

    st.markdown("""
    <div class="hero">
        <span class="badge">✦ A smarter way to manage email</span>
        <div class="hero-title">
            Take Control of<br>
            Your Inbox.
        </div>
        <p class="hero-text">
            Meet a smarter email experience. Organize what matters,
            find important messages faster, and make room for the
            things that deserve your attention.
        </p>
    </div>
    """, unsafe_allow_html=True)

    center1, center2, center3 = st.columns([1, 1, 1])

    with center2:
        if st.button(
            "🚀 Get Started",
            type="primary",
            use_container_width=True
        ):
            st.session_state["page"] = "signup"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("## Everything important, in one place")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="feature">
            <h3>🧠 Smart Organization</h3>
            <p>Explore a future where important emails are easier
            to find and organize.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature">
            <h3>⚡ Less Searching</h3>
            <p>Spend less time looking through messages and
            more time getting things done.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature">
            <h3>🔐 Privacy First</h3>
            <p>Security is part of our development plan from
            the beginning, not an afterthought.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div class="hero">
        <h2>Your inbox. Smarter. Simpler.</h2>
        <p class="hero-text">
            We're building a better way to experience email.
        </p>
    </div>
    """, unsafe_allow_html=True)

    center1, center2, center3 = st.columns([1, 1, 1])

    with center2:
        if st.button("Create Your Account", use_container_width=True):
            st.session_state["page"] = "signup"
            st.rerun()

# Sign-up interface
elif st.session_state["page"] == "signup":

    st.markdown("## 📝 Create your SmartMail AI account")
    st.write("Join us as we build a smarter email experience.")

    with st.form("signup_form"):
        full_name = st.text_input(
            "Full name",
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email address",
            placeholder="you@example.com"
        )

        st.info(
            "Account registration and email verification are not "
            "active yet. Do not enter a real password."
        )

        submitted = st.form_submit_button(
            "Continue",
            use_container_width=True
        )

        if submitted:
            if not full_name.strip():
                st.error("Please enter your name.")
            elif "@" not in email or "." not in email.split("@")[-1]:
                st.error("Please enter a valid email address.")
            else:
                st.success(
                    "The sign-up interface is working! Secure "
                    "registration and email verification will be "
                    "added in a later step."
                )

    if st.button("← Back to welcome page"):
        st.session_state["page"] = "home"
        st.rerun()

st.markdown("""
<div class="footer">
    SmartMail AI © 2026 · Your inbox. Smarter. Simpler.<br>
    Demo interface — secure registration and email delivery
    are not yet enabled.
</div>
""", unsafe_allow_html=True)
