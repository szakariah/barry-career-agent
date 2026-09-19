import streamlit as st
from google import genai

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Barry King | Executive Career Agent",
    page_icon="💼",
    layout="wide"
)

# --- INITIALIZE GEMINI CLIENT ---
@st.cache_resource
def get_gemini_client():
    # Pulls the API key securely from Streamlit Secrets
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

try:
    client = get_gemini_client()
except Exception as e:
    st.error("⚠️ Gemini API Key missing or invalid. Please check your Streamlit Secrets.")

# --- EMBEDDED RESUME DATA (BARRY KOFI KING) ---
BARRY_RESUME_CONTEXT = """
BARRY KOFI KING - Senior People Strategy & Organisational Transformation Executive
Credentials: MBA (Thunderbird), SHRM-SCP, MCIPD, CPHR, PMP, MCIHRMP.
Experience: 17+ years across 30+ African markets, workforces exceeding 13,000 employees.

Key Achievements & Roles:
1. Head of People - WaterAid Ghana (June 2025 - Present):
   - Executive Committee member, strategic HR partnership, workforce strategy, governance.
   - Acted as Country Director during leadership cover. Redesigned People Policy Manual.
2. Deputy Lead, Centralized Performance Management - Ecobank Group (2021 - 2025):
   - Co-led enterprise performance governance across 30+ markets and 13,000+ employees.
   - Translated enterprise performance requirements into Oracle HCM deployment.
3. Senior HR Business Partner, West Africa - Ecobank Ghana (2021 - 2025):
   - HR Business Partner to Corporate & Investment Banking (CIB) contributing 60%+ of bank revenue.
   - Job architecture across 218 unique roles; performance normalization for 1,255 scorecards.
4. Commercial & Early Career Roots (2007 - 2013):
   - E-Banking Sales & Support, Digital Financial Services, VISA revenue growth (16%).
   - Unique commercial mindset bridging business revenue with HR strategy.
"""

# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("🎯 Target Role Setup")
st.sidebar.markdown("Configure your target parameters to customize all AI outputs.")

target_sector = st.sidebar.selectbox(
    "Target Industry / Sector",
    [
        "FinTech & Digital Banking",
        "Pan-African Enterprise Banking",
        "Global NGO & International Development",
        "Multinational Technology / Remote",
        "Custom / Other"
    ]
)

target_role = st.sidebar.text_input("Target Job Title", value="Chief Human Resources Officer (CHRO)")
target_location = st.sidebar.selectbox("Location Preference", ["Accra / Hybrid", "Pan-African / Regional", "Global Remote (USD)"])
target_salary = st.sidebar.slider("Target Total Compensation (USD)", min_value=80000, max_value=300000, value=150000, step=10000)

st.sidebar.markdown("---")
st.sidebar.subheader("Pillars to Emphasize")
emp_commercial = st.sidebar.checkbox("Commercial Sales & E-Banking Growth (VISA/CIB)", value=True)
emp_oracle = st.sidebar.checkbox("Oracle HCM & 30+ Markets Scale (13k+ staff)", value=True)
emp_governance = st.sidebar.checkbox("Job Architecture (218 roles) & Policy Redesign", value=True)
emp_csuite = st.sidebar.checkbox("Board Advisory & Acting Country Director Experience", value=True)

# --- MAIN INTERFACE ---
st.title("💼 Executive Career Agent (Powered by Gemini)")
st.caption(f"Configured for: **{target_role}** in **{target_sector}** ({target_location})")

tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Executive Asset Generator", 
    "🔍 Job Description Tailoring", 
    "🎙️ Board Interview Simulator", 
    "💰 Compensation Negotiator"
])

# --- TAB 1: EXECUTIVE ASSET GENERATOR ---
with tab1:
    st.header("Generate Core C-Suite Assets")
    st.write("Generate high-impact messaging optimized for board members, executive search firms, and CEOs.")
    
    asset_type = st.selectbox("Select Asset to Generate", [
        "Executive LinkedIn / Bio Pitch (3 Sentences)",
        "Executive Value Proposition Matrix (Commercial vs HR)",
        "90-Day Executive Transition Strategy",
        "Tailored C-Suite Resume Summary"
    ])
    
    if st.button("🚀 Generate Asset with Gemini"):
        with st.spinner("Gemini is engineering your executive narrative..."):
            prompt = f"""
            You are an executive career strategist for C-suite leaders.
            Candidate Context:
            {BARRY_RESUME_CONTEXT}
            
            Target Parameters:
            - Industry: {target_sector}
            - Target Role: {target_role}
            - Location: {target_location}
            - Desired Pay: ${target_salary:,}
            - Emphasize Focus Areas: Commercial={emp_commercial}, Scale={emp_oracle}, Governance={emp_governance}, C-Suite={emp_csuite}
            
            Task: Write a polished, professional '{asset_type}' tailored specifically for these parameters.
            Highlight Barry's rare fusion of commercial sales roots and enterprise HR scale across 30+ markets.
            """
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            
            st.success("Asset Generated Successfully!")
            st.markdown(f"### {asset_type}")
            st.markdown(response.text)

