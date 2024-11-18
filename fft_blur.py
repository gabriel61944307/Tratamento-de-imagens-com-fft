import cv2
import numpy as np
import matplotlib.pyplot as plt

# Carrega a imagem na escala de cinza
image = cv2.imread("Creedence.jpg", cv2.IMREAD_GRAYSCALE)
rows, cols = image.shape

# Passo 1: Cria uma mascara 7x7 de média
kernel_size = 7
average_kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)

# Passo 2: Igualar o tamanho da mascara ao tamanho da imagem adicionando padding com zeros a kernel
padded_kernel = np.zeros_like(image, dtype=np.float32)
padded_kernel[:kernel_size, :kernel_size] = average_kernel

# Passo 3: Transformada de Fourier na imagem e no kernel
f_image = np.fft.fft2(image)
f_kernel = np.fft.fft2(padded_kernel)

# Passo 4: Multiplicação da imagem pelo kernel já passados pela transformada
f_image_filtered = f_image * f_kernel

# Passo 5: Executar a transformada inversa de Fourier na imagem multiplicada pelo filtro
img_back = np.fft.ifft2(f_image_filtered)
img_back = np.abs(img_back)

# Impressão dos resultados
plt.figure(figsize=(20, 5))

# Imagem original
plt.subplot(151), plt.imshow(image, cmap='gray')
plt.title('Imagem original'), plt.axis('off')

# Espectro de Fourier da imagem original
plt.subplot(152), plt.imshow(np.log(np.abs(np.fft.fftshift(f_image)) + 1), cmap='gray')
plt.title('Espectro de Fourier (imagem original)'), plt.axis('off')

# Ângulo de fase da imagem original
plt.subplot(153), plt.imshow(np.angle(f_image), cmap='gray')
plt.title('Ângulo de fase (imagem original)'), plt.axis('off')

# Espectro de Fourier da mascara
plt.subplot(154), plt.imshow(np.log(1 + np.fft.fftshift(np.abs(f_kernel))), cmap='gray')
plt.title('Espectro de Fourier (filtro de desfoque)'), plt.axis('off')

# Imagem desfocada
plt.subplot(155), plt.imshow(img_back, cmap='gray')
plt.title('Imagem desfocada'), plt.axis('off')

plt.savefig("Creedence_desfocado.png", dpi=300, bbox_inches='tight')