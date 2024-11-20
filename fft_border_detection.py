import cv2
import numpy as np
import matplotlib.pyplot as plt

# Carrega a imagem na escala de cinza
image = cv2.imread("metallica.jpeg", cv2.IMREAD_GRAYSCALE)
rows, cols = image.shape

# Passo 1: Criação da mascara horizontal e da mascara vertical
horizontal_kernel_size = 3
vertical_kernel_size = 3
horizontal_kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
vertical_kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

# Passo 2: Igualar o tamanho das mascaras ao da imagem adicionando padding com zeros as mascaras
horizontal_padded_kernel = np.zeros_like(image, dtype=np.float32)
horizontal_padded_kernel[:horizontal_kernel_size, :horizontal_kernel_size] = horizontal_kernel

vertical_padded_kernel = np.zeros_like(image, dtype=np.float32)
vertical_padded_kernel[:vertical_kernel_size, :vertical_kernel_size] = vertical_kernel

# Passo 3: Aplicar a transformada de Fourier na imagem e nos filtros
f_image = np.fft.fft2(image)
f_horizontal_kernel = np.fft.fft2(horizontal_padded_kernel)
f_vertical_kernel = np.fft.fft2(vertical_padded_kernel)

# Passo 4: Multiplique a imagem e as mascaras
f_image_filtered = f_image * f_horizontal_kernel * f_vertical_kernel

# Passo 5: Aplique a transformação inversa
img_back = np.fft.ifft2(f_image_filtered)
img_back = np.abs(img_back)

# Aplicação de um treshold: Se o pixel for menor que 125 ele é zerado do contrario ganha valor igual a 255
_, img_thresholded = cv2.threshold(img_back, 125, 255, cv2.THRESH_BINARY)

# Impressão dos resultados
plt.figure(figsize=(20, 15))

# Imagem original
plt.subplot(331), plt.imshow(image, cmap='gray')
plt.title('Imagem original'), plt.axis('off')

# Espectro de Fourier da imagem original
plt.subplot(332), plt.imshow(np.log(np.abs(np.fft.fftshift(f_image)) + 1), cmap='gray')
plt.title('Espectro de Fourier (imagem original)'), plt.axis('off')

# Ângulo de fase da imagem original
plt.subplot(333), plt.imshow(np.angle(f_image), cmap='gray')
plt.title('Ângulo de fase (imagem original)'), plt.axis('off')

# Espectro de Fourier da mascara horizontal
plt.subplot(334), plt.imshow(np.log(1 + np.fft.fftshift(np.abs(f_horizontal_kernel))), cmap='gray')
plt.title('Espectro de Fourier (filtro horizontal)'), plt.axis('off')

# Espectro de Fourier da mascara vertical
plt.subplot(335), plt.imshow(np.log(1 + np.fft.fftshift(np.abs(f_vertical_kernel))), cmap='gray')
plt.title('Espectro de Fourier (filtro vertical)'), plt.axis('off')

# Imagem apenas com as bordas (sem threshold)
plt.subplot(336), plt.imshow(img_back, cmap='gray')
plt.title('Imagem com detecção de borda'), plt.axis('off')

# Imagem apenas com as bordas (com threshold)
plt.subplot(337), plt.imshow(img_thresholded, cmap='gray')
plt.title('Imagem com detecção de borda (Threshold)'), plt.axis('off')

plt.tight_layout()
plt.savefig("metallica_black_deteccao.png", dpi=300, bbox_inches='tight')