# --- TAB 2: JOB DESCRIPTION TAILORING ---
with tab2:
    st.header("Tailor Portfolio to Active Job Openings")
    jd_input = st.text_area("Paste Active Job Description / Board Brief Here:", height=200)
    
    if st.button("⚡ Analyze Alignment & Draft Cover Letter"):
        if jd_input:
            with st.spinner("Gemini is analyzing role alignment..."):
                prompt = f"""
                Act as an Executive Recruiter. Analyze this job description against Barry Kofi King's resume.
                
                Candidate Resume:
                {BARRY_RESUME_CONTEXT}
                
                Job Description:
                {jd_input}
                
                Provide:
                1. A brief "Match Rating" (Percentage & top 3 alignment points).
                2. A bespoke C-Suite Cover Letter addressed to the Hiring Board/CEO linking Barry's background directly to the job requirements.
                """
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                
                st.markdown(response.text)
        else:
            st.warning("Please paste a job description first.")

# --- TAB 3: MOCK INTERVIEW SIMULATOR ---
with tab3:
    st.header("Boardroom & Executive Interview Prep")
    st.write("Practice high-stakes questions tailored to your target role.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"Welcome Barry. I am the Board Chair hiring for the {target_role} position in the {target_sector} space. To start, how does your background in commercial sales and E-Banking give you an edge over traditional HR leaders?"}
        ]
        
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
        
    if user_input := st.chat_input("Type your response to the Board Chair..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        # Build chat history for Gemini
        conversation_history = f"""
        System Persona: You are a sharp, analytical Board Chairman interviewing Barry Kofi King for a {target_role} role. 
        Evaluate his answer briefy, then ask the next high-stakes follow-up question.
        
        Candidate Context:
        {BARRY_RESUME_CONTEXT}
        
        Conversation history:
        """
        for m in st.session_state.messages:
            conversation_history += f"\n{m['role'].upper()}: {m['content']}"
            
        with st.spinner("Board Chair is evaluating..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=conversation_history
            )
            
            ai_reply = response.text
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            st.chat_message("assistant").write(ai_reply)

# --- TAB 4: COMPENSATION NEGOTIATOR ---
with tab4:
    st.header("Total Rewards & Counter-Offer Engine")
    
    col_a, col_b = st.columns(2)
    with col_a:
        offered_base = st.number_input("Offered Base Salary (USD)", value=110000)
        offered_bonus = st.number_input("Offered Annual Bonus / STI (USD)", value=15000)
    with col_b:
        offered_allowances = st.number_input("Offered Allowances (USD)", value=10000)
        target_increase = st.slider("Target Counter-Offer Increase (%)", 10, 40, 20)
        
    total_offered = offered_base + offered_bonus + offered_allowances
    counter_target = total_offered * (1 + target_increase / 100)
    
    st.metric("Total Offered Package", f"${total_offered:,.2f}")
    st.metric("Recommended Counter-Offer Target", f"${counter_target:,.2f}", delta=f"+${counter_target - total_offered:,.2f}")
    
    if st.button("✉️ Draft Gemini Counter-Offer Email"):
        with st.spinner("Gemini is calculating leverage and drafting negotiation strategy..."):
            prompt = f"""
            Act as an Executive Compensation Negotiator. 
            Draft a counter-offer email from Barry Kofi King to a hiring committee for a {target_role} role.
            
            Details:
            - Current Offer: Base ${offered_base:,}, Bonus ${offered_bonus:,}, Allowances ${offered_allowances:,} (Total: ${total_offered:,})
            - Target Counter-Offer Total: ${counter_target:,}
            - Key Selling Points to Leverage: 17+ years experience across 30+ markets, MBA, SHRM-SCP, MCIPD, past track record managing 13,000+ employees and driving revenue.
            
            Draft a high-leverage, highly professional email requesting this adjustment while reinforcing Barry's high ROI.
            """
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            
            st.markdown(response.text)
