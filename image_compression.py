import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

# Carrega a imagem na escala de cinza
image = cv2.imread('mega.jpg', cv2.IMREAD_GRAYSCALE)

# Aplicação da fft na imagem original
f = np.fft.fft2(image)
fshift = np.fft.fftshift(f)  # Invertendo a frequência alta para o centro

# Niveis de comprensão de imagem
compression_levels = [0.2, 0.1, 0.05]

# Prepare to display multiple images in one figure
plt.figure(figsize=(15, 5))
plt.subplot(1, len(compression_levels) + 1, 1)
plt.title("Imagem Original")
plt.imshow(image, cmap='gray')
plt.axis('off')

# Comprimindo a imagem em diferentes niveis e salvando
for i, keep in enumerate(compression_levels, start=2):
    # Obtendo espectro de magnitude e setando um threshold
    f_magnitude = np.abs(fshift).flatten()
    f_magnitude.sort()
    threshold = f_magnitude[math.floor((1 - keep) * len(f_magnitude))]

    # Mascara criada colocando 0 nos valores abaixo do threshold e 1 nos locais acima e multiplicação pela imagem
    mask = np.abs(fshift) > threshold
    fshift_compressed = fshift * mask

    # Aplicação da função inversa de Fourier na imagem original
    f_ishift = np.fft.ifftshift(fshift_compressed)
    image_compressed = np.fft.ifft2(f_ishift)
    image_compressed = np.abs(image_compressed)

    # Salvando a imagem de cada compressão
    plt.subplot(1, len(compression_levels) + 1, i)
    plt.title(f"Mantendo {keep*100}% das frequências")
    plt.imshow(image_compressed, cmap='gray')
    plt.axis('off')

plt.savefig('compressed_images.png', bbox_inches='tight')
