import cv2
import numpy as np
from scipy.fft import fft2, ifft2, fftshift, ifftshift
from scipy.ndimage import rotate
import matplotlib.pyplot as plt

# Carregar uma imagem
image = cv2.imread("judas.jpg", cv2.IMREAD_GRAYSCALE)

# Aplicar a Transformada de Fourier
F = fft2(image)
F_shifted = fftshift(F)  # Centralizar o espectro

# Rotacionar o espectro de Fourier COMPLETO (magnitude e fase)
angle = 90  # Ângulo de rotação em graus
F_rotated = rotate(F_shifted, angle)

# Rotacionar a imagem
F_rotated_shifted = ifftshift(F_rotated)
image_rotated = np.real(ifft2(F_rotated_shifted))
original_image_rotated = rotate(image, angle)

# Visualizar os resultados
plt.figure(figsize=(10, 10))
plt.subplot(2, 2, 1)
plt.title("Imagem Original")
plt.imshow(image, cmap='gray')

plt.subplot(2, 2, 2)
plt.title("Espectro Rotacionado")
plt.imshow(np.log(1 + np.abs(F_rotated)), cmap='gray')

plt.subplot(2, 2, 3)
plt.title("Imagem Rotacionada")
plt.imshow(original_image_rotated, cmap='gray')

plt.subplot(2, 2, 4)
plt.title("Imagem Rotacionada (Fourier)")
plt.imshow(image_rotated, cmap='gray')

plt.savefig('judas_rotacionado.png')