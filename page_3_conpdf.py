import streamlit as st
import pandas as pd
from model_streamlit import train_model, evaluate_model, predict
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Funzione per preprocessare i dati
def preprocess_data(raw_data):
    # Standardizza i nomi delle colonne (minuscolo e rimozione spazi)
    raw_data.columns = raw_data.columns.str.strip().str.lower()
    
    # Se esiste la colonna 'gender', applica il dummy encoding
    if 'gender' in raw_data.columns:
        processed_data = pd.get_dummies(raw_data, columns=['gender'])
    else:
        processed_data = pd.get_dummies(raw_data)
    
    return processed_data

def create_pdf_report(accuracy, log_loss_value, precision, recall, f1, report_text, df_results):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --- First Page: Evaluation Metrics ---
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, "Model evaluation report")

    p.setFont("Helvetica", 12)
    y = height - 100
    p.drawString(50, y, f"Accuracy: {accuracy:.2f}")
    y -= 20
    p.drawString(50, y, f"Log Loss: {log_loss_value:.2f}")
    y -= 20
    p.drawString(50, y, f"Precision: {precision:.2f}")
    y -= 20
    p.drawString(50, y, f"Recall: {recall:.2f}")
    y -= 20
    p.drawString(50, y, f"F1 Score: {f1:.2f}")
    y -= 30

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Classification Report:")
    y -= 20
    p.setFont("Helvetica", 10)
    for line in report_text.split("\n"):
        p.drawString(50, y, line)
        y -= 12
        if y < 50:
            p.showPage()
            y = height - 50

    # --- Second Page: Prediction Results ---
    p.showPage()
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, "Predicted results")
    p.setFont("Helvetica", 12)
    y = height - 100
    for index, prediction in enumerate(df_results['predicted_disease']):
        sample_id = df_results['id'].iloc[index]
        if prediction == 1:
            result_text = f"Sample ID {sample_id}: Adipose tissue is predicted to be lipedema."
        else:
            result_text = f"Sample ID {sample_id}: Adipose tissue is predicted to be healthy."
        p.drawString(50, y, result_text)
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 50

    p.save()
    buffer.seek(0)
    return buffer.getvalue()

# Titolo e descrizione dell'applicazione
st.title("Upload your sample")
st.write("On this page you can upload your sample data.")

st.subheader("Upload an Excel file with sample data")
st.write(
    "Upload an Excel file with your data."
    "The data will be analyzed by our machine learning model, and upon completion, "
    "each sample will be predicted as **sick** or **healthy**."
)

st.write(
    "The Excel file should contain 32 columns, each row representing a sample. "
    "You can view and download an example file below:"
)

# Visualizza il file di esempio
excel_file = "test_data.xlsx"  # Aggiorna il path se necessario
df_example = pd.read_excel(excel_file, sheet_name=0)
st.dataframe(df_example)

# Widget per caricare il file Excel
uploaded_file = st.file_uploader("Scegli un file Excel", type="xlsx")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name=0)
    df.columns = df.columns.str.strip().str.lower()
    st.write("Anteprima dei dati:")
    st.dataframe(df)
    num_rows, num_columns = df.shape
    st.write(f"Il dataset contiene {num_rows} righe e {num_columns} colonne.")
    
    # Salva il file caricato nello session state per usarlo nella pagina successiva
    st.session_state.df = df

# Carica i dati raw per il training
raw_data = pd.read_excel("raw_data.xlsx")
raw_data.columns = raw_data.columns.str.strip().str.lower()

if 'df' in st.session_state:
    df = st.session_state.df
    
    # Preprocessa i dati raw e quelli di valutazione
    new_raw_data = preprocess_data(raw_data)
    
    # Applica il dummy encoding su 'gender' se presente, altrimenti su tutte le colonne categoriche
    if 'gender' in df.columns:
        df = pd.get_dummies(df, columns=['gender'])
    else:
        st.write("La colonna 'gender' manca dai dati caricati.")
        df = pd.get_dummies(df)
    
    # Assicura la consistenza tra le colonne dummy dei dati raw e quelli caricati
    missing_cols = set(new_raw_data.columns) - set(df.columns)
    for col in missing_cols:
        df[col] = 0
    df = df[new_raw_data.columns.drop('disease')]
    
    # Prepara i dati per il training
    X = new_raw_data.drop(['id', 'disease'], axis=1).values
    y = new_raw_data['disease']
    
    # Allena il modello
    clf = train_model(X, y)
    
    # Valuta il modello
    accuracy, log_loss_value, precision, recall, f1, report = evaluate_model(clf, X, y)
    st.write(f'Accuracy: {accuracy}')
    st.write(f'Log Loss: {log_loss_value}')
    st.write(f'Precision: {precision}')
    st.write(f'Recall: {recall}')
    st.write(f'F1 Score: {f1}')
    st.text(report)
    
    # Prepara il dataset di valutazione e fai la predizione
    new_evaluation_data = df
    X_test = new_evaluation_data.drop(['id'], axis=1).values
    y_test_pred = predict(clf, X_test)
    df['predicted_disease'] = y_test_pred

    # Mostra i risultati predetti
    st.write("Results:")
    for index, prediction in enumerate(df['predicted_disease']):
        sample_id = df['id'].iloc[index]
        if prediction == 1:
            st.write(f"Sample ID {sample_id}: The adipose tissue is predicted to be **lipedema**.")
        else:
            st.write(f"Sample ID {sample_id}: The adipose tissue is predicted to be **healthy**.")
    
    # Bottone per generare e scaricare il report PDF
    if st.button("Press the button to create a PDF report."):
        pdf_data = create_pdf_report(accuracy, log_loss_value, precision, recall, f1, report, df)
        st.download_button(
            label="Download PDF Report",
            data=pdf_data,
            file_name="report.pdf",
            mime="application/pdf"
        )
