import streamlit as st
import pandas as pd
import joblib

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Performance AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# LOAD MODEL
# ============================================================

try:
    model = joblib.load("student_performance_model.pkl")
except FileNotFoundError:
    st.error(
        "❌ Model file not found.\n\n"
        "Make sure `student_performance_model.pkl` is in the same "
        "folder as `app.py`."
    )
    st.stop()

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #777777;
        margin-bottom: 25px;
    }

    .student-name {
        font-size: 22px;
        font-weight: 600;
        text-align: center;
        margin-bottom: 20px;
    }

    .study-info {
        padding: 12px;
        border-radius: 10px;
        background-color: #f0f6ff;
        margin-top: 5px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎓 Student Performance AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered early prediction of student final performance'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "🧠 Early Prediction Mode: G1 and G2 are intentionally excluded. "
    "The model predicts the final grade using information available earlier "
    "in the student's academic life."
)

# ============================================================
# STUDENT NAME
# ============================================================

st.header("👤 Student Information")

student_name = st.text_input(
    "Student Name",
    placeholder="Enter student's full name",
    max_chars=100
)

if student_name.strip():
    st.markdown(
        f'<div class="student-name">Student: {student_name.strip()}</div>',
        unsafe_allow_html=True
    )

# ============================================================
# BASIC STUDENT INFORMATION
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    sex = st.selectbox(
        "Gender",
        ["F", "M"]
    )

    age = st.slider(
        "Age",
        min_value=15,
        max_value=22,
        value=17
    )

    address = st.selectbox(
        "Area",
        ["U", "R"],
        format_func=lambda x:
            "Urban" if x == "U" else "Rural"
    )

    famsize = st.selectbox(
        "Family Size",
        ["GT3", "LE3"],
        format_func=lambda x:
            "More than 3 members" if x == "GT3"
            else "3 or fewer members"
    )

    Pstatus = st.selectbox(
        "Parent Status",
        ["A", "T"],
        format_func=lambda x:
            "Apart" if x == "A"
            else "Living together"
    )

with col2:

    Medu = st.slider(
        "Mother's Education Level",
        min_value=0,
        max_value=4,
        value=2,
        help=(
            "0 = none, 1 = primary education, "
            "2 = 5th–9th grade, 3 = secondary education, "
            "4 = higher education"
        )
    )

    Fedu = st.slider(
        "Father's Education Level",
        min_value=0,
        max_value=4,
        value=2,
        help=(
            "0 = none, 1 = primary education, "
            "2 = 5th–9th grade, 3 = secondary education, "
            "4 = higher education"
        )
    )

    Mjob = st.selectbox(
        "Mother's Job",
        ["teacher", "health", "services", "at_home", "other"]
    )

    Fjob = st.selectbox(
        "Father's Job",
        ["teacher", "health", "services", "at_home", "other"]
    )

with col3:

    reason = st.selectbox(
        "Reason for Choosing School",
        ["course", "home", "reputation", "other"]
    )

    guardian = st.selectbox(
        "Main Guardian",
        ["mother", "father", "other"]
    )

    traveltime = st.slider(
        "Travel Time to School",
        min_value=1,
        max_value=4,
        value=2,
        help=(
            "1 = less than 15 min, "
            "2 = 15–30 min, "
            "3 = 30–60 min, "
            "4 = more than 60 min"
        )
    )

    failures = st.slider(
        "Previous Class Failures",
        min_value=0,
        max_value=3,
        value=0
    )

# ============================================================
# STUDY HABITS
# ============================================================

st.header("📚 Study & Academic Habits")

study_col1, study_col2, study_col3 = st.columns(3)

with study_col1:

    studytime = st.slider(
        "Weekly Study Time",
        min_value=1,
        max_value=4,
        value=2,
        help=(
            "1 = less than 2 hours/week, "
            "2 = 2–5 hours/week, "
            "3 = 5–10 hours/week, "
            "4 = more than 10 hours/week"
        )
    )

with study_col2:

    study_hours = {
        1: "< 2 hours/week",
        2: "2–5 hours/week",
        3: "5–10 hours/week",
        4: "> 10 hours/week"
    }

    st.markdown(
        f"""
        <div class="study-info">
        📖 <b>Study-time interpretation:</b><br>
        {study_hours[studytime]}
        </div>
        """,
        unsafe_allow_html=True
    )

with study_col3:

    absences = st.number_input(
        "Number of Absences",
        min_value=0,
        max_value=100,
        value=4,
        step=1
    )

