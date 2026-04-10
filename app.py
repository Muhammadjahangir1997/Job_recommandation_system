import streamlit as st
from groq import Groq
import PyPDF2
import docx
import io
import json

# Page config
st.set_page_config(
    page_title="AI Job Recommender",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #12121a;
    --card: #1a1a26;
    --accent: #6c63ff;
    --accent2: #ff6584;
    --gold: #ffd700;
    --text: #e8e8f0;
    --muted: #7878a0;
    --border: #2a2a3d;
}

* { font-family: 'DM Sans', sans-serif; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
}

[data-testid="stHeader"] { background: transparent !important; }

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text) !important;
}

.hero {
    text-align: center;
    padding: 60px 20px 40px;
    position: relative;
}

.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    color: white;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    margin-bottom: 20px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, var(--accent) 50%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
    margin-bottom: 16px;
}

.hero-sub {
    color: var(--muted);
    font-size: 1.1rem;
    max-width: 500px;
    margin: 0 auto 40px;
    line-height: 1.6;
}

.upload-zone {
    background: var(--card);
    border: 2px dashed var(--border);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    transition: all 0.3s ease;
    margin-bottom: 24px;
}

.upload-zone:hover {
    border-color: var(--accent);
}

.job-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.job-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, var(--accent), var(--accent2));
    border-radius: 4px 0 0 4px;
}

.job-card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(108, 99, 255, 0.15);
}

.match-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 12px;
}

.match-high { background: rgba(72, 199, 116, 0.15); color: #48c774; }
.match-mid { background: rgba(255, 213, 0, 0.15); color: #ffd500; }
.match-low { background: rgba(255, 56, 96, 0.15); color: #ff3860; }

.skill-tag {
    display: inline-block;
    background: rgba(108, 99, 255, 0.12);
    color: var(--accent);
    border: 1px solid rgba(108, 99, 255, 0.3);
    padding: 3px 10px;
    border-radius: 8px;
    font-size: 12px;
    margin: 3px;
}

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 8px;
}

.info-box {
    background: linear-gradient(135deg, rgba(108,99,255,0.08), rgba(255,101,132,0.08));
    border: 1px solid rgba(108, 99, 255, 0.2);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 20px;
}

.divider {
    height: 1px;
    background: var(--border);
    margin: 32px 0;
}

/* Streamlit overrides */
[data-testid="stFileUploader"] {
    background: var(--card) !important;
    border: 2px dashed var(--border) !important;
    border-radius: 16px !important;
    padding: 20px !important;
}

[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent), #8b85ff) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 32px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
}

[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(108, 99, 255, 0.4) !important;
}

.stSelectbox > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
}

.stTextArea textarea {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
}

.stSpinner > div { color: var(--accent) !important; }

