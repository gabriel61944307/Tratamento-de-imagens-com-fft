import cv2
import numpy as np
import matplotlib.pyplot as plt

# Carrega a imagem na escala de cinza
image = cv2.imread("mega.jpg", cv2.IMREAD_GRAYSCALE)
rows, cols = image.shape

# Passo 1: Cria a mascara de realce de bordas
kernel_size = 3
average_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

# Passo 2: Igualar o tamanho da mascara ao tamanho da imagem adicionando padding com zeros a kernel
padded_kernel = np.zeros_like(image, dtype=np.float32)
padded_kernel[:kernel_size, :kernel_size] = average_kernel

# Passo 3: Aplicação da transformada de Fourier na imagem e na mascara
f_image = np.fft.fft2(image)
f_kernel = np.fft.fft2(padded_kernel)

# Passo 4: Multiplicação da mascara e da imagem ambas após a transformada de Fourier
f_image_filtered = f_image * f_kernel

# Passo 5: Aplicação da transformada inversa e de normalização na imagem
img_back = np.fft.ifft2(f_image_filtered)
img_back = np.abs(img_back)
img_back = np.uint8(np.clip(img_back, 0, 255))

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
plt.title('Ângulo de Fase (imagem original)'), plt.axis('off')

# Espectro de Fourier da mascara
plt.subplot(154), plt.imshow(np.log(1 + np.fft.fftshift(np.abs(f_kernel))), cmap='gray')
plt.title('Espectro de Fourier (filtro realce de borda)'), plt.axis('off')

# imagem com as bordas realçadas
plt.subplot(155), plt.imshow(img_back, cmap='gray')
plt.title('Imagem com bordas realçadas'), plt.axis('off')

plt.savefig("megadeth_realce.png", dpi=300, bbox_inches='tight')