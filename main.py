import qrcode
from PIL import Image, ImageDraw, ImageFont

# Configura tu dirección de wallet y detalles
wallet_address = "TZ1MP76aV6mfQGcAuHQXQr6ZJ9VB9QKt2A"  # Reemplaza con tu dirección real
crypto_scheme = "tron"  # Cambia a "tron" si usas TRC-20, por ejemplo
amount = "5"  # Monto opcional en USDT (puedes dejarlo vacío si no quieres especificar)

# Crear la URI para criptomonedas
if amount:
    crypto_uri = f"{crypto_scheme}:{wallet_address}?amount={amount}"
else:
    crypto_uri = f"{crypto_scheme}:{wallet_address}"

# Crear el objeto QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

# Añadir la URI al QR
qr.add_data(crypto_uri)
qr.make(fit=True)

# Generar la imagen del QR
qr_image = qr.make_image(fill_color="black", back_color="white").convert('RGB')

# (Opcional) Añadir un logo de USDT
try:
    logo = Image.open("usdt_logo.png").convert('RGBA')
    qr_width, qr_height = qr_image.size
    logo_size = qr_width // 4
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
    qr_image.paste(logo, logo_position, logo)
except FileNotFoundError:
    print("No se encontró 'usdt_logo.png'. Se generará el QR sin logo.")

# Crear una nueva imagen con espacio adicional para el texto
original_width, original_height = qr_image.size
text_height = 50  # Altura adicional para el texto
new_height = original_height + text_height
new_image = Image.new('RGB', (original_width, new_height), color="white")
new_image.paste(qr_image, (0, 0))

# Añadir la dirección de la wallet como texto
draw = ImageDraw.Draw(new_image)
try:
    font = ImageFont.truetype("arial.ttf", 20)  # Usa una fuente instalada en tu sistema
except:
    font = ImageFont.load_default()  # Fuente por defecto si no encuentra arial.ttf

# Calcular la posición del texto (centrado en el borde inferior)
text = wallet_address
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_x = (original_width - text_width) // 2
text_y = original_height + (text_height - (text_bbox[3] - text_bbox[1])) // 2

draw.text((text_x, text_y), text, font=font, fill="black")

# Guardar la imagen
new_image.save("usdt_wallet_qr_con_direccion.png")

print("¡Código QR para USDT con dirección en el borde inferior generado como 'usdt_wallet_qr_con_direccion.png'!")