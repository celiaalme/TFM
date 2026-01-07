import os
import glob
import pandas as pd
from pathlib import Path

base = Path("/Users/celiaalme/Desktop/TFM/Practica_Celia/Estudios")

# Creamos una función para procesar el CSV de un ratón (luego lo aplicaremos
# a todos los CSVs)
def procesar_csv(path, diet, week, sex, mouse_id=None):
    df = pd.read_csv(path) 
    df = df.rename(columns={df.columns[0]: "feature"})
    # solo queremos las filas de las features, las de los metadatos no las necesitamos
    df = df[df["feature"].str.startswith("original_")].copy() 
    
    # Queremos conseguir que las ROIs no sean columnas sino que formen parte 
    # del nombre de las características; ej: original_shape_Elongation_ALL
    # Cambiaremos el formato ancho a formato largo para poder llevarlo a cabo
    long = df.melt(
        id_vars= "feature",
        var_name= "ROI", 
        value_name= "value"
    )
    # Convertimos "value" a numérico
    long["value"] = pd.to_numeric(long["value"], errors="coerce")
    long["feature_ROI"] = long["feature"] + "_" + long["ROI"]
    wide = long.pivot_table(
        index=None, 
        columns="feature_ROI",
        values="value",
        aggfunc="mean"
    ).reset_index(drop=True)
    wide["diet"] = diet
    wide["week"] = week
    wide["sex"] = sex
    
    if mouse_id is None:
        mouse_id = Path(path).stem
    wide["mouse_id"] = mouse_id
    
    metadata_cols = ["mouse_id", "diet", "week", "sex"]
    feature_cols = [c for c in wide.columns if c not in metadata_cols]
    wide = wide[metadata_cols + feature_cols]
    
    return wide

# Iteramos las carpetas para aplicar la función a cada csv
# En "rows" guardaremos un dataframe por cada ratón
rows = []
sex_dict = {"Hembras": "F", "Machos": "M"}
# Procesamos los CSVs de la dieta control a las 10 semanas
for sex_folder, sex_label in sex_dict.items():
    selected_path = base/"ControlDiet_10_SEMANAS"/"CSV"/sex_folder/"*.csv"
    for csv_path in glob.glob(str(selected_path)):
        row = procesar_csv(
            path=csv_path,
            diet="Control",
            week=10, 
            sex=sex_label
        )
        rows.append(row)
        
# ControlDiet 20 semanas
for sex_folder, sex_label in sex_dict.items():
    selected_path = base/"ControlDiet_20_SEMANAS"/"CSV"/sex_folder/"*.csv"
    for csv_path in glob.glob(str(selected_path)):
        row = procesar_csv(
            path=csv_path,
            diet="Control",
            week=20, 
            sex=sex_label
        )
        rows.append(row)

# Procesamos los CSVs de la dieta alta en grasa (HFD) a las 10 semanas
for sex_folder, sex_label in sex_dict.items():
    selected_path = base/"HFD_10_SEMANAS"/"CSV"/sex_folder/"*.csv"
    for csv_path in glob.glob(str(selected_path)):
        row = procesar_csv(
            path=csv_path,
            diet="HFD",
            week=10, 
            sex=sex_label
        )
        rows.append(row)

# HFD 20 semanas
for sex_folder, sex_label in sex_dict.items():
    selected_path = base/"HFD_20_SEMANAS"/"CSV"/sex_folder/"*.csv"
    for csv_path in glob.glob(str(selected_path)):
        row = procesar_csv(
            path=csv_path,
            diet="HFD",
            week=20, 
            sex=sex_label
        )
        rows.append(row)


# Unimos todas las filas (ratones) en una tabla
data = pd.concat(rows, axis=0, ignore_index=True)

output_path = base/"features_all.csv"
# Guardamos el CSV final (con 15 decimales para evitar problemas de precisión) 
data.to_csv(output_path, index=False, float_format="%.15g")