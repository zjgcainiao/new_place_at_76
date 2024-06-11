
import qrcode


def generate_qrcode(data_str):

    qr = qrcode.QRCode(
        version=1,  # Adjust version based on the amount of data
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data_str)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
