import streamlit as st
import base64


# Define a function to load and encode the image in base64
def load_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Load your logo image
logo_base64 = load_image_as_base64("logo MAGI GROUP.png")  # Update the path accordingly


# Define pages
pages = {
    "Introduction": "page_1",
    "Dataset": "page_2",
    "Upload your sample": "page_3_conpdf",
#    "Explanation of the mathematical model": "page_4.5",
    "Collaborators": "page_5"
}

# Sidebar for navigation
st.sidebar.title("Machine learning in Lipedema: Index")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Load the selected page
page_file = pages[selection]
with open(f"{page_file}.py") as f:
    exec(f.read())

# Footer banner with logo and contact information
st.markdown(
    f"""
    <style>
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: #333;
        text-align: center;
        padding: 10px;
        font-size: 1.2em;
    }}
    .footer img {{
        height: 50px;
        vertical-align: middle;
        margin-right: 10px;
    }}
    </style>
    <div class="footer">
        <img src="data:image/png;base64,{logo_base64}" alt="Company Logo">
        <span>Contact us at: <strong>+39 0365.62.061</strong></span>
        <span> or at the email: <strong>matteo.bertelli@assomagi.org</strong></span>
    </div>
    """,
    unsafe_allow_html=True
)