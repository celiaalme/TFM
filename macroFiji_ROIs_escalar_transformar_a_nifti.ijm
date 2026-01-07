// Crear un diálogo para ingresar el tamaño de la imagen
//Dialog.create("Definir tamaño de la imagen");

// Añadir campos de entrada para el ancho, alto y profundidad
//Dialog.addNumber("Ancho (Width):", 256);
//Dialog.addNumber("Alto (Height):", 256);
//Dialog.addNumber("Profundidad (Depth):", 1);  // Usar 1 para imágenes 2D o mayor para 3D

// Mostrar el diálogo y obtener los valores introducidos
//Dialog.show();
//width = Dialog.getNumber();
//height = Dialog.getNumber();
//depth = Dialog.getNumber();
width = 256;
height = 256;
depth = 1;

// Solicitar el archivo de ROIs
roiFile = File.openDialog("Selecciona el archivo de ROIs (.zip o .roi)");
//if (roiFile == null) {
//    exit("No se seleccionó ningún archivo de ROIs.");
//}

// Cargar el archivo de ROIs en el RoiManager
run("ROI Manager...");
roiManager("reset");
roiManager("Open", roiFile);
nRois = roiManager("count");

// Escalamos las ROIs para que su tamaño coincida con las imágenes de MRI
roiManager("Deselect");
array = newArray(nRois);
for (j=0; j<array.length; j++) {
        array[j] = j;
}
roiManager("select", array);
RoiManager.scale(2.0, 2.0, false);

// Crear una nueva imagen vacía para cada ROI, donde cada ROI tendrá un valor único
// Crear una imagen nueva en 32 bits
outputPath = getDirectory("Selecciona dónde guardar la imagen de máscara");
for (i=0; i<array.length; i++) {
	newImage("Mask Image", "32-bit black", width, height, depth); 
	// Rellenar la máscara con cada ROI asignándole un valor único    
	roiManager("select", i);
    run("Set...", "value=" + 1);
    RoiName = Roi.getName;
    // Guardar la imagen como NIfTI
    run("NIfTI-1", "save=[" + outputPath + "mask_" + RoiName +  ".nii" + "]");
	close;
}