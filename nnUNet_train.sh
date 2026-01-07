# Primer fold (0)
nnUNetv2_train 11 2d 0 -tr nnUNetTrainer_100epochs -device mps

# Segundo fold (1)
nnUNetv2_train 11 2d 1 -tr nnUNetTrainer_100epochs -device mps

# Tercer fold (2)
nnUNetv2_train 11 2d 2 -tr nnUNetTrainer_100epochs -device mps

# Cuarto fold (4)
nnUNetv2_train 11 2d 1 -tr nnUNetTrainer_100epochs -device mps

# Quinto fold (5)
nnUNetv2_train 11 2d 1 -tr nnUNetTrainer_100epochs -device mps