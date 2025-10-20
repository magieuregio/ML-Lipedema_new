import streamlit as st

st.title("Introduction: Machine Learning and Lipedema")
st.markdown(
    """
    <p style="text-align: justify;">
    Machine learning (ML) is revolutionizing many areas of healthcare, and its application in lipedema research is particularly promising. 
    Lipedema is a chronic condition characterized by abnormal fat accumulation, primarily in the legs and arms, which is often resistant to conventional weight loss methods. 
    This condition frequently causes significant physical and emotional distress for those affected. 
    Traditional diagnostic and treatment approaches have limitations, and ML can offer transformative improvements.
    </p>
    """,
    unsafe_allow_html=True
)

st.subheader("Our project in a nutshell")
st.markdown(
    """
    <p style="text-align: justify;">
    Our project focuses on analyzing and distinguishing between lipedema tissue and healthy adipose tissue using metabolomic and proteomic analysis. 
    Tissue samples from lipedema patients and healthy individuals are collected, and both types undergo extensive analysis to identify unique biomarkers and molecular characteristics. 
    Clinical data from patients are integrated with these findings, forming a comprehensive dataset and a control dataset, with the potential inclusion of a synthetic dataset to enhance model training and validation. 
    The project involves initial data understanding through exploratory analysis, followed by data preparation to clean and normalize the data for ML applications. 
    Using tools like TensorFlow and Scikit-Learn, ML models are developed to analyze the data, aiming to identify patterns, classify tissue types, or predict outcomes. 
    The models are then rigorously assessed and evaluated for accuracy and effectiveness. 
    Key tools used include Pandas for data manipulation, Matplotlib for visualization, and ML frameworks for model development, all working towards a better understanding of lipedema, potentially leading to improved diagnostics and treatments.
    </p>
    """,
    unsafe_allow_html=True
)
st.image("Project scheme.png", caption="Project scheme", use_column_width=True)

