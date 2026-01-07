import os
import json
import SimpleITK as sitk
import numpy as np
from PIL import Image
from pathlib import Path
import random


# Paths relativos de las imágenes y las máscaras
dir_datos = Path("/Users/celiaalme/Desktop/TFM/Practica_Celia/Estudios")
dir_datosROIs = Path("/Users/celiaalme/Desktop/TFM/Practica_Celia/ROIS")

# Directorio de salida en formato nnU-Net
dir_target = "/Users/celiaalme/Desktop/TFM"
dir_output = os.path.join(dir_target, "nnUNet/nnUNet_raw/Dataset011_Glioblastoma")
os.makedirs(dir_output, exist_ok=True)
os.makedirs(os.path.join(dir_output, "imagesTr"), exist_ok=True)
os.makedirs(os.path.join(dir_output, "labelsTr"), exist_ok=True)
os.makedirs(os.path.join(dir_output, "imagesTs"), exist_ok=True)

# Lista para almacenar las imágenes y máscaras procesadas
cases = []
case_id = 0

# Función para extraer el slice de la imagen 3D donde se dibujaron las ROIs
def extract_slice(image_3d, slice_index=2):
    # Cargamos la imagen y las labels (no hago bucle porque hay distintos tipos de corte); cambiamos el nombre del archivo 
    image_3d = sitk.ReadImage(str(dir_datos.joinpath(dir).joinpath(subDir).joinpath(resoDir).joinpath(sourcedataDir).joinpath(studyDir).joinpath(imgfile)))
    # Obtenemos el tamaño de la imagen
    size = list(image_3d.GetSize())
    size[2] = 1  # cambiamos el tamaño de la dimensión Z a 1 (para extraer un solo corte)
    # Establecer el índice de inicio del corte
    index = [0, 0, slice_index]
    # Usar el filtro de extracción
    ex_slicer = sitk.ExtractImageFilter()
    ex_slicer.SetSize(size)
    ex_slicer.SetIndex(index)
    slice = ex_slicer.Execute(image_3d)  
    # Convertir la imagen a 2D eliminando la dimensión Z
    slice_2D = sitk.GetImageFromArray(sitk.GetArrayFromImage(slice))
    # Ajustar el espaciado para la imagen 2D
    slice_2D.SetSpacing(slice.GetSpacing()) # Solo se usan las dos primeras dimensiones
    return slice_2D



# Función para comprobar que cogeremos la máscara que se corresponda con la imagen 
# (comprobación del nombre de los directorios)
def verificar_codigo(dir_img, dir_ROIs):
    codigo = dir_ROIs[:7]
    if codigo in dir_img:
        return True
    else:
        return False  



