import os
import re
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

import requests
import streamlit as st

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================
API_BASE = os.getenv("HOSTEL_API_BASE", "http://127.0.0.1:8000").rstrip("/")
API_TIMEOUT = 12

st.set_page_config(
    page_title="Hostel Management System",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# GLOBAL STYLING (MODERN ENTERPRISE BLUE/WHITE UI)
# ==============================================================================
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --primary: #1976D2;
        --primary-dark: #0D47A1;
        --primary-light: #E3F2FD;
        --bg-main: #F8FAFC;
        --surface: #FFFFFF;
        --text-primary: #0F172A;
        --text-secondary: #475569;
        --border-color: #E2E8F0;
        --success: #15803D;
        --success-bg: #DCFCE7;
        --danger: #B91C1C;
        --danger-bg: #FEE2E2;
        --warning: #B45309;
        --warning-bg: #FEF3C7;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
    }

    #MainMenu, footer, header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0px;
    }

    .block-container {
        max-width: 1440px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
    }

    /* Top Navigation Banner */
    .top-banner {
        background: linear-gradient(135deg, #1565C0 0%, #1976D2 50%, #1E88E5 100%);
        padding: 16px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 16px rgba(21, 101, 192, 0.16);
        color: white;
    }
    .top-banner .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 20px;
        font-weight: 750;
        letter-spacing: -0.3px;
    }
    .top-banner .brand-icon {
        font-size: 24px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 4px 8px;
    }
    .top-banner .user-meta {
        text-align: right;
        line-height: 1.3;
    }
    .top-banner .user-id {
        font-size: 14px;
        font-weight: 700;
    }
    .top-banner .user-role {
        font-size: 12px;
        opacity: 0.9;
        background: rgba(255, 255, 255, 0.25);
        padding: 2px 8px;
        border-radius: 10px;
        display: inline-block;
        margin-top: 2px;
    }

    /* Hero Card for Auth & Pages */
    .hero-container {
        background: linear-gradient(135deg, #0D47A1 0%, #1976D2 100%);
        color: white;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(13, 71, 161, 0.15);
    }
    .hero-title {
        font-size: 26px;
        font-weight: 800;
        margin: 0;
        color: white;
    }
    .hero-subtitle {
        font-size: 14.5px;
        margin: 6px 0 0 0;
        color: #E3F2FD;
        font-weight: 400;
    }

    /* Cards & Panels */
    .hms-card {
        background: #FFFFFF;
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 22px 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    }
    .hms-card-header {
        font-size: 17px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Stat Metric Cards */
    .stat-card {
        background: #FFFFFF;
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .stat-label {
        font-size: 12.5px;
        color: var(--text-secondary);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stat-value {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A;
        margin-top: 4px;
    }
    .stat-icon {
        font-size: 22px;
        margin-bottom: 6px;
    }

    /* Status Badges */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 14px;
        font-size: 11.5px;
        font-weight: 650;
        text-align: center;
    }
    .badge-success { background-color: var(--success-bg); color: var(--success); }
    .badge-danger { background-color: var(--danger-bg); color: var(--danger); }
    .badge-warning { background-color: var(--warning-bg); color: var(--warning); }
    .badge-info { background-color: #E0F2FE; color: #0369A1; }

    /* Persistent Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid var(--border-color) !important;
        min-width: 260px;
    }
    section[data-testid="stSidebar"] > div {
        background-color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 8px 12px !important;
        border-radius: 8px !important;
        font-weight: 550 !important;
        font-size: 14px !important;
        color: #334155 !important;
        transition: all 0.15s ease-in-out;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background-color: #F1F5F9 !important;
        color: #0F172A !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background-color: #E3F2FD !important;
        color: #1565C0 !important;
        font-weight: 700 !important;
    }

    /* Form & Input Aesthetics */
    div[data-testid="stForm"] {
        border-radius: 14px !important;
        border: 1px solid var(--border-color) !important;
        background-color: #FFFFFF !important;
        padding: 26px 28px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
    }

    .stTextInput input, .stTextArea textarea, .stSelectbox select, .stDateInput input {
        border-radius: 8px !important;
        border: 1px solid #CBD5E1 !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #1976D2 !important;
        box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.15) !important;
    }

    /* Buttons */
    .stButton > button[kind="primary"], .stFormSubmitButton > button {
        background-color: #1976D2 !important;
        border-color: #1976D2 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 8px 18px !important;
        box-shadow: 0 2px 4px rgba(25, 118, 210, 0.2) !important;
    }
    .stButton > button[kind="primary"]:hover, .stFormSubmitButton > button:hover {
        background-color: #1565C0 !important;
        border-color: #1565C0 !important;
    }

    /* Clean Tables */
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        background-color: white !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
def init_session_state():
    defaults = {
        "logged_in": False,
        "role": None,  # "Student" or "Admin"
        "token": None,  # JWT access token string
        "user_hsn": "",  # Student HSN (mapped to USN for API compatibility)
        "student_name": "",  # Student Full Name
        "admin_username": "",  # Admin username
        "profile": {},  # Student profile object from /student/me
        "login_tab_index": 0,  # 0: Student Login, 1: Admin Login, 2: Student Registration
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_session_state()


# ==============================================================================
# API CLIENT UTILITIES
# ==============================================================================
def get_auth_headers(auth: bool = True) -> Dict[str, str]:
    headers = {"Accept": "application/json"}
    token = st.session_state.get("token")
    if auth and token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def api_request(
    method: str,
    path: str,
    payload: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    auth: bool = True,
) -> Tuple[bool, Any, int]:
    """Execute HTTP request against the FastAPI backend, preserving existing endpoints and payload schemas."""
    url = f"{API_BASE}/{path.lstrip('/')}"
    headers = get_auth_headers(auth=auth)

    try:
        response = requests.request(
            method=method,
            url=url,
            json=payload,
            params=params,
            headers=headers,
            timeout=API_TIMEOUT,
        )
        try:
            body = response.json()
        except Exception:
            body = response.text

        return response.ok, body, response.status_code
    except requests.RequestException as exc:
        return (
            False,
            {
                "detail": (
                    f"Unable to reach the FastAPI backend at {API_BASE}. "
                    f"Please confirm the backend server is running. Error: {str(exc)}"
                )
            },
            0,
        )


def format_error_message(body: Any, status_code: int) -> str:
    """Format backend error responses into actionable, user-friendly messages without masking backend issues."""
    if isinstance(body, dict):
        detail = body.get("detail", body.get("message", "Request failed."))
        if isinstance(detail, list):
            parts = []
            for item in detail:
                if isinstance(item, dict):
                    loc_parts = [
                        str(x)
                        for x in item.get("loc", [])
                        if str(x) not in ("body",)
                    ]
                    loc = " -> ".join(loc_parts)
                    msg = item.get("msg", str(item))
                    parts.append(f"{loc}: {msg}" if loc else msg)
                else:
                    parts.append(str(item))
            return "; ".join(parts)
        return str(detail)
    elif isinstance(body, str):
        return body
    return f"Request failed with status HTTP {status_code}."


def safe_display_table(
    data: Any,
    column_renames: Optional[Dict[str, str]] = None,
    empty_message: str = "No records found.",
):
    """Utility to display API records cleanly in a Streamlit table, with column renaming for Student HSN."""
    if not data:
        st.info(empty_message)
        return

    records = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                row = item.copy()
                if column_renames:
                    for old_k, new_k in column_renames.items():
                        if old_k in row:
                            row[new_k] = row.pop(old_k)
                records.append(row)
            else:
                records.append({"Value": item})
    elif isinstance(data, dict):
        row = data.copy()
        if column_renames:
            for old_k, new_k in column_renames.items():
                if old_k in row:
                    row[new_k] = row.pop(old_k)
        records = [row]

    if records:
        st.dataframe(records, use_container_width=True, hide_index=True)
    else:
        st.info(empty_message)


# ==============================================================================
# PUBLIC LOGIN & REGISTRATION INTERFACE
# ==============================================================================
def render_public_auth_page():
    # Hero Title Card
    st.markdown(
        """
    <div class="hero-container">
        <h1 class="hero-title">🏨 Hostel Management System</h1>
        <p class="hero-subtitle">Official portal for student accommodation, dining services, fee tracking, and administration</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    _, center_col, _ = st.columns([1, 2.2, 1])

    with center_col:
        tabs = st.tabs(
            [
                "🎓 Student Login",
                "🛡️ Admin Login",
                "📝 Student Registration",
            ]
        )

        # ----------------------------------------------------------------------
        # TAB 1: STUDENT LOGIN
        # ----------------------------------------------------------------------
        with tabs[0]:
            st.markdown(
                """
            <div style="margin-bottom: 16px;">
                <h3 style="margin: 0; color: #1E293B;">Student Portal Login</h3>
                <p style="margin: 4px 0 0 0; color: #64748B; font-size: 13.5px;">
                    Enter your Student HSN and password to access your hostel profile and services.
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            with st.form("student_login_form"):
                student_hsn = st.text_input(
                    "Student HSN",
                    placeholder="Enter your Student HSN",
                    help="Your unique Student Hostel Serial Number / USN registered in the system",
                    key="login_student_hsn_input",
                )
                student_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    key="login_student_password_input",
                )
                student_submit = st.form_submit_button(
                    "Sign In as Student", use_container_width=True
                )

            if student_submit:
                if not student_hsn.strip():
                    st.error("Please enter your Student HSN.")
                elif not student_password:
                    st.error("Please enter your password.")
                else:
                    with st.spinner("Authenticating student credentials..."):
                        # PRESERVE BACKEND API: POST /student/login expects JSON {"usn": ..., "password": ...}
                        ok, body, status = api_request(
                            method="POST",
                            path="/student/login",
                            payload={
                                "usn": student_hsn.strip(),
                                "password": student_password,
                            },
                            auth=False,
                        )

                        if ok and isinstance(body, dict) and body.get("access_token"):
                            st.session_state.logged_in = True
                            st.session_state.role = "Student"
                            st.session_state.token = body["access_token"]
                            st.session_state.user_hsn = student_hsn.strip()

                            # Fetch profile info for display
                            p_ok, p_body, _ = api_request(
                                method="GET", path="/student/me", auth=True
                            )
                            if p_ok and isinstance(p_body, dict):
                                st.session_state.profile = p_body
                                st.session_state.student_name = p_body.get(
                                    "name", "Student"
                                )
                            else:
                                st.session_state.profile = {
                                    "usn": student_hsn.strip()
                                }
                                st.session_state.student_name = "Student"

                            st.success(
                                "Authentication successful! Redirecting to Student Dashboard..."
                            )
                            st.rerun()
                        else:
                            st.error(format_error_message(body, status))

            st.markdown(
                """
            <div style="margin-top: 20px; padding: 14px; background: #F1F5F9; border-radius: 8px; font-size: 13px; color: #475569;">
                <b>New Student?</b> If you have not registered your student account yet, click the <b>Student Registration</b> tab above to create your profile.
            </div>
            """,
                unsafe_allow_html=True,
            )

        # ----------------------------------------------------------------------
        # TAB 2: ADMIN LOGIN (NO PUBLIC ADMIN REGISTRATION)
        # ----------------------------------------------------------------------
        with tabs[1]:
            st.markdown(
                """
            <div style="margin-bottom: 16px;">
                <h3 style="margin: 0; color: #1E293B;">Administrator Access</h3>
                <p style="margin: 4px 0 0 0; color: #64748B; font-size: 13.5px;">
                    Restricted access for authorized hostel wardens and administrative staff.
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            with st.form("admin_login_form"):
                admin_username = st.text_input(
                    "Admin Username / Email",
                    placeholder="Enter your admin username",
                    key="login_admin_user_input",
                )
                admin_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter admin password",
                    key="login_admin_password_input",
                )
                admin_submit = st.form_submit_button(
                    "Sign In as Administrator", use_container_width=True
                )

            if admin_submit:
                if not admin_username.strip():
                    st.error("Please enter your admin username.")
                elif not admin_password:
                    st.error("Please enter your admin password.")
                else:
                    with st.spinner("Authenticating administrator..."):
                        # PRESERVE BACKEND API: POST /admin/login expects JSON {"username": ..., "password": ...}
                        ok, body, status = api_request(
                            method="POST",
                            path="/admin/login",
                            payload={
                                "username": admin_username.strip(),
                                "password": admin_password,
                            },
                            auth=False,
                        )

                        if ok and isinstance(body, dict) and body.get("access_token"):
                            st.session_state.logged_in = True
                            st.session_state.role = "Admin"
                            st.session_state.token = body["access_token"]
                            st.session_state.admin_username = admin_username.strip()

                            st.success(
                                "Admin authentication successful! Redirecting to Admin Dashboard..."
                            )
                            st.rerun()
                        else:
                            st.error(format_error_message(body, status))

            st.markdown(
                """
            <div style="margin-top: 20px; padding: 14px; background: #FEF3C7; border-left: 4px solid #F59E0B; border-radius: 6px; font-size: 12.5px; color: #92400E;">
                <b>Security Notice:</b> Admin accounts can only be provisioned by existing authenticated administrators inside the dashboard. There is no public admin registration.
            </div>
            """,
                unsafe_allow_html=True,
            )

        # ----------------------------------------------------------------------
        # TAB 3: PUBLIC STUDENT REGISTRATION
        # ----------------------------------------------------------------------
        with tabs[2]:
            st.markdown(
                """
            <div style="margin-bottom: 16px;">
                <h3 style="margin: 0; color: #1E293B;">New Student Registration</h3>
                <p style="margin: 4px 0 0 0; color: #64748B; font-size: 13.5px;">
                    Fill in your details below to register your student profile with the hostel system.
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            with st.form("public_student_registration_form"):
                col_a, col_b = st.columns(2)

                with col_a:
                    reg_name = st.text_input("Full Name *", placeholder="e.g. Ramesh Kumar", key="pub_reg_name")
                    reg_hsn = st.text_input(
                        "Student HSN *",
                        placeholder="Enter your Student HSN (e.g. 1UV23AI001)",
                        help="Enter your assigned Student HSN identifier",
                        key="pub_reg_hsn",
                    )
                    reg_email = st.text_input("Email Address *", placeholder="ramesh@example.com", key="pub_reg_email")
                    reg_phone = st.text_input("Phone Number *", placeholder="10-digit mobile number", key="pub_reg_phone")
                    reg_course = st.text_input("Course / Department *", placeholder="e.g. Computer Science, AIML", key="pub_reg_course")
                    reg_year = st.selectbox("Year of Study *", options=[1, 2, 3, 4], index=0, key="pub_reg_year")

                with col_b:
                    reg_gender = st.selectbox("Gender *", options=["Male", "Female", "Other"], key="pub_reg_gender")
                    reg_address = st.text_area("Permanent Address *", placeholder="Enter your full home address", key="pub_reg_addr", height=70)
                    reg_gname = st.text_input("Guardian Name *", placeholder="Parent or guardian name", key="pub_reg_gname")
                    reg_gphone = st.text_input("Guardian Phone *", placeholder="Guardian mobile number", key="pub_reg_gphone")
                    reg_pwd = st.text_input("Password *", type="password", placeholder="Choose a secure password", key="pub_reg_pwd")
                    reg_confirm_pwd = st.text_input("Confirm Password *", type="password", placeholder="Re-enter password", key="pub_reg_cpwd")

                reg_submit = st.form_submit_button("Register Student Account", use_container_width=True)

            if reg_submit:
                # Comprehensive Client-Side Validations
                empty_fields = []
                if not reg_name.strip(): empty_fields.append("Full Name")
                if not reg_hsn.strip(): empty_fields.append("Student HSN")
                if not reg_email.strip(): empty_fields.append("Email Address")
                if not reg_phone.strip(): empty_fields.append("Phone Number")
                if not reg_course.strip(): empty_fields.append("Course / Department")
                if not reg_address.strip(): empty_fields.append("Permanent Address")
                if not reg_gname.strip(): empty_fields.append("Guardian Name")
                if not reg_gphone.strip(): empty_fields.append("Guardian Phone")
                if not reg_pwd: empty_fields.append("Password")

                if empty_fields:
                    st.error(f"Please fill in all mandatory fields: {', '.join(empty_fields)}")
                elif "@" not in reg_email or "." not in reg_email:
                    st.error("Please enter a valid email address.")
                elif len(reg_pwd) < 4:
                    st.error("Password must be at least 4 characters long.")
                elif reg_pwd != reg_confirm_pwd:
                    st.error("Passwords do not match. Please verify and re-enter.")
                else:
                    with st.spinner("Submitting registration to the hostel system..."):
                        # PRESERVE BACKEND API: schemas.StudentCreate expects usn field
                        payload = {
                            "name": reg_name.strip(),
                            "usn": reg_hsn.strip(),
                            "phone": reg_phone.strip(),
                            "email": reg_email.strip(),
                            "course": reg_course.strip(),
                            "year": int(reg_year),
                            "gender": reg_gender,
                            "address": reg_address.strip(),
                            "guardian_name": reg_gname.strip(),
                            "guardian_phone": reg_gphone.strip(),
                            "password": reg_pwd,
                        }

                        ok, body, status = api_request(
                            method="POST",
                            path="/students/",
                            payload=payload,
                            auth=False,
                        )

                        if ok:
                            st.success(
                                f"🎉 Registration successful for {reg_name.strip()}! "
                                f"Your Student HSN is '{reg_hsn.strip()}'. You can now switch to the 'Student Login' tab to log in."
                            )
                        else:
                            st.error(format_error_message(body, status))


# ==============================================================================
# LOGOUT ACTION
# ==============================================================================
def handle_logout():
    for key in [
        "logged_in",
        "role",
        "token",
        "user_hsn",
        "student_name",
        "admin_username",
        "profile",
    ]:
        st.session_state.pop(key, None)
    init_session_state()
    st.rerun()


# ==============================================================================
# TOP BANNER
# ==============================================================================
def render_top_navbar(role: str, user_title: str):
    st.markdown(
        f"""
    <div class="top-banner">
        <div class="brand">
            <span class="brand-icon">🏠</span>
            <span>Hostel Management System</span>
        </div>
        <div class="user-meta">
            <div class="user-id">👤 {user_title}</div>
            <div class="user-role">{role} Portal</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# ADMIN MODULES
# ==============================================================================
def render_admin_dashboard_home():
    st.subheader("📊 Administrative Overview")

    ok, stats, status = api_request("GET", "/dashboard/stats", auth=True)
    if not ok:
        st.warning(f"Could not load dashboard metrics: {format_error_message(stats, status)}")
        stats = {}

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">👥</div>
            <div class="stat-label">Total Students</div>
            <div class="stat-value">{stats.get("total_students", "—")}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">🛏️</div>
            <div class="stat-label">Total Rooms</div>
            <div class="stat-value">{stats.get("total_rooms", "—")}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">🚪</div>
            <div class="stat-label">Available Rooms</div>
            <div class="stat-value" style="color:#15803D;">{stats.get("available_rooms", "—")}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">🔒</div>
            <div class="stat-label">Occupied Rooms</div>
            <div class="stat-value">{stats.get("occupied_rooms", "—")}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    c5, c6, c7 = st.columns(3)
    with c5:
        pending_fees = stats.get("total_pending_fees", 0.0)
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">💰</div>
            <div class="stat-label">Pending Fees</div>
            <div class="stat-value" style="color:#B91C1C;">₹ {float(pending_fees):,.2f}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with c6:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">📋</div>
            <div class="stat-label">Pending Leaves</div>
            <div class="stat-value" style="color:#B45309;">{stats.get("pending_leaves", "—")}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with c7:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">🔔</div>
            <div class="stat-label">Open Complaints</div>
            <div class="stat-value" style="color:#B91C1C;">{stats.get("open_complaints", "—")}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='margin: 24px 0;'>", unsafe_allow_html=True)
    st.info("💡 Use the persistent sidebar navigation to view and manage specific modules.")


def render_admin_student_management():
    st.subheader("👥 Student Management")

    # Search bar
    col_search, col_btn = st.columns([3, 1])
    with col_search:
        search_query = st.text_input(
            "Search Students",
            placeholder="Search by Student HSN or Name...",
            label_visibility="collapsed",
            key="admin_student_search_box",
        )

    ok, students, status = api_request("GET", "/students/", auth=True)
    if not ok:
        st.error(f"Failed to fetch students: {format_error_message(students, status)}")
        return

    filtered_students = students
    if search_query.strip():
        q = search_query.strip().lower()
        filtered_students = [
            s
            for s in students
            if q in str(s.get("usn", "")).lower()
            or q in str(s.get("name", "")).lower()
            or q in str(s.get("email", "")).lower()
        ]

    st.markdown(f"**Total Registered Students:** {len(filtered_students)}")

    # Format table with Student HSN label
    safe_display_table(
        filtered_students,
        column_renames={"usn": "Student HSN"},
        empty_message="No matching student records found.",
    )

    # Option to delete student
    with st.expander("🗑️ Delete Student Record"):
        with st.form("admin_delete_student_form"):
            del_id = st.number_input("Enter Student ID to delete", min_value=1, step=1, key="del_student_id_input")
            del_submit = st.form_submit_button("Delete Student", type="primary")

        if del_submit:
            with st.spinner("Deleting student record..."):
                d_ok, d_body, d_status = api_request("DELETE", f"/students/{int(del_id)}", auth=True)
                if d_ok:
                    st.success(f"Student ID {del_id} deleted successfully.")
                    st.rerun()
                else:
                    st.error(format_error_message(d_body, d_status))


def render_admin_register_student():
    st.subheader("📝 Register New Student (Admin Side)")
    st.markdown("Add a new student record to the system using the official registration API.")

    with st.form("admin_register_student_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name *", placeholder="e.g. Rahul Sharma", key="adm_reg_name")
            hsn = st.text_input("Student HSN *", placeholder="Enter Student HSN", key="adm_reg_hsn")
            email = st.text_input("Email Address *", placeholder="rahul@example.com", key="adm_reg_email")
            phone = st.text_input("Phone Number *", placeholder="10-digit mobile number", key="adm_reg_phone")
            course = st.text_input("Course / Department *", placeholder="e.g. Information Science", key="adm_reg_course")
            year = st.selectbox("Year of Study *", [1, 2, 3, 4], index=0, key="adm_reg_year")

        with c2:
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"], key="adm_reg_gender")
            address = st.text_area("Permanent Address *", placeholder="Full home address", key="adm_reg_address", height=70)
            guardian_name = st.text_input("Guardian Name *", placeholder="Guardian name", key="adm_reg_gname")
            guardian_phone = st.text_input("Guardian Phone *", placeholder="Guardian phone", key="adm_reg_gphone")
            password = st.text_input("Initial Password *", type="password", placeholder="Set initial password", key="adm_reg_pwd")
            confirm_pwd = st.text_input("Confirm Password *", type="password", placeholder="Confirm password", key="adm_reg_cpwd")

        submit = st.form_submit_button("Register Student", use_container_width=True)

    if submit:
        if not (name.strip() and hsn.strip() and email.strip() and phone.strip() and course.strip() and address.strip() and guardian_name.strip() and guardian_phone.strip() and password):
            st.error("Please fill in all mandatory fields.")
        elif password != confirm_pwd:
            st.error("Passwords do not match.")
        else:
            payload = {
                "name": name.strip(),
                "usn": hsn.strip(),
                "phone": phone.strip(),
                "email": email.strip(),
                "course": course.strip(),
                "year": int(year),
                "gender": gender,
                "address": address.strip(),
                "guardian_name": guardian_name.strip(),
                "guardian_phone": guardian_phone.strip(),
                "password": password,
            }
            with st.spinner("Registering student record..."):
                ok, body, status = api_request("POST", "/students/", payload=payload, auth=True)
                if ok:
                    st.success(f"Student '{name.strip()}' (Student HSN: {hsn.strip()}) registered successfully!")
                else:
                    st.error(format_error_message(body, status))


def render_admin_management():
    st.subheader("🛡️ Administrator Management (Admin Only)")
    st.markdown("Manage administrative accounts for the hostel management system.")

    t1, t2 = st.tabs(["👥 Existing Administrators", "➕ Add New Administrator"])

    with t1:
        ok, admins, status = api_request("GET", "/admin/", auth=True)
        if ok and isinstance(admins, list):
            st.markdown(f"**Total Administrators:** {len(admins)}")
            safe_display_table(admins)

            with st.expander("🗑️ Delete Administrator"):
                with st.form("delete_admin_form"):
                    del_admin_id = st.number_input("Enter Admin ID to remove", min_value=1, step=1, key="del_admin_id_input")
                    del_admin_btn = st.form_submit_button("Delete Administrator", type="primary")

                if del_admin_btn:
                    with st.spinner("Deleting administrator..."):
                        d_ok, d_body, d_status = api_request("DELETE", f"/admin/{int(del_admin_id)}", auth=True)
                        if d_ok:
                            st.success(f"Administrator ID {del_admin_id} deleted successfully.")
                            st.rerun()
                        else:
                            st.error(format_error_message(d_body, d_status))
        else:
            st.error(f"Failed to fetch administrators: {format_error_message(admins, status)}")

    with t2:
        with st.form("create_admin_form"):
            new_admin_user = st.text_input("New Admin Username *", placeholder="e.g. warden_north", key="adm_create_user")
            new_admin_pwd = st.text_input("Admin Password *", type="password", placeholder="Enter secure password", key="adm_create_pwd")
            new_admin_cpwd = st.text_input("Confirm Password *", type="password", placeholder="Re-enter password", key="adm_create_cpwd")
            admin_create_submit = st.form_submit_button("Create Administrator Account", use_container_width=True)

        if admin_create_submit:
            if not new_admin_user.strip() or not new_admin_pwd:
                st.error("Admin username and password are required.")
            elif new_admin_pwd != new_admin_cpwd:
                st.error("Passwords do not match.")
            else:
                with st.spinner("Creating new administrator account..."):
                    payload = {
                        "username": new_admin_user.strip(),
                        "password": new_admin_pwd,
                    }
                    ok, body, status = api_request("POST", "/admin/", payload=payload, auth=True)
                    if ok:
                        st.success(f"Administrator '{new_admin_user.strip()}' created successfully!")
                        st.rerun()
                    else:
                        st.error(format_error_message(body, status))


def render_admin_rooms():
    st.subheader("🛏️ Rooms Management")

    ok, rooms, status = api_request("GET", "/rooms/", auth=True)
    if ok and isinstance(rooms, list):
        st.markdown(f"**Total Configured Rooms:** {len(rooms)}")
        safe_display_table(rooms)
    else:
        st.error(f"Could not load rooms: {format_error_message(rooms, status)}")

    c1, c2 = st.columns(2)
    with c1:
        with st.expander("➕ Add New Room"):
            with st.form("add_room_form"):
                room_no = st.text_input("Room Number *", placeholder="e.g. 101, A-204", key="add_room_no")
                floor = st.number_input("Floor Number *", min_value=0, max_value=20, value=1, key="add_room_floor")
                capacity = st.number_input("Capacity *", min_value=1, max_value=10, value=2, key="add_room_cap")
                room_type = st.selectbox("Room Type *", ["Single", "Double", "Triple"], key="add_room_type")
                room_status = st.selectbox("Status", ["Available", "Full"], key="add_room_status")
                room_submit = st.form_submit_button("Save Room")

            if room_submit:
                if not room_no.strip():
                    st.error("Room number is required.")
                else:
                    payload = {
                        "room_number": room_no.strip(),
                        "floor": int(floor),
                        "capacity": int(capacity),
                        "room_type": room_type,
                        "status": room_status,
                        "occupied": 0,
                    }
                    with st.spinner("Adding room..."):
                        a_ok, a_body, a_status = api_request("POST", "/rooms/", payload=payload, auth=True)
                        if a_ok:
                            st.success(f"Room {room_no.strip()} created successfully!")
                            st.rerun()
                        else:
                            st.error(format_error_message(a_body, a_status))

    with c2:
        with st.expander("🗑️ Delete Room"):
            with st.form("delete_room_form"):
                del_room_id = st.number_input("Enter Room ID to delete", min_value=1, step=1, key="del_room_id_input")
                del_room_btn = st.form_submit_button("Delete Room", type="primary")

            if del_room_btn:
                with st.spinner("Deleting room..."):
                    d_ok, d_body, d_status = api_request("DELETE", f"/rooms/{int(del_room_id)}", auth=True)
                    if d_ok:
                        st.success(f"Room ID {del_room_id} deleted successfully.")
                        st.rerun()
                    else:
                        st.error(format_error_message(d_body, d_status))


def render_admin_allocations():
    st.subheader("🔑 Room Allocations")

    # PRESERVE BACKEND ROUTER: /allocations/
    ok, allocations, status = api_request("GET", "/allocations/", auth=True)
    if ok and isinstance(allocations, list):
        st.markdown(f"**Total Room Allocations:** {len(allocations)}")
        safe_display_table(allocations)
    else:
        st.error(f"Could not load allocations: {format_error_message(allocations, status)}")

    c1, c2 = st.columns(2)
    with c1:
        with st.expander("➕ Allocate Room to Student"):
            with st.form("create_allocation_form"):
                alloc_sid = st.number_input("Student ID *", min_value=1, step=1, key="alloc_sid_input")
                alloc_rid = st.number_input("Room ID *", min_value=1, step=1, key="alloc_rid_input")
                alloc_date = st.date_input("Allocation Date *", value=date.today(), key="alloc_date_input")
                alloc_submit = st.form_submit_button("Allocate Room")

            if alloc_submit:
                payload = {
                    "student_id": int(alloc_sid),
                    "room_id": int(alloc_rid),
                    "allocated_date": alloc_date.isoformat(),
                }
                with st.spinner("Allocating room..."):
                    a_ok, a_body, a_status = api_request("POST", "/allocations/", payload=payload, auth=True)
                    if a_ok:
                        st.success("Room successfully allocated to student!")
                        st.rerun()
                    else:
                        st.error(format_error_message(a_body, a_status))

    with c2:
        with st.expander("🗑️ Deallocate / Remove Allocation"):
            with st.form("delete_allocation_form"):
                del_alloc_id = st.number_input("Enter Allocation ID to remove", min_value=1, step=1, key="del_alloc_id_input")
                del_alloc_btn = st.form_submit_button("Remove Allocation", type="primary")

            if del_alloc_btn:
                with st.spinner("Removing allocation..."):
                    d_ok, d_body, d_status = api_request("DELETE", f"/allocations/{int(del_alloc_id)}", auth=True)
                    if d_ok:
                        st.success(f"Allocation ID {del_alloc_id} removed successfully.")
                        st.rerun()
                    else:
                        st.error(format_error_message(d_body, d_status))


def render_admin_attendance():
    st.subheader("📅 Attendance Management")

    ok, records, status = api_request("GET", "/attendance/", auth=True)
    if ok and isinstance(records, list):
        st.markdown(f"**Total Attendance Records:** {len(records)}")
        safe_display_table(records)
    else:
        st.error(f"Could not load attendance records: {format_error_message(records, status)}")

    c1, c2 = st.columns(2)
    with c1:
        with st.expander("✓ Mark Student Attendance"):
            with st.form("mark_attendance_form"):
                att_sid = st.number_input("Student ID *", min_value=1, step=1, key="att_sid_input")
                att_date = st.date_input("Date *", value=date.today(), key="att_date_input")
                att_status = st.selectbox("Attendance Status *", ["Present", "Absent"], key="att_status_input")
                att_marked_by = st.number_input("Marked By (Admin ID, optional)", min_value=1, step=1, value=1, key="att_marker_input")
                att_submit = st.form_submit_button("Record Attendance")

            if att_submit:
                payload = {
                    "student_id": int(att_sid),
                    "date": att_date.isoformat(),
                    "status": att_status,
                    "marked_by": int(att_marked_by),
                }
                with st.spinner("Recording attendance..."):
                    a_ok, a_body, a_status = api_request("POST", "/attendance/", payload=payload, auth=True)
                    if a_ok:
                        st.success(f"Attendance recorded as {att_status} for Student ID {att_sid}.")
                        st.rerun()
                    else:
                        st.error(format_error_message(a_body, a_status))

    with c2:
        with st.expander("🗑️ Delete Attendance Record"):
            with st.form("delete_attendance_form"):
                del_att_id = st.number_input("Enter Attendance ID to delete", min_value=1, step=1, key="del_att_id_input")
                del_att_btn = st.form_submit_button("Delete Record", type="primary")

            if del_att_btn:
                with st.spinner("Deleting record..."):
                    d_ok, d_body, d_status = api_request("DELETE", f"/attendance/{int(del_att_id)}", auth=True)
                    if d_ok:
                        st.success(f"Attendance record ID {del_att_id} deleted successfully.")
                        st.rerun()
                    else:
                        st.error(format_error_message(d_body, d_status))


def render_admin_food_menu():
    st.subheader("🍴 Daily Food Menu Management")

    # PRESERVE BACKEND ROUTE: /food/menu
    ok, menus, status = api_request("GET", "/food/menu", auth=True)
    if ok and isinstance(menus, list):
        st.markdown(f"**Total Food Menus:** {len(menus)}")
        safe_display_table(menus)
    else:
        st.error(f"Could not load food menus: {format_error_message(menus, status)}")

    c1, c2 = st.columns(2)
    with c1:
        with st.expander("➕ Add Food Menu"):
            with st.form("add_food_menu_form"):
                f_date = st.date_input("Menu Date *", value=date.today(), key="menu_date_input")
                meal_type = st.selectbox("Meal Type *", ["Breakfast", "Lunch", "Dinner", "Snacks"], key="menu_meal_type")
                menu_items = st.text_area("Menu Details *", placeholder="e.g. Idli, Sambar, Chutney, Tea", key="menu_items_input")
                availability = st.selectbox("Availability", ["Available", "Not Available"], key="menu_avail_input")
                menu_submit = st.form_submit_button("Publish Menu")

            if menu_submit:
                if not menu_items.strip():
                    st.error("Please enter the menu items.")
                else:
                    payload = {
                        "date": f_date.isoformat(),
                        "meal_type": meal_type,
                        "menu": menu_items.strip(),
                        "availability": availability,
                    }
                    with st.spinner("Publishing food menu..."):
                        a_ok, a_body, a_status = api_request("POST", "/food/menu", payload=payload, auth=True)
                        if a_ok:
                            st.success("Food menu published successfully!")
                            st.rerun()
                        else:
                            st.error(format_error_message(a_body, a_status))

    with c2:
        with st.expander("🗑️ Delete Food Menu"):
            with st.form("delete_food_menu_form"):
                del_food_id = st.number_input("Enter Food Menu ID to delete", min_value=1, step=1, key="del_food_id_input")
                del_food_btn = st.form_submit_button("Delete Menu", type="primary")

            if del_food_btn:
                with st.spinner("Deleting menu..."):
                    d_ok, d_body, d_status = api_request("DELETE", f"/food/menu/{int(del_food_id)}", auth=True)
                    if d_ok:
                        st.success(f"Food menu ID {del_food_id} deleted successfully.")
                        st.rerun()
                    else:
                        st.error(format_error_message(d_body, d_status))


def render_admin_fees():
    st.subheader("💰 Fees Management")

    ok, fees, status = api_request("GET", "/fees/", auth=True)
    if ok and isinstance(fees, list):
        st.markdown(f"**Total Fee Records:** {len(fees)}")
        safe_display_table(fees)
    else:
        st.error(f"Could not load fee records: {format_error_message(fees, status)}")

    c1, c2 = st.columns(2)
    with c1:
        with st.expander("➕ Create Fee Record"):
            with st.form("create_fee_form"):
                fee_sid = st.number_input("Student ID *", min_value=1, step=1, key="fee_sid_input")
                fee_amount = st.number_input("Amount (₹) *", min_value=100.0, step=500.0, value=5000.0, key="fee_amt_input")
                fee_due_date = st.date_input("Due Date *", value=date.today(), key="fee_due_date_input")
                fee_status = st.selectbox("Payment Status *", ["Pending", "Paid"], key="fee_status_input")
                fee_submit = st.form_submit_button("Create Fee Record")

            if fee_submit:
                payload = {
                    "student_id": int(fee_sid),
                    "amount": float(fee_amount),
                    "due_date": fee_due_date.isoformat(),
                    "payment_date": date.today().isoformat() if fee_status == "Paid" else None,
                    "status": fee_status,
                }
                with st.spinner("Creating fee record..."):
                    a_ok, a_body, a_status = api_request("POST", "/fees/", payload=payload, auth=True)
                    if a_ok:
                        st.success("Fee record created successfully!")
                        st.rerun()
                    else:
                        st.error(format_error_message(a_body, a_status))

    with c2:
        with st.expander("🗑️ Delete Fee Record"):
            with st.form("delete_fee_form"):
                del_fee_id = st.number_input("Enter Fee ID to delete", min_value=1, step=1, key="del_fee_id_input")
                del_fee_btn = st.form_submit_button("Delete Fee Record", type="primary")

            if del_fee_btn:
                with st.spinner("Deleting fee record..."):
                    d_ok, d_body, d_status = api_request("DELETE", f"/fees/{int(del_fee_id)}", auth=True)
                    if d_ok:
                        st.success(f"Fee record ID {del_fee_id} deleted successfully.")
                        st.rerun()
                    else:
                        st.error(format_error_message(d_body, d_status))


def render_admin_complaints():
    st.subheader("🔔 Student Complaints")

    ok, complaints, status = api_request("GET", "/complaints/", auth=True)
    if ok and isinstance(complaints, list):
        st.markdown(f"**Total Complaints Registered:** {len(complaints)}")
        safe_display_table(complaints)

        c1, c2 = st.columns(2)
        with c1:
            with st.expander("🔄 Update Complaint Status"):
                with st.form("update_complaint_form"):
                    cmp_id = st.number_input("Complaint ID *", min_value=1, step=1, key="upd_cmp_id")
                    cmp_status = st.selectbox("New Status *", ["Open", "In Progress", "Resolved"], key="upd_cmp_status")
                    cmp_submit = st.form_submit_button("Update Status")

                if cmp_submit:
                    with st.spinner("Updating status..."):
                        # PRESERVE BACKEND ROUTE: PUT /complaints/{id}?status=...
                        u_ok, u_body, u_status = api_request(
                            "PUT", f"/complaints/{int(cmp_id)}", params={"status": cmp_status}, auth=True
                        )
                        if u_ok:
                            st.success(f"Complaint ID {cmp_id} updated to '{cmp_status}'.")
                            st.rerun()
                        else:
                            st.error(format_error_message(u_body, u_status))

        with c2:
            with st.expander("🗑️ Delete Complaint"):
                with st.form("delete_complaint_form"):
                    del_cmp_id = st.number_input("Enter Complaint ID to delete", min_value=1, step=1, key="del_cmp_id_input")
                    del_cmp_btn = st.form_submit_button("Delete Complaint", type="primary")

                if del_cmp_btn:
                    with st.spinner("Deleting complaint..."):
                        d_ok, d_body, d_status = api_request("DELETE", f"/complaints/{int(del_cmp_id)}", auth=True)
                        if d_ok:
                            st.success(f"Complaint ID {del_cmp_id} deleted.")
                            st.rerun()
                        else:
                            st.error(format_error_message(d_body, d_status))
    else:
        st.error(f"Could not load complaints: {format_error_message(complaints, status)}")


def render_admin_leaves():
    st.subheader("📋 Leave & Outpass Requests")

    ok, leaves, status = api_request("GET", "/leaves/", auth=True)
    if ok and isinstance(leaves, list):
        st.markdown(f"**Total Leave Requests:** {len(leaves)}")
        safe_display_table(leaves)

        c1, c2 = st.columns(2)
        with c1:
            with st.expander("🔄 Update Leave Status (Approve / Reject)"):
                with st.form("update_leave_form"):
                    leave_id = st.number_input("Leave Request ID *", min_value=1, step=1, key="upd_leave_id")
                    leave_status = st.selectbox("Action *", ["Approved", "Rejected", "Pending"], key="upd_leave_status")
                    leave_submit = st.form_submit_button("Update Leave Status")

                if leave_submit:
                    with st.spinner("Updating leave status..."):
                        # PRESERVE BACKEND ROUTE: PUT /leaves/{id} with JSON {"status": ...}
                        u_ok, u_body, u_status = api_request(
                            "PUT", f"/leaves/{int(leave_id)}", payload={"status": leave_status}, auth=True
                        )
                        if u_ok:
                            st.success(f"Leave Request ID {leave_id} set to '{leave_status}'.")
                            st.rerun()
                        else:
                            st.error(format_error_message(u_body, u_status))

        with c2:
            with st.expander("🗑️ Delete Leave Record"):
                with st.form("delete_leave_form"):
                    del_leave_id = st.number_input("Enter Leave ID to delete", min_value=1, step=1, key="del_leave_id_input")
                    del_leave_btn = st.form_submit_button("Delete Leave Record", type="primary")

                if del_leave_btn:
                    with st.spinner("Deleting leave record..."):
                        d_ok, d_body, d_status = api_request("DELETE", f"/leaves/{int(del_leave_id)}", auth=True)
                        if d_ok:
                            st.success(f"Leave ID {del_leave_id} deleted.")
                            st.rerun()
                        else:
                            st.error(format_error_message(d_body, d_status))
    else:
        st.error(f"Could not load leave records: {format_error_message(leaves, status)}")


def render_admin_visitor_management():
    st.subheader("🚪 Visitor Management")

    st.markdown(
        """
    <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-left: 5px solid #F59E0B; padding: 20px; border-radius: 8px;">
        <h4 style="margin: 0 0 8px 0; color: #92400E;">Backend Capability Notice</h4>
        <p style="margin: 0; color: #78350F; font-size: 14px; line-height: 1.5;">
            The <b>Visitor Management</b> feature is currently not supported by the FastAPI backend.
            No visitor data model or dedicated API route (such as <code>/visitors</code>) exists in the database schema.
        </p>
        <p style="margin: 10px 0 0 0; color: #78350F; font-size: 13.5px;">
            In accordance with project guidelines, this frontend does not simulate fake visitor records. Once visitor models and endpoints are added to the backend, they will be surfaced here immediately.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# STUDENT MODULES
# ==============================================================================
def render_student_dashboard_home():
    st.subheader("🎓 Student Portal Overview")

    p = st.session_state.get("profile", {})
    student_name = p.get("name", st.session_state.get("student_name", "Student"))
    student_hsn = p.get("usn", st.session_state.get("user_hsn", "—"))

    # Fetch room
    r_ok, room, _ = api_request("GET", "/student/my-room", auth=True)
    room_number = room.get("room_number", "Not Allocated") if r_ok and isinstance(room, dict) else "Not Allocated"

    # Fetch fees
    f_ok, fees, _ = api_request("GET", "/student/my-fees", auth=True)
    pending_fee_total = 0.0
    if f_ok and isinstance(fees, list):
        for f in fees:
            if str(f.get("status", "")).lower() == "pending":
                pending_fee_total += float(f.get("amount", 0.0) or 0.0)

    # Fetch complaints
    c_ok, complaints, _ = api_request("GET", "/student/my-complaints", auth=True)
    open_complaints = 0
    if c_ok and isinstance(complaints, list):
        open_complaints = sum(1 for c in complaints if str(c.get("status", "")).lower() != "resolved")

    # Fetch attendance
    a_ok, att, _ = api_request("GET", "/student/my-attendance", auth=True)
    total_attendance = len(att) if a_ok and isinstance(att, list) else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">🛏️</div>
            <div class="stat-label">Allocated Room</div>
            <div class="stat-value">{room_number}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">💰</div>
            <div class="stat-label">Pending Fees</div>
            <div class="stat-value" style="color: {'#B91C1C' if pending_fee_total > 0 else '#15803D'};">₹ {pending_fee_total:,.2f}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">📅</div>
            <div class="stat-label">Attendance Records</div>
            <div class="stat-value">{total_attendance}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">🔔</div>
            <div class="stat-label">Active Complaints</div>
            <div class="stat-value" style="color: {'#B91C1C' if open_complaints > 0 else '#15803D'};">{open_complaints}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='margin: 24px 0;'>", unsafe_allow_html=True)

    col_notif, col_menu = st.columns(2)
    with col_notif:
        st.markdown(
            f"""
        <div class="hms-card">
            <div class="hms-card-header">📌 Profile Summary</div>
            <p><b>Student Name:</b> {student_name}</p>
            <p><b>Student HSN:</b> {student_hsn}</p>
            <p><b>Department / Course:</b> {p.get("course", "—")}</p>
            <p><b>Year of Study:</b> Year {p.get("year", "—")}</p>
            <p><b>Email:</b> {p.get("email", "—")}</p>
            <p><b>Phone:</b> {p.get("phone", "—")}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_menu:
        st.markdown(
            """
        <div class="hms-card">
            <div class="hms-card-header">🍴 Today's Food Menu Preview</div>
        """,
            unsafe_allow_html=True,
        )
        m_ok, menu_list, _ = api_request("GET", "/student/my-food-menu", auth=True)
        if m_ok and isinstance(menu_list, list) and menu_list:
            safe_display_table(menu_list[:3])
        else:
            st.info("No daily menu items published for today yet.")
        st.markdown("</div>", unsafe_allow_html=True)


def render_student_profile():
    st.subheader("👤 My Profile")

    ok, profile, status = api_request("GET", "/student/me", auth=True)
    if not ok:
        st.error(f"Could not load student profile: {format_error_message(profile, status)}")
        return

    # Update local session profile
    st.session_state.profile = profile

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""
        <div class="hms-card">
            <div class="hms-card-header">Academic & Contact Information</div>
            <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                <tr style="border-bottom: 1px solid #F1F5F9; height: 36px;">
                    <td style="color: #64748B; width: 40%;"><b>Full Name</b></td>
                    <td><b>{profile.get("name", "—")}</b></td>
                </tr>
                <tr style="border-bottom: 1px solid #F1F5F9; height: 36px;">
                    <td style="color: #64748B;"><b>Student HSN</b></td>
                    <td><span class="badge badge-info">{profile.get("usn", "—")}</span></td>
                </tr>
                <tr style="border-bottom: 1px solid #F1F5F9; height: 36px;">
                    <td style="color: #64748B;"><b>Email Address</b></td>
                    <td>{profile.get("email", "—")}</td>
                </tr>
                <tr style="border-bottom: 1px solid #F1F5F9; height: 36px;">
                    <td style="color: #64748B;"><b>Mobile Phone</b></td>
                    <td>{profile.get("phone", "—")}</td>
                </tr>
                <tr style="border-bottom: 1px solid #F1F5F9; height: 36px;">
                    <td style="color: #64748B;"><b>Department / Course</b></td>
                    <td>{profile.get("course", "—")}</td>
                </tr>
                <tr style="height: 36px;">
                    <td style="color: #64748B;"><b>Year of Study</b></td>
                    <td>Year {profile.get("year", "—")}</td>
                </tr>
            </table>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
        <div class="hms-card">
            <div class="hms-card-header">Personal & Guardian Details</div>
            <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                <tr style="border-bottom: 1px solid #F1F5F9; height: 36px;">
                    <td style="color: #64748B; width: 40%;"><b>Gender</b></td>
                    <td>{profile.get("gender", "—")}</td>
                </tr>
                <tr style="border-bottom: 1px solid #F1F5F9; height: 36px;">
                    <td style="color: #64748B;"><b>Guardian Name</b></td>
                    <td>{profile.get("guardian_name", "—")}</td>
                </tr>
                <tr style="border-bottom: 1px solid #F1F5F9; height: 36px;">
                    <td style="color: #64748B;"><b>Guardian Phone</b></td>
                    <td>{profile.get("guardian_phone", "—")}</td>
                </tr>
                <tr style="height: 36px;">
                    <td style="color: #64748B; vertical-align: top; padding-top: 6px;"><b>Permanent Address</b></td>
                    <td style="vertical-align: top; padding-top: 6px;">{profile.get("address", "—")}</td>
                </tr>
            </table>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_student_room():
    st.subheader("🛏️ My Room Details")

    ok, room, status = api_request("GET", "/student/my-room", auth=True)
    if not ok:
        if status == 404:
            st.info("ℹ️ No room has been allocated to your account yet. Please contact the hostel administration.")
        else:
            st.error(f"Could not load room information: {format_error_message(room, status)}")
        return

    c1, c2 = st.columns([1, 1.4])
    with c1:
        st.markdown(
            f"""
        <div class="hms-card" style="text-align: center;">
            <div style="font-size: 42px; margin-bottom: 8px;">🛏️</div>
            <div style="font-size: 13px; color: #64748B; font-weight: 600; text-transform: uppercase;">Room Number</div>
            <div style="font-size: 32px; font-weight: 800; color: #1565C0; margin: 4px 0;">{room.get("room_number", "—")}</div>
            <div><span class="badge badge-success">{room.get("status", "Allocated")}</span></div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
        <div class="hms-card">
            <div class="hms-card-header">Allocation Details</div>
            <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                <tr style="border-bottom: 1px solid #F1F5F9; height: 36px;">
                    <td style="color: #64748B;"><b>Floor</b></td>
                    <td>Floor {room.get("floor", "—")}</td>
                </tr>
                <tr style="border-bottom: 1px solid #F1F5F9; height: 36px;">
                    <td style="color: #64748B;"><b>Room Type</b></td>
                    <td>{room.get("room_type", "—")}</td>
                </tr>
                <tr style="border-bottom: 1px solid #F1F5F9; height: 36px;">
                    <td style="color: #64748B;"><b>Total Capacity</b></td>
                    <td>{room.get("capacity", "—")} Students</td>
                </tr>
                <tr style="border-bottom: 1px solid #F1F5F9; height: 36px;">
                    <td style="color: #64748B;"><b>Current Occupancy</b></td>
                    <td>{room.get("occupied", "—")} Students</td>
                </tr>
                <tr style="height: 36px;">
                    <td style="color: #64748B;"><b>Allocation Date</b></td>
                    <td>{room.get("allocated_date", "—")}</td>
                </tr>
            </table>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_student_attendance():
    st.subheader("📅 My Attendance")

    ok, records, status = api_request("GET", "/student/my-attendance", auth=True)
    if not ok:
        st.error(f"Could not load attendance: {format_error_message(records, status)}")
        return

    if isinstance(records, list) and records:
        total = len(records)
        present = sum(1 for r in records if str(r.get("status", "")).lower() == "present")
        absent = total - present
        pct = (present / total) * 100 if total > 0 else 0

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Records", total)
        with c2:
            st.metric("Days Present", present)
        with c3:
            st.metric("Days Absent", absent)
        with c4:
            st.metric("Attendance Rate", f"{pct:.1f}%")

        st.markdown("<hr style='margin: 16px 0;'>", unsafe_allow_html=True)
        safe_display_table(records)
    else:
        st.info("No attendance records found for your account.")


def render_student_fees():
    st.subheader("💰 My Fees")

    ok, fees, status = api_request("GET", "/student/my-fees", auth=True)
    if not ok:
        st.error(f"Could not load fee records: {format_error_message(fees, status)}")
        return

    if isinstance(fees, list) and fees:
        pending_total = sum(
            float(f.get("amount", 0.0) or 0.0)
            for f in fees
            if str(f.get("status", "")).lower() == "pending"
        )
        paid_total = sum(
            float(f.get("amount", 0.0) or 0.0)
            for f in fees
            if str(f.get("status", "")).lower() == "paid"
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Pending", f"₹ {pending_total:,.2f}")
        with c2:
            st.metric("Total Paid", f"₹ {paid_total:,.2f}")
        with c3:
            st.metric("Fee Records", len(fees))

        st.markdown("<hr style='margin: 16px 0;'>", unsafe_allow_html=True)
        safe_display_table(fees)
    else:
        st.info("No fee records registered for your account.")


def render_student_complaints():
    st.subheader("🔔 My Complaints")

    ok, complaints, status = api_request("GET", "/student/my-complaints", auth=True)
    if ok and isinstance(complaints, list):
        safe_display_table(complaints, empty_message="You have not submitted any complaints yet.")
    else:
        st.error(f"Could not load complaints: {format_error_message(complaints, status)}")

    with st.expander("➕ Submit a New Complaint"):
        with st.form("submit_complaint_form"):
            complaint_text = st.text_area(
                "Describe the issue *",
                placeholder="e.g. Bathroom tap leaking, study light not functioning...",
                key="student_complaint_input",
            )
            cmp_submit = st.form_submit_button("Submit Complaint")

        if cmp_submit:
            if not complaint_text.strip():
                st.error("Please enter your complaint details.")
            else:
                with st.spinner("Submitting complaint..."):
                    # PRESERVE BACKEND ROUTE: POST /student/my-complaints expects query parameter 'complaint'
                    c_ok, c_body, c_status = api_request(
                        "POST",
                        "/student/my-complaints",
                        params={"complaint": complaint_text.strip()},
                        auth=True,
                    )
                    if c_ok:
                        st.success("Your complaint has been submitted successfully.")
                        st.rerun()
                    else:
                        st.error(format_error_message(c_body, c_status))


def render_student_leaves():
    st.subheader("📝 Leave & Outpass Requests")

    ok, leaves, status = api_request("GET", "/student/my-leaves", auth=True)
    if ok and isinstance(leaves, list):
        safe_display_table(leaves, empty_message="You have no submitted leave requests.")
    else:
        st.error(f"Could not load leave records: {format_error_message(leaves, status)}")

    with st.expander("➕ Apply for Leave / Outpass"):
        with st.form("student_leave_application_form"):
            c1, c2 = st.columns(2)
            with c1:
                start_d = st.date_input("Start Date *", value=date.today(), key="leave_start_d")
            with c2:
                end_d = st.date_input("End Date *", value=date.today(), key="leave_end_d")
            reason = st.text_area("Reason for Leave *", placeholder="e.g. Family function, medical leave", key="leave_reason_input")
            leave_sub = st.form_submit_button("Submit Leave Application")

        if leave_sub:
            if end_d < start_d:
                st.error("End date cannot be earlier than start date.")
            elif not reason.strip():
                st.error("Please provide a reason for the leave.")
            else:
                with st.spinner("Submitting leave request..."):
                    payload = {
                        "start_date": start_d.isoformat(),
                        "end_date": end_d.isoformat(),
                        "reason": reason.strip(),
                    }
                    l_ok, l_body, l_status = api_request("POST", "/student/my-leaves", payload=payload, auth=True)
                    if l_ok:
                        st.success("Leave request submitted successfully. Awaiting warden approval.")
                        st.rerun()
                    else:
                        st.error(format_error_message(l_body, l_status))


def render_student_food_menu():
    st.subheader("🍴 Daily Food Menu")

    ok, menus, status = api_request("GET", "/student/my-food-menu", auth=True)
    if ok and isinstance(menus, list):
        safe_display_table(menus, empty_message="No food menus currently available.")
    else:
        st.error(f"Could not load food menu: {format_error_message(menus, status)}")


def render_student_food_consumption():
    st.subheader("🍽️ Food Consumption Tracker")

    ok, records, status = api_request("GET", "/student/my-food-consumption", auth=True)
    if ok and isinstance(records, list):
        safe_display_table(records, empty_message="No meal consumption records found.")
    else:
        st.error(f"Could not load consumption records: {format_error_message(records, status)}")

    with st.expander("✓ Record Meal Consumption"):
        # Fetch current menus to let student pick valid food_id
        m_ok, menu_list, _ = api_request("GET", "/student/my-food-menu", auth=True)
        menu_options = {}
        if m_ok and isinstance(menu_list, list):
            for m in menu_list:
                label = f"ID {m.get('food_id')} - {m.get('date')} ({m.get('meal_type')}): {m.get('menu')}"
                menu_options[label] = m.get("food_id")

        with st.form("mark_food_consumption_form"):
            if menu_options:
                selected_menu_label = st.selectbox("Select Meal Menu *", options=list(menu_options.keys()))
                cons_status = st.selectbox("Consumption Status *", ["Taken", "Not Taken"])
                cons_submit = st.form_submit_button("Save Meal Record")

                if cons_submit:
                    food_id = menu_options[selected_menu_label]
                    payload = {
                        "food_id": int(food_id),
                        "status": cons_status,
                    }
                    with st.spinner("Recording meal consumption..."):
                        c_ok, c_body, c_status = api_request(
                            "POST", "/student/my-food-consumption", payload=payload, auth=True
                        )
                        if c_ok:
                            st.success("Meal consumption record updated successfully.")
                            st.rerun()
                        else:
                            st.error(format_error_message(c_body, c_status))
            else:
                st.info("No active food menus available to select.")
                st.form_submit_button("Refresh", disabled=True)


# ==============================================================================
# MAIN APPLICATION CONTROLLER
# ==============================================================================
def main():
    if not st.session_state.logged_in:
        render_public_auth_page()
        return

    role = st.session_state.role

    # Render Persistent Sidebar
    with st.sidebar:
        st.markdown(
            """
        <div style="padding: 10px 0 16px 0; border-bottom: 1px solid #E2E8F0; margin-bottom: 14px;">
            <div style="font-size: 18px; font-weight: 800; color: #1E293B; display: flex; align-items: center; gap: 8px;">
                <span>🏨</span> <span>HMS Portal</span>
            </div>
            <div style="font-size: 12px; color: #64748B; margin-top: 4px;">Hostel Management System</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if role == "Admin":
            st.caption(f"Signed in as: **{st.session_state.admin_username}**")
            admin_pages = [
                "📊 Dashboard",
                "👥 Student Management",
                "📝 Register Student",
                "🛡️ Admin Management",
                "🛏️ Rooms",
                "🔑 Room Allocation",
                "📅 Attendance",
                "🍴 Daily Food Menu",
                "💰 Fees Management",
                "🔔 Complaints",
                "📋 Leave Requests",
                "🚪 Visitor Management",
            ]
            selected_page = st.radio("ADMIN NAVIGATION", admin_pages, key="admin_nav_radio")
        else:
            p = st.session_state.get("profile", {})
            st.caption(f"Student HSN: **{p.get('usn', st.session_state.user_hsn)}**")
            student_pages = [
                "📊 Dashboard",
                "👤 My Profile",
                "🛏️ My Room",
                "📅 My Attendance",
                "💰 My Fees",
                "🔔 My Complaints",
                "📝 Leave / Outpass",
                "🍴 Daily Food Menu",
                "🍽️ Food Consumption",
            ]
            selected_page = st.radio("STUDENT NAVIGATION", student_pages, key="student_nav_radio")

        st.markdown("<hr style='margin: 20px 0 16px 0;'>", unsafe_allow_html=True)
        if st.button("↪ Sign Out", use_container_width=True, type="secondary"):
            handle_logout()

    # Render Main View Area
    user_title = (
        st.session_state.admin_username
        if role == "Admin"
        else st.session_state.get("student_name", "Student")
    )
    render_top_navbar(role=role, user_title=user_title)

    if role == "Admin":
        if selected_page == "📊 Dashboard":
            render_admin_dashboard_home()
        elif selected_page == "👥 Student Management":
            render_admin_student_management()
        elif selected_page == "📝 Register Student":
            render_admin_register_student()
        elif selected_page == "🛡️ Admin Management":
            render_admin_management()
        elif selected_page == "🛏️ Rooms":
            render_admin_rooms()
        elif selected_page == "🔑 Room Allocation":
            render_admin_allocations()
        elif selected_page == "📅 Attendance":
            render_admin_attendance()
        elif selected_page == "🍴 Daily Food Menu":
            render_admin_food_menu()
        elif selected_page == "💰 Fees Management":
            render_admin_fees()
        elif selected_page == "🔔 Complaints":
            render_admin_complaints()
        elif selected_page == "📋 Leave Requests":
            render_admin_leaves()
        elif selected_page == "🚪 Visitor Management":
            render_admin_visitor_management()
    else:
        if selected_page == "📊 Dashboard":
            render_student_dashboard_home()
        elif selected_page == "👤 My Profile":
            render_student_profile()
        elif selected_page == "🛏️ My Room":
            render_student_room()
        elif selected_page == "📅 My Attendance":
            render_student_attendance()
        elif selected_page == "💰 My Fees":
            render_student_fees()
        elif selected_page == "🔔 My Complaints":
            render_student_complaints()
        elif selected_page == "📝 Leave / Outpass":
            render_student_leaves()
        elif selected_page == "🍴 Daily Food Menu":
            render_student_food_menu()
        elif selected_page == "🍽️ Food Consumption":
            render_student_food_consumption()


if __name__ == "__main__":
    main()