import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="SmartMail AI",
    page_icon="📩",
    layout="wide",
)

APP_URL = "https://smartmail-ai-bigwcyber1.streamlit.app/"


@st.cache_resource
def get_supabase():
    url = st.secrets.get("SUPABASE_URL", "")
    key = st.secrets.get("SUPABASE_KEY", "")

    if not url or not key:
        return None

    return create_client(url, key)


try:
    supabase = get_supabase()
except Exception:
    supabase = None


if "page" not in st.session_state:
    st.session_state.page = "home"

if "user" not in st.session_state:
    st.session_state.user = None


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
    padding: 45px 15px 30px;
    text-align: center;
}

.badge {
    display: inline-block;
    padding: 8px 15px;
    border-radius: 30px;
    background: #172c50;
    color: #93c5fd;
    border: 1px solid #31558b;
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
    min-height: 160px;
    margin-bottom: 12px;
}

div.stButton > button,
div.stFormSubmitButton > button {
    border-radius: 10px;
    min-height: 44px;
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


def go(page):
    st.session_state.page = page
    st.rerun()


def show_config_warning():
    if supabase is None:
        st.error(
            "Authentication is not configured. "
            "Check SUPABASE_URL and SUPABASE_KEY "
            "in Streamlit Cloud → Settings → Secrets."
        )
        return True

    return False


def auth_error_message(exc):
    message = str(exc).lower()

    if "email not confirmed" in message:
        return "Verify your email before logging in."

    if "already registered" in message:
        return "An account may already exist. Try logging in."

    if "invalid login credentials" in message:
        return "Incorrect email or password."

    return "We couldn't complete that request. Check your details and try again."


# TOP NAVIGATION
left, middle, right = st.columns([3, 1, 1])

with left:
    st.markdown("## 📩 SmartMail AI")

with middle:
    if st.button("Log in", use_container_width=True):
        go("login")

with right:
    if st.button("Sign up", use_container_width=True):
        go("signup")


st.markdown("---")
# HOMEPAGE
if st.session_state.user is None and st.session_state.page == "home":

    st.markdown("""
    <div class="hero">
        <span class="badge">✦ A smarter way to manage email</span>
        <div class="hero-title">
            Take Control of<br>Your Inbox.
        </div>
        <p class="hero-text">
            Organize what matters, find important messages faster,
            and make room for the things that deserve your attention.
        </p>
    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1, 1])

    with center:
        if st.button(
            "🚀 Get Started",
            type="primary",
            use_container_width=True
        ):
            go("signup")

    st.markdown("## Everything important, in one place")

    a, b, c = st.columns(3)

    with a:
        st.markdown("""
        <div class="feature">
            <h3>🧠 Smart Organization</h3>
            <p>Make important messages easier to find.</p>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="feature">
            <h3>⚡ Less Searching</h3>
            <p>Spend less time searching through messages.</p>
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="feature">
            <h3>🔐 Privacy First</h3>
            <p>Your account security comes first.</p>
        </div>
        """, unsafe_allow_html=True)


# SIGN-UP PAGE
elif st.session_state.user is None and st.session_state.page == "signup":

    st.markdown("## 📝 Create your account")

    with st.form("signup_form"):

        full_name = st.text_input("Full name")
        email = st.text_input("Email address")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input(
            "Confirm password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Create account",
            type="primary",
            use_container_width=True
        )

    if submitted:

        if show_config_warning():
            pass

        elif not full_name.strip():
            st.error("Enter your full name.")

        elif "@" not in email or "." not in email.split("@")[-1]:
            st.error("Enter a valid email address.")

        elif len(password) < 8:
            st.error("Use a password with at least 8 characters.")

        elif password != confirm_password:
            st.error("Your passwords do not match.")

        else:
            try:
                result = supabase.auth.sign_up({
                    "email": email.strip(),
                    "password": password,
                    "options": {
                        "data": {
                            "full_name": full_name.strip()
                        },
                        "email_redirect_to": APP_URL,
                    },
                })

                if result.user and result.session:
                    st.session_state.user = result.user
                    go("dashboard")

                elif result.user:
                    st.success(
                        "Account created! Check your email and click "
                        "the verification link before logging in."
                    )

                else:
                    st.error("Registration could not be completed.")

            except Exception as exc:
                st.error(auth_error_message(exc))

    if st.button("Already registered? Log in"):
        go("login")


# LOGIN PAGE
elif st.session_state.user is None and st.session_state.page == "login":

    st.markdown("## 🔐 Welcome back")

    with st.form("login_form"):

        email = st.text_input("Email address")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button(
            "Log in",
            type="primary",
            use_container_width=True
        )

    if submitted:

        if show_config_warning():
            pass

        elif not email.strip() or not password:
            st.error("Enter your email and password.")

        else:
            try:
                result = supabase.auth.sign_in_with_password({
                    "email": email.strip(),
                    "password": password,
                })

                if result.user:
                    st.session_state.user = result.user
                    go("dashboard")

                else:
                    st.error("Login failed. Try again.")

            except Exception as exc:
                st.error(auth_error_message(exc))

    if st.button("Forgot password?"):
        go("reset")

    if st.button("Create a new account"):
        go("signup")


# PASSWORD RESET PAGE
elif st.session_state.user is None and st.session_state.page == "reset":

    st.markdown("## 🔑 Reset your password")

    with st.form("reset_form"):

        email = st.text_input("Account email")

        submitted = st.form_submit_button(
            "Send reset email",
            use_container_width=True
        )

    if submitted:

        if show_config_warning():
            pass

        elif "@" not in email:
            st.error("Enter a valid email address.")

        else:
            try:
                supabase.auth.reset_password_for_email(
                    email.strip(),
                    options={"redirect_to": APP_URL},
                )

                st.success(
                    "If an account exists for that address, "
                    "a password-reset email should arrive. "
                    "Check your Spam folder too."
                )

            except Exception as exc:
                st.error(auth_error_message(exc))

    if st.button("Back to login"):
        go("login")# DASHBOARD
elif st.session_state.user is not None:

    user = st.session_state.user
    user_email = getattr(user, "email", "") or "Signed-in user"

    st.markdown("## Welcome to SmartMail AI")
    st.caption(f"Signed in as {user_email}")

    st.success("You're signed in. Your workspace is ready.")

    section = st.selectbox(
        "Navigate your workspace",
        [
            "Overview",
            "Inbox",
            "Important",
            "Categories",
            "AI Summaries",
            "Settings",
        ],
    )

    if section == "Overview":

        st.markdown("### Your workspace")

        a, b, c = st.columns(3)

        a.metric("Email accounts", "0")
        b.metric("Unread messages", "—")
        c.metric("AI summaries", "Not enabled")

        st.info(
            "Your dashboard is ready for development. "
            "No email accounts are connected yet."
        )

    elif section == "Inbox":

        st.markdown("### 📥 Inbox")

        st.info(
            "Gmail and Outlook connections are not enabled yet."
        )

    elif section == "Important":

        st.markdown("### ⭐ Important")

        st.info(
            "Important-message detection will be added "
            "when email syncing is implemented."
        )

    elif section == "Categories":

        st.markdown("### 🗂️ Categories")

        st.info(
            "Email categorization is not connected yet."
        )

    elif section == "AI Summaries":

        st.markdown("### 🤖 AI Summaries")

        st.info(
            "AI summaries are not enabled yet."
        )

    elif section == "Settings":

        st.markdown("### ⚙️ Settings")

        st.write("Account:", user_email)

        st.info(
            "Account billing and email-provider settings "
            "are not available yet."
        )

    if st.button("Log out", use_container_width=True):

        try:
            if supabase is not None:
                supabase.auth.sign_out()
        except Exception:
            pass

        st.session_state.user = None
        go("home")


# FOOTER
st.markdown("---")

st.markdown("""
<div class="footer">
    SmartMail AI © 2026<br>
    Your inbox. Smarter. Simpler.<br><br>
    Email syncing, AI features, welcome emails,
    and billing require further setup.
</div>
""", unsafe_allow_html=True)
