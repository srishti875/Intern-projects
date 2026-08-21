import streamlit as st

st.set_page_config(
    page_title="Formal Application Form",
    page_icon="📋",
    layout="centered"
)

# Inject custom CSS for a beautiful, formal background and styling
st.markdown("""
    <style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Form container styling */
    .div-form {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #e0e0e0;
    }
    
    /* Header customization */
    h1 {
        color: #1e3a8a;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Label font styling */
    label {
        font-weight: 600 !important;
        color: #334155 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Form Title
st.markdown("<h1>Registration Form</h1>", unsafe_allow_html=True)

# Wrap form elements in a container for styling
with st.container():
    # Create the form
    with st.form(key="application_form", clear_on_submit=True):
        
        # Name Input
        name = st.text_input("Full Name", placeholder="John Doe")
        
        # Gender Selection
        gender = st.selectbox(
            "Gender",
            options=["Select your gender", "Male", "Female", "Non-binary", "Prefer not to say"]
        )
        
        # Age Input
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        
        # Course Type Selection
        course_type = st.radio(
            "Course Type",
            options=["Full-Time", "Part-Time", "Online / Distance Learning", "Weekend Bootcamp"]
        )
        
        # Statement of Interest
        interest_reason = st.text_area(
            "Why are you interested in this?",
            placeholder="Please describe your motivations and goals for this course..."
        )
        
        # Submit Button
        submit_button = st.form_submit_button(label="Submit Application")
        
    # Form submission logic
    if submit_button:
        # Validation checks
        if not name.strip():
            st.error("Please enter your name.")
        elif gender == "Select your gender":
            st.error("Please select your gender.")
        elif not interest_reason.strip():
            st.error("Please let us know why you are interested.")
        else:
            # Success confirmation message
            st.success("Submit Successfully!")
            
            # Optional: Display submitted data back to the user neatly
            with st.expander("View Submitted Details"):
                st.write(f"**Name:** {name}")
                st.write(f"**Gender:** {gender}")
                st.write(f"**Age:** {age}")
                st.write(f"**Course Type:** {course_type}")
                st.write(f"**Reason for Interest:** {interest_reason}")