# ============================================================
# EDUCATIONAL SUPPORT
# ============================================================

st.header("🏫 Educational Support")

support1, support2, support3 = st.columns(3)

with support1:

    schoolsup = st.selectbox(
        "Extra School Support",
        ["yes", "no"]
    )

with support2:

    famsup = st.selectbox(
        "Family Educational Support",
        ["yes", "no"]
    )

with support3:

    paid = st.selectbox(
        "Extra Paid Classes",
        ["yes", "no"]
    )

# ============================================================
# ACTIVITIES & TECHNOLOGY
# ============================================================

st.header("🌐 Activities & Technology")

activity1, activity2, activity3 = st.columns(3)

with activity1:

    activities = st.selectbox(
        "Extra-Curricular Activities",
        ["yes", "no"]
    )

with activity2:

    internet = st.selectbox(
        "Internet Access",
        ["yes", "no"]
    )

with activity3:

    romantic = st.selectbox(
        "Romantic Relationship",
        ["yes", "no"]
    )

# ============================================================
# LIFESTYLE
# ============================================================

st.header("📊 Lifestyle & Well-being")

life1, life2, life3 = st.columns(3)

with life1:

    famrel = st.slider(
        "Family Relationship Quality",
        min_value=1,
        max_value=5,
        value=4
    )

with life2:

    freetime = st.slider(
        "Free Time",
        min_value=1,
        max_value=5,
        value=3
    )

with life3:

    goout = st.slider(
        "Going Out With Friends",
        min_value=1,
        max_value=5,
        value=3
    )

life4, life5, life6 = st.columns(3)

with life4:

    Dalc = st.slider(
        "Weekday Alcohol Consumption",
        min_value=1,
        max_value=5,
        value=1
    )

with life5:

    Walc = st.slider(
        "Weekend Alcohol Consumption",
        min_value=1,
        max_value=5,
        value=1
    )

with life6:

    health = st.slider(
        "Current Health",
        min_value=1,
        max_value=5,
        value=3
    )

# ============================================================
# PREDICTION BUTTON
# ============================================================

st.divider()

predict_button = st.button(
    "🔮 Predict Student Performance",
    type="primary",
    use_container_width=True
)

# ============================================================
# PREDICTION
# ============================================================

