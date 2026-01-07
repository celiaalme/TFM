#Si se requiere
pip install nnunetv2


# Inicializamos variables
export nnUNet_raw=/Users/celiaalme/Desktop/TFM/nnUNet/nnUNet_raw
export nnUNet_preprocessed=/Users/celiaalme/Desktop/TFM/nnUNet/nnUNet_preprocessed
export nnUNet_results=/Users/celiaalme/Desktop/TFM/nnUNet/nnUNet_results

# Plan de entrenamiento generado por nnU-Net
nnUNetv2_plan_and_preprocess -d 011 --verify_dataset_integrity