[data-testid="stMetric"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

[data-testid="stMetricValue"] { color: var(--accent) !important; }

footer { display: none !important; }
</style>
""", unsafe_allow_html=True)


def extract_text_from_pdf(file_bytes):
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def extract_text_from_docx(file_bytes):
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text_from_txt(file_bytes):
    return file_bytes.decode("utf-8", errors="ignore")


def extract_cv_text(uploaded_file):
    file_bytes = uploaded_file.read()
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    elif name.endswith(".txt"):
        return extract_text_from_txt(file_bytes)
    return ""


def get_job_recommendations(cv_text, job_field, experience_level, location_pref, api_key):
    prompt = f"""You are an expert career advisor and job matching specialist. Analyze the following CV and provide highly personalized job recommendations.

CV CONTENT:
{cv_text}

USER PREFERENCES:
- Preferred Job Field: {job_field}
- Experience Level: {experience_level}
- Location Preference: {location_pref}

Based on this CV, provide exactly 6 job recommendations. Return ONLY a valid JSON array (no markdown, no backticks, no explanation):

[
  {{
    "title": "Job Title",
    "company_type": "Type of company (e.g., Tech Startup, MNC, Government, NGO)",
    "match_score": 92,
    "match_reason": "Why this is a great match in 1-2 sentences",
    "key_skills_matched": ["skill1", "skill2", "skill3"],
    "skills_to_develop": ["skill1", "skill2"],
    "salary_range": "PKR 80,000 - 150,000/month",
    "job_type": "Full-time / Remote / Hybrid",
    "industry": "Industry name",
    "description": "2-3 sentence description of the role",
    "where_to_apply": "LinkedIn, Indeed, Rozee.pk, etc.",
    "apply_links": [
      {{"platform": "LinkedIn", "url": "https://www.linkedin.com/jobs/search/?keywords=Job+Title"}},
      {{"platform": "Rozee.pk", "url": "https://www.rozee.pk/job/jsearch/q/Job+Title"}},
      {{"platform": "Indeed", "url": "https://pk.indeed.com/jobs?q=Job+Title"}}
    ]
  }}
]

For apply_links, generate REAL search URLs by replacing spaces with + in the job title for each platform.
Make recommendations realistic, specific to Pakistan job market if location is Pakistan. Sort by match_score descending.

For apply_links, generate REAL search URLs for each job using these formats:
- LinkedIn: https://www.linkedin.com/jobs/search/?keywords=JOB+TITLE+KEYWORDS
- Rozee.pk: https://www.rozee.pk/job/jsearch/q/JOB+TITLE
- Indeed: https://pk.indeed.com/jobs?q=JOB+TITLE
- Mustakbil: https://www.mustakbil.com/jobs/search/?search=JOB+TITLE
Replace spaces with + in job title for URLs."""

    groq_client = Groq(api_key=api_key)
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=3000,
    )
    response_text = response.choices[0].message.content.strip()
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
    return json.loads(response_text.strip())
def get_cv_summary(cv_text, api_key):
    prompt = f"""Analyze this CV and return ONLY a JSON object (no markdown, no backticks):
{{
  "name": "candidate name or 'Not specified'",
  "top_skills": ["skill1", "skill2", "skill3", "skill4", "skill5"],
  "experience_years": "X years or 'Fresher'",
  "education": "Highest degree",
  "strengths": ["strength1", "strength2", "strength3"],
  "profile_score": 78
}}

CV: {cv_text[:2000]}"""
    groq_client = Groq(api_key=api_key)
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=600,
    )
    text = response.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


# ─── UI ───────────────────────────────────────────────────

st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ AI Powered</div>
    <div class="hero-title">Smart Job<br>Recommender</div>
    <div class="hero-sub">CV upload karo — AI aapke liye perfect jobs dhundega. Pakistan & worldwide opportunities.</div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar: API Key ──
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 16px;">
        <div style="font-family:'Syne',sans-serif; font-size:18px; font-weight:700; color:#e8e8f0; margin-bottom:6px;">⚙️ Settings</div>
        <div style="font-size:12px; color:#7878a0; line-height:1.6;">
            Groq API key daalo — bilkul free hai!<br>
            <a href="https://console.groq.com/keys" target="_blank" style="color:#6c63ff;">console.groq.com/keys</a> se lo
        </div>
    </div>
    """, unsafe_allow_html=True)

    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="console.groq.com/keys se free key lo"
    )

    if groq_api_key:
        st.markdown('<div style="color:#48c774; font-size:13px; margin-top:4px;">✅ Key set ho gayi!</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(108,99,255,0.1); border:1px solid rgba(108,99,255,0.3); border-radius:10px; padding:12px; margin-top:8px; font-size:12px; color:#b0b0c8; line-height:1.7;">
            <strong style="color:#e8e8f0;">Free Key kaise milegi?</strong><br>
            1️⃣ <a href="https://console.groq.com" target="_blank" style="color:#6c63ff;">console.groq.com</a> pe jao<br>
            2️⃣ Sign up karo (free)<br>
            3️⃣ API Keys → Create Key<br>
            4️⃣ <code>gsk_...</code> key copy karo<br>
            5️⃣ Upar box mein paste karo
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-size:11px; color:#3a3a52;">🔒 Key sirf is session mein store hoti hai</div>', unsafe_allow_html=True)

# Main layout
col_left, col_right = st.columns([1, 1.6], gap="large")

with col_left:
    st.markdown('<div class="section-label">📄 Apna CV Upload Karein</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "CV drag & drop karein ya browse karein",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed"
    )

    st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">🎯 Apni Preferences Batayein</div>', unsafe_allow_html=True)

    job_field = st.selectbox(
        "Job Field",
        ["Koi bhi field", "Software Engineering", "Data Science / AI", "Marketing & Digital",
         "Finance & Accounting", "HR & Management", "Design / Creative",
         "Teaching / Education", "Healthcare", "Engineering (Civil/Mech/Elec)",
         "Sales & Business Dev", "Content Writing", "Cybersecurity", "Operations"],
        label_visibility="collapsed"
    )

    exp_level = st.selectbox(
        "Experience Level",
        ["Fresher (0-1 saal)", "Junior (1-3 saal)", "Mid-level (3-5 saal)",
         "Senior (5-8 saal)", "Lead / Manager (8+ saal)"],
        label_visibility="collapsed"
    )

    location = st.selectbox(
        "Location Preference",
        ["Pakistan (Any)", "Karachi", "Lahore", "Islamabad", "Remote / Work from Home",
         "UAE / Gulf", "UK / Europe", "USA / Canada", "Worldwide"],
        label_visibility="collapsed"
    )

    st.markdown('<div style="margin-top: 24px;"></div>', unsafe_allow_html=True)

    # Button disabled if no file OR no api key
    btn_disabled = (uploaded_file is None) or (not groq_api_key)
    analyze_btn = st.button("🚀 Jobs Dhundo", disabled=btn_disabled)

    if not groq_api_key:
        st.markdown("""
        <div class="info-box" style="margin-top: 12px;">
            <div style="font-size:13px; color:#7878a0;">
                👈 <strong style="color:#e8e8f0;">Pehle sidebar mein API key daalo</strong><br>
                Left mein <code>⚙️ Settings</code> panel kholo
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif not uploaded_file:
        st.markdown("""
        <div class="info-box" style="margin-top: 16px;">
            <div style="font-size: 13px; color: #7878a0;">
                💡 <strong style="color: #e8e8f0;">Supported formats:</strong> PDF, DOCX, TXT<br>
                🔒 <strong style="color: #e8e8f0;">Privacy:</strong> CV sirf analysis ke liye use hota hai<br>
                ⚡ <strong style="color: #e8e8f0;">Time:</strong> 10-15 seconds mein results
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    if uploaded_file and analyze_btn:
        with st.spinner("🔍 CV analyze ho raha hai..."):
            cv_text = extract_cv_text(uploaded_file)

        if not cv_text.strip():
            st.error("❌ CV se text extract nahi ho saka. Dobara try karein.")
        else:
            # Profile summary
            with st.spinner("📊 Profile summary ban rahi hai..."):
                try:
                    summary = get_cv_summary(cv_text, groq_api_key)

                    st.markdown('<div class="section-label">👤 Aapka Profile</div>', unsafe_allow_html=True)

                    m1, m2, m3 = st.columns(3)
                    m1.metric("Experience", summary.get("experience_years", "N/A"))
                    m2.metric("Education", summary.get("education", "N/A")[:12])
                    m3.metric("Profile Score", f"{summary.get('profile_score', 0)}%")

                    st.markdown('<div style="margin: 12px 0 4px;"></div>', unsafe_allow_html=True)
                    st.markdown('<div class="section-label">🛠️ Top Skills</div>', unsafe_allow_html=True)
                    skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in summary.get("top_skills", [])])
                    st.markdown(f'<div style="margin-bottom: 8px;">{skills_html}</div>', unsafe_allow_html=True)

                except Exception:
                    pass

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            # Job recommendations
            with st.spinner("💼 Perfect jobs dhundhe ja rahe hain..."):
                try:
                    jobs = get_job_recommendations(cv_text, job_field, exp_level, location, groq_api_key)

                    st.markdown(f'<div class="section-label">✨ {len(jobs)} Recommended Jobs</div>', unsafe_allow_html=True)

                    for i, job in enumerate(jobs):
                        score = job.get("match_score", 0)
                        if score >= 85:
                            badge_class = "match-high"
                            badge_text = f"🔥 {score}% Match"
                        elif score >= 70:
                            badge_class = "match-mid"
                            badge_text = f"⭐ {score}% Match"
                        else:
                            badge_class = "match-low"
                            badge_text = f"💡 {score}% Match"

                        matched_skills = "".join([
                            f'<span class="skill-tag">{s}</span>'
                            for s in job.get("key_skills_matched", [])
                        ])

                        # Skills to develop tags
                        develop_skills = "".join([
                            f'<span style="display:inline-block;background:rgba(255,101,132,0.1);color:#ff6584;border:1px solid rgba(255,101,132,0.3);padding:3px 10px;border-radius:8px;font-size:12px;margin:3px;">{s}</span>'
                            for s in job.get("skills_to_develop", [])
                        ])

                        # Apply buttons HTML
                        apply_links = job.get("apply_links", [])
                        title_query = job.get('title', '').replace(' ', '+')
                        if not apply_links:
                            apply_links = [
                                {"platform": "LinkedIn", "url": f"https://www.linkedin.com/jobs/search/?keywords={title_query}"},
                                {"platform": "Rozee.pk", "url": f"https://www.rozee.pk/job/jsearch/q/{title_query}"},
                                {"platform": "Indeed",   "url": f"https://pk.indeed.com/jobs?q={title_query}"},
                            ]

                        btn_styles = {
                            "LinkedIn":   "background:linear-gradient(135deg,#6c63ff,#8b85ff)",
                            "Rozee.pk":   "background:linear-gradient(135deg,#0f6e56,#1d9e75)",
                            "Indeed":     "background:linear-gradient(135deg,#185fa5,#378add)",
                            "Mustakbil":  "background:linear-gradient(135deg,#854f0b,#ef9f27)",
                            "Glassdoor":  "background:linear-gradient(135deg,#3b6d11,#639922)",
                            "Bayt":       "background:linear-gradient(135deg,#993556,#d4537e)",
                        }
                        platform_icons = {"LinkedIn":"💼","Rozee.pk":"🇵🇰","Indeed":"🔍","Mustakbil":"📋","Glassdoor":"🌟","Bayt":"🌍"}

                        apply_btns_html = ""
                        for lnk in apply_links:
                            pl   = lnk.get("platform", "Apply")
                            url  = lnk.get("url", "#")
                            icon = platform_icons.get(pl, "🔗")
                            sty  = btn_styles.get(pl, "background:linear-gradient(135deg,#6c63ff,#8b85ff)")
                            apply_btns_html += f'''<a href="{url}" target="_blank" style="{sty};color:white;padding:9px 16px;border-radius:10px;text-decoration:none;font-size:13px;font-weight:600;font-family:Syne,sans-serif;">{icon} {pl}</a>'''

                        st.markdown(f"""
                        <div class="job-card">
                            <span class="match-badge {badge_class}">{badge_text}</span>
                            <h3 style="margin:0 0 4px;font-size:1.1rem;font-family:'Syne',sans-serif;">{job.get('title','')}</h3>
                            <div style="color:#7878a0;font-size:13px;margin-bottom:12px;">
                                🏢 {job.get('company_type','')} &nbsp;•&nbsp;
                                💰 {job.get('salary_range','')} &nbsp;•&nbsp;
                                📍 {job.get('job_type','')}
                            </div>
                            <p style="color:#b0b0c8;font-size:13px;margin-bottom:12px;line-height:1.6;">
                                {job.get('description','')}
                            </p>
                            <div style="margin-bottom:8px;">
                                <span style="font-size:11px;color:#7878a0;text-transform:uppercase;letter-spacing:1px;">✅ Matched Skills</span><br>
                                {matched_skills}
                            </div>
                            {"<div style='margin-bottom:10px;'><span style='font-size:11px;color:#7878a0;text-transform:uppercase;letter-spacing:1px;'>📈 Seekhne wali Skills</span><br>" + develop_skills + "</div>" if develop_skills else ""}
                            <div style="font-size:12px;color:#7878a0;margin-top:8px;padding-top:8px;border-top:1px solid #2a2a3d;">
                                💡 <em style="color:#b0b0c8;">{job.get('match_reason','')}</em>
                            </div>
                            <div style="display:flex;gap:10px;margin-top:14px;flex-wrap:wrap;">
                                {apply_btns_html}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)



                except json.JSONDecodeError:
                    st.error("❌ Results parse karne mein error. Dobara try karein.")
                except Exception as e:
                    st.error(f"❌ Kuch masla aaya: {str(e)}")

    elif not uploaded_file:
        st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 400px; text-align: center;">
            <div style="font-size: 64px; margin-bottom: 20px;">💼</div>
            <div style="font-family: 'Syne', sans-serif; font-size: 1.4rem; color: #e8e8f0; margin-bottom: 12px;">CV Upload Karein</div>
            <div style="color: #7878a0; font-size: 14px; max-width: 300px; line-height: 1.6;">
                Left side se apna CV upload karein aur AI aapke liye best jobs recommend karega
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 40px 0 20px; color: #3a3a52; font-size: 12px;">
    Built with ❤️ using Claude AI & Streamlit &nbsp;•&nbsp; Pakistan Jobs & Beyond
</div>
""", unsafe_allow_html=True)