if predict_button:

    # --------------------------------------------------------
    # NAME VALIDATION
    # --------------------------------------------------------

    if not student_name.strip():

        st.error(
            "⚠️ Please enter the student's name before predicting."
        )

        st.stop()

    # --------------------------------------------------------
    # CREATE INPUT DATA
    # --------------------------------------------------------

    student = pd.DataFrame([{

        "sex": sex,
        "age": age,
        "address": address,
        "famsize": famsize,
        "Pstatus": Pstatus,
        "Medu": Medu,
        "Fedu": Fedu,
        "Mjob": Mjob,
        "Fjob": Fjob,
        "reason": reason,
        "guardian": guardian,
        "traveltime": traveltime,

        # IMPORTANT:
        # studytime must be included because the model
        # was trained using this feature.
        "studytime": studytime,

        "failures": failures,
        "schoolsup": schoolsup,
        "famsup": famsup,
        "paid": paid,
        "activities": activities,

        "internet": internet,

        "romantic": romantic,
        "famrel": famrel,
        "freetime": freetime,
        "goout": goout,
        "Dalc": Dalc,
        "Walc": Walc,
        "health": health,
        "absences": absences

    }])

    # --------------------------------------------------------
    # MAKE PREDICTION
    # --------------------------------------------------------

    try:

        prediction = model.predict(student)[0]

    except Exception as e:

        st.error("❌ Prediction error.")

        st.code(str(e))

        st.warning(
            "This usually means that `train_model.py` and `app.py` "
            "are using different input columns. Retrain the model "
            "using the matching training code."
        )

        st.stop()

    # --------------------------------------------------------
    # LIMIT RESULT TO 0–20
    # --------------------------------------------------------

    prediction = float(prediction)

    prediction = max(
        0.0,
        min(20.0, prediction)
    )

    # --------------------------------------------------------
    # PERCENTAGE
    # --------------------------------------------------------

    progress = int(
        round((prediction / 20) * 100)
    )

    # --------------------------------------------------------
    # PERFORMANCE CATEGORY
    # --------------------------------------------------------

    if prediction < 8:

        category = "🔴 At Risk"

        recommendation = (
            "The predicted performance is below the satisfactory range. "
            "The student should focus on increasing study consistency, "
            "reducing unnecessary absences and using available academic "
            "support."
        )

    elif prediction < 10:

        category = "🟠 Needs Improvement"

        recommendation = (
            "The student has room for improvement. Increasing study time "
            "and maintaining regular attendance may help improve the "
            "predicted final result."
        )

    elif prediction < 14:

        category = "🟡 Average"

        recommendation = (
            "The student is predicted to perform at an average level. "
            "Consistent study habits and maintaining good attendance "
            "could help improve the final result."
        )

    elif prediction < 17:

        category = "🟢 Good"

        recommendation = (
            "The student shows good predicted academic performance. "
            "Maintaining consistent study habits and attendance should "
            "help sustain this level."
        )

    else:

        category = "🔵 Excellent"

        recommendation = (
            "The student shows strong predicted performance. "
            "Maintaining the current academic habits is recommended."
        )

    # ========================================================
    # RESULTS
    # ========================================================

    st.divider()

    st.header("📈 Prediction Results")

    st.markdown(
        f"""
        <div class="student-name">
        🎓 Prediction for {student_name.strip()}
        </div>
        """,
        unsafe_allow_html=True
    )

    result1, result2 = st.columns(2)

    with result1:

        st.metric(
            "Predicted Final Grade",
            f"{prediction:.1f} / 20"
        )

    with result2:

        st.metric(
            "Performance Level",
            category
        )

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    st.subheader("📊 Performance Score")

    st.progress(progress)

    st.write(
        f"**Predicted performance: {progress}% "
        f"of the maximum grade**"
    )

    # --------------------------------------------------------
    # AI RECOMMENDATION
    # --------------------------------------------------------

    st.header("💡 AI Recommendations")

    st.success(recommendation)

    # ========================================================
    # STUDENT INSIGHTS
    # ========================================================

    st.header("🔍 Student Insights")

    insight1, insight2, insight3 = st.columns(3)

    # --------------------------------------------------------
    # STUDY INSIGHT
    # --------------------------------------------------------

    with insight1:

        if studytime == 4:

            st.success(
                "📚 Very high study-time input"
            )

        elif studytime == 3:

            st.success(
                "📚 Good study-time input"
            )

        else:

            st.warning(
                "📚 Study time could be increased"
            )

    # --------------------------------------------------------
    # ATTENDANCE INSIGHT
    # --------------------------------------------------------

    with insight2:

        if absences <= 5:

            st.success(
                "🏫 Very good attendance"
            )

        elif absences <= 10:

            st.success(
                "🏫 Absence level is relatively low"
            )

        elif absences <= 20:

            st.warning(
                "🏫 Attendance could be improved"
            )

        else:

            st.error(
                "🏫 High number of absences"
            )

    # --------------------------------------------------------
    # FAILURE INSIGHT
    # --------------------------------------------------------

    with insight3:

        if failures == 0:

            st.success(
                "🎯 No previous class failures"
            )

        elif failures == 1:

            st.warning(
                "⚠️ One previous class failure"
            )

        else:

            st.error(
                f"⚠️ {failures} previous class failures"
            )

    # ========================================================
    # ADDITIONAL INSIGHTS
    # ========================================================

    st.subheader("📋 Additional Analysis")

    extra1, extra2, extra3 = st.columns(3)

    with extra1:

        if internet == "yes":

            st.success(
                "🌐 Internet access available"
            )

        else:

            st.warning(
                "🌐 No internet access"
            )

    with extra2:

        if famsup == "yes":

            st.success(
                "👨‍👩‍👧 Family educational support available"
            )

        else:

            st.info(
                "👨‍👩‍👧 No family educational support selected"
            )

    with extra3:

        if schoolsup == "yes":

            st.success(
                "🏫 Additional school support available"
            )

        else:

            st.info(
                "🏫 No additional school support selected"
            )

# ============================================================
# ABOUT PROJECT
# ============================================================

st.divider()

with st.expander("ℹ️ About This Project"):

    st.write(
        """
        **Student Performance AI** is a machine-learning application
        designed to estimate a student's final academic performance.

        The model is based on the UCI Student Performance dataset and
        predicts the student's final grade on a scale from 0 to 20.

        ### Early Prediction

        G1 and G2 are intentionally excluded from this application.
        This means the system attempts to make the prediction using
        information that can be available before the student's final
        grades are known.

        ### Important

        The student's name is used only for displaying the prediction
        result. It is not sent to the machine-learning model.

        The application runs locally when started with:

        `streamlit run app.py`

        Therefore, opening `http://localhost:8501` means the application
        is running on your own computer.
        """
    )