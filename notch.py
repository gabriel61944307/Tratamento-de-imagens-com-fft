import numpy as np
import matplotlib.pyplot as plt
import cv2

# Carrega a imagem na escala de cinza
image = cv2.imread("menino_ruido.png", cv2.IMREAD_GRAYSCALE)
rows, cols = image.shape

# Passo 1: Transformada de Fourier da imagem
f_image = np.fft.fft2(image)
f_image_shifted = np.fft.fftshift(f_image)  # Mova o componente de frequencia zero para o centro

# Passo 2: Crie a mascara que anule os pontos de alta frequência
filter_mask = np.ones((rows, cols))

filter_mask[240:241,224:225] = 0
filter_mask[272:273,224:225] = 0
filter_mask[240:241,288:289] = 0
filter_mask[272:273,288:289] = 0

# Passo 3: Multiplique a imagem no dominio da frequência pelo filtro
f_image_filtered = f_image_shifted * filter_mask

# Passo 4: Execute a transformada inversa de Fourier
img_back = np.fft.ifft2(np.fft.ifftshift(f_image_filtered))

# Impressão dos resultados
plt.figure(figsize=(20, 15))

# Imagem original
plt.subplot(331), plt.imshow(image, cmap='gray')
plt.title('Original Image'), plt.axis('off')

# Espectro de Fourier da imagem original
plt.subplot(332), plt.imshow(np.log(np.abs(f_image_shifted) + 1), cmap='gray')
plt.title('Fourier Spectrum (Original Image)'), plt.axis('off')

# Ângulo de fase da imagem original
plt.subplot(333), plt.imshow(np.angle(f_image), cmap='gray')
plt.title('Phase Angle (Original Image)'), plt.axis('off')

# Mascara
plt.subplot(334), plt.imshow(filter_mask, cmap='gray')
plt.title('Spacial Mask'), plt.axis('off')

# Imagem Filtrada
plt.subplot(335), plt.imshow(np.abs(img_back), cmap='gray')
plt.title('Filtered Image'), plt.axis('off')

# Espectro de Fourier da imagem filtrada
plt.subplot(336), plt.imshow(np.log(np.abs(f_image_filtered) + 1), cmap='gray')
plt.title('Fourier Spectrum (Filtered Image)'), plt.axis('off')

plt.tight_layout()
plt.savefig("menino_sem_ruido.png", dpi=300, bbox_inches='tight')