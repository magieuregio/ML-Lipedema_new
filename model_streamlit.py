"""
Funzioni di training / valutazione / inferenza
ricavate dal notebook ML Class 2-Copy1.ipynb
"""
import numpy as np
import pandas as pd
from sklearn.utils import resample
from xgboost import XGBClassifier
from sklearn.metrics import (accuracy_score, log_loss,
                             precision_score, recall_score,
                             f1_score, classification_report)

# ---------------------------------------------------------------------
#  PRE-PROCESSING
# ---------------------------------------------------------------------
def preprocess(df: pd.DataFrame,
               *, drop_noise_cols=True,
               add_noise: bool = True,
               noise_std: float = 2.2,
               random_state: int = 42):
    """
    - converte i nomi colonna in minuscolo e toglie spazi
    - dummifica 'gender' (se presente)
    - preserva la colonna 'id' per i report finali
    - rimuove le colonne 'age', 'gender_*' (come nel notebook)
    - opzionale: inietta rumore gaussiano (σ = noise_std)
    Ritorna: X (np.ndarray), y (Series o None), feature_names
    """
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    if 'gender' in df.columns:
        df = pd.get_dummies(df, columns=['gender'])

    # isola y se presente
    y = None
    if 'disease' in df.columns:
        y = df['disease']
        df = df.drop(columns=['disease'])

    # opzionale: drop colonne poco utili / sensibili
    if drop_noise_cols:
        df = df.drop(columns=['age', 'gender_f', 'gender_m'], errors='ignore')

    # mantieni solo numeriche
    X = df.select_dtypes(include=[np.number])

    # iniezione di rumore (solo in training)
    if add_noise and noise_std > 0:
        np.random.seed(random_state)
        noise = np.random.normal(0, noise_std, X.shape)
        X = X + noise

    return X.values, y, X.columns.tolist()

# ---------------------------------------------------------------------
#  TRAINING
# ---------------------------------------------------------------------
def train_model(X: np.ndarray, y: pd.Series,
                *, oversample_factor: int = 20,
                noise_std: float = 2.2) -> XGBClassifier:
    """
    - random oversampling per ridurre lo sbilanciamento (× oversample_factor)
    - inietta rumore gaussiano (σ = noise_std)
    - addestra un XGBClassifier (parametri di base identici al notebook)
    """
    # oversampling con rimpiazzo
    X_res, y_res = resample(X, y,
                            replace=True,
                            n_samples=len(X) * oversample_factor,
                            random_state=42,
                            stratify=y)

    # rumore gaussiano
    noise = np.random.normal(0, noise_std, X_res.shape)
    X_res_noisy = X_res + noise

    # modello
    clf = XGBClassifier(
        use_label_encoder=False,
        eval_metric='logloss',
        random_state=42,
        n_jobs=1
    )
    clf.fit(X_res_noisy, y_res)
    return clf

# ---------------------------------------------------------------------
#  EVALUATION
# ---------------------------------------------------------------------
def evaluate_model(clf, X, y):
    y_pred  = clf.predict(X)
    y_prob  = clf.predict_proba(X)
    acc     = accuracy_score(y, y_pred)
    ll      = log_loss(y, y_prob)
    prec    = precision_score(y, y_pred, average='weighted', zero_division=0)
    rec     = recall_score(y, y_pred, average='weighted', zero_division=0)
    f1      = f1_score(y, y_pred, average='weighted', zero_division=0)
    report  = classification_report(y, y_pred, zero_division=0)
    return acc, ll, prec, rec, f1, report

# ---------------------------------------------------------------------
#  INFERENCE
# ---------------------------------------------------------------------
def predict(clf, X_test):
    """
    Ritorna la label predetta (0 = sano, 1 = malato)
    """
    return clf.predict(X_test)
