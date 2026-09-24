import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

MODELO_PATH = os.path.join(os.path.dirname(__file__), "modelo_rigfy.joblib")

FEATURES_CATEGORICAS = [
    "categoria", "marca", "cpu_linha", "ram_tipo", 
    "storage_tipo", "gpu", "gpu_memoria_tipo"
]
FEATURES_NUMERICAS = [
    "cpu_geracao_num", "ram_gb", "storage_gb", 
    "gpu_vram_gb", "ano_lancamento"
]

def preparar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # Extrai número de geração da CPU (ex: '10ª Geração' -> 10)
    if "cpu_geracao" in df.columns:
        df["cpu_geracao_num"] = pd.to_numeric(
            df["cpu_geracao"].astype(str).str.extract(r"(\d+)")[0], 
            errors="coerce"
        ).fillna(0)
    else:
        df["cpu_geracao_num"] = 0.0
        
    for col in FEATURES_CATEGORICAS:
        if col not in df.columns:
            df[col] = "desconhecido"
        else:
            df[col] = df[col].fillna("desconhecido").astype(str).str.strip().str.lower()
            
    for col in FEATURES_NUMERICAS:
        if col not in df.columns:
            df[col] = 0.0
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
            
    return df

def criar_pipeline_ml() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", FEATURES_NUMERICAS),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), FEATURES_CATEGORICAS),
        ]
    )
    
    rf = RandomForestRegressor(
        n_estimators=100,
        max_depth=12,
        min_samples_split=3,
        random_state=42,
        n_jobs=-1
    )
    
    return Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", rf)
    ])

def prever_faixa_preco(model_pipeline: Pipeline, input_data: dict) -> dict:
    df_input = pd.DataFrame([input_data])
    df_preparado = preparar_dataframe(df_input)
    
    rf_regressor = model_pipeline.named_steps["regressor"]
    preprocessor = model_pipeline.named_steps["preprocessor"]
    
    X_trans = preprocessor.transform(df_preparado)
    
    predicoes_arvores = np.array([tree.predict(X_trans)[0] for tree in rf_regressor.estimators_])
    
    return {
        "preco_estimado": round(float(np.median(predicoes_arvores)), 2),
        "preco_medio": round(float(np.mean(predicoes_arvores)), 2),
        "preco_minimo": round(float(np.percentile(predicoes_arvores, 15)), 2),
        "preco_maximo": round(float(np.percentile(predicoes_arvores, 85)), 2),
        "variancia_arvores": round(float(np.std(predicoes_arvores)), 2)
    }

def salvar_modelo(model_pipeline: Pipeline):
    joblib.dump(model_pipeline, MODELO_PATH)

def carregar_modelo() -> Pipeline | None:
    if os.path.exists(MODELO_PATH):
        return joblib.load(MODELO_PATH)
    return None