for dir in os.listdir(dir_datos):
    if not dir.startswith('.'):
        
        # subDir: hembras, machos
        for subDir in os.listdir(dir_datos.joinpath(dir)):
            if not subDir.startswith('.'):
                
                # resoDir: resomapper_output
                for resoDir in os.listdir(dir_datos.joinpath(dir).joinpath(subDir)):
                    if not resoDir.startswith('.'):
                        
                    # sourcedataDir: derivatives, sourcedata
                        for sourcedataDir in os.listdir(dir_datos.joinpath(dir).joinpath(subDir).joinpath(resoDir)):
                            if not sourcedataDir.startswith('.') and sourcedataDir == "sourcedata":
                                
                                # studyDir: estudio
                                for studyDir in os.listdir(dir_datos.joinpath(dir).joinpath(subDir).joinpath(resoDir).joinpath(sourcedataDir)):
                                    if not studyDir.startswith('.'):
                                        for imgfile in os.listdir(dir_datos.joinpath(dir).joinpath(subDir).joinpath(resoDir).joinpath(sourcedataDir).joinpath(studyDir)):
                                            if not imgfile.startswith('.') and imgfile.endswith('.nii.gz'):
                                                slice_2D = extract_slice(imgfile)
                                                
                                                
                                                for dir_ROI in os.listdir(dir_datosROIs):
                                                    if not dir_ROI.startswith('.'):
                                                        for subDir_ROI in os.listdir(dir_datosROIs.joinpath(dir_ROI)):
                                                            if not subDir_ROI.startswith('.'):
                                                                for studyDir_ROI in os.listdir(dir_datosROIs.joinpath(dir_ROI).joinpath(subDir_ROI)):
                                                                    if not studyDir_ROI.startswith('.'):
                                                                        if verificar_codigo(imgfile, studyDir_ROI):
                                                                            
                                                                            # Crear una máscara combinada inicializada con ceros
                                                                            combined_mask = sitk.Image(slice_2D.GetSize(), sitk.sitkUInt8)
                                                                            combined_mask.SetOrigin(slice_2D.GetOrigin())
                                                                            combined_mask.SetSpacing(slice_2D.GetSpacing())
                                                                            combined_mask.SetDirection(slice_2D.GetDirection())
                                                                            
                                                                            for maskfile in os.listdir(dir_datosROIs.joinpath(dir_ROI).joinpath(subDir_ROI).joinpath(studyDir_ROI)):
                                                                                # Seleccionamos las máscaras en archivo NIfTI
                                                                                if maskfile.endswith('.nii'): 
                                                                                    mask_2D = sitk.ReadImage(str(dir_datosROIs.joinpath(dir_ROI).joinpath(subDir_ROI).joinpath(studyDir_ROI).joinpath(maskfile)))
                                                                                    mask_2D.SetOrigin(slice_2D.GetOrigin())
                                                                                    mask_2D.SetSpacing(slice_2D.GetSpacing())
                                                                                    mask_2D.SetDirection(slice_2D.GetDirection())
                                                                                    
                                                                                    # Identificar el tipo de máscara (ALL, CL, IN, TC, TP)
                                                                                    mask_value = 0
                                                                                    if "ALL" in maskfile:
                                                                                        mask_value = "1"
                                                                                    elif "CL" in maskfile:
                                                                                        mask_value = "2"
                                                                                    elif "IN" in maskfile:
                                                                                        mask_value = "3"
                                                                                    elif "TC" in maskfile:
                                                                                        mask_value = "4"
                                                                                    elif "TP" in maskfile:
                                                                                        mask_value = "5"
                                                                                        
                                                                                    # Combinar la máscara actual con la máscara combinada
                                                                                    mask_array = sitk.GetArrayFromImage(mask_2D)
                                                                                    combined_array = sitk.GetArrayFromImage(combined_mask)
                                                                                    
                                                                                    # Asegurarse de que no haya solapamientos
                                                                                    combined_array[mask_array > 0] = mask_value
                                                                                    combined_mask = sitk.GetImageFromArray(combined_array)
                                                                                    combined_mask.SetOrigin(slice_2D.GetOrigin())
                                                                                    combined_mask.SetSpacing(slice_2D.GetSpacing())
                                                                                    combined_mask.SetDirection(slice_2D.GetDirection())
                                                                                        
                                                # Guardar en formato nnU-Net
                                                case_name = f"case_{case_id:03d}"
                                                sitk.WriteImage(slice_2D, os.path.join(dir_output, "imagesTr", f"{case_name}_0000.nii.gz"))
                                                #sitk.WriteImage(combined_mask, os.path.join(dir_output, "labelsTr", f"{case_name}_0000.nii.gz"))
                                                sitk.WriteImage(combined_mask, os.path.join(dir_output, "labelsTr", f"{case_name}.nii.gz"))
                                                cases.append(case_name)
                                                case_id += 1
                                                
# Mezclar las imágenes aleatoriamente
random.shuffle(cases)

# Dividir el dataset en entrenamiento y test
num_training = int(len(cases) * 0.7)  # 70% para entrenamiento
training_cases = cases[:num_training]
test_cases = cases[num_training:]    

# Movemos las imágenes de training a la carpeta imagesTs
for case_name in test_cases:
    slice_2D = sitk.ReadImage(str(os.path.join(dir_output, "imagesTr", f"{case_name}_0000.nii.gz")))
    sitk.WriteImage(slice_2D, os.path.join(dir_output, "imagesTs", f"{case_name}_0000.nii.gz"))
    # Eliminamos la imagen de prueba de imagesTr
    os.remove(os.path.join(dir_output, "imagesTr", f"{case_name}_0000.nii.gz"))         
    
    # Eliminar la máscara correspondiente de labelsTr
    label_path = os.path.join(dir_output, "labelsTr", f"{case_name}.nii.gz")
    if os.path.exists(label_path):
        os.remove(label_path)                              

# Crear el archivo dataset.json (metadatos)
dataset_json = {
    "name": "Task011_Glioblastoma",
    "description": "Segmentacion 2D de GBM con varias mascaras",
    "tensorImageSize": "2D", # trabajamos con imágenes 2D (hemos extraído un slice)
    # Cada etiqueta corresponde a una ROI diferente    
    "labels": {
        "background": 0,
        "ALL": 1,
        "CL": 2,
        "IN": 3,
        "TC": 4,
        "TP": 5
    },
    #Como solo tenemos un canal T2, debe ser:
    "channel_names": { "0": "T2" },
    "file_ending": ".nii.gz",
    "numTraining": len(training_cases),
    "training": [
        {
            "image": f"./imagesTr/{training_case}_0000.nii.gz",
            "label": f"./labelsTr/{training_case}.nii.gz"
        }
        for training_case in training_cases
    ],
    "numTest": len(test_cases),
    "test": [
        {
            "image": f"./imagesTs/{test_case}_0000.nii.gz",
        }
        for test_case in test_cases
    ]
}


with open(os.path.join(dir_output, "dataset.json"), "w") as f:
    json.dump(dataset_json, f, indent=4)

print("dataset.json generado correctamente.")
                                                                                    