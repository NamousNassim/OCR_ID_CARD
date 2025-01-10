import pyotp
import qrcode
import io
import base64
from app.core.config import settings

class TOTPService:
    def __init__(self):
        self.period = 30
        self.digits = 6

    def generate_secret(self) -> str:
         
        return pyotp.random_base32()

    def create_totp(self, secret: str) -> pyotp.TOTP:
         
        return pyotp.TOTP(secret, digits=self.digits, interval=self.period)

    def verify_code(self, secret: str, code: str) -> bool:
        
        totp = self.create_totp(secret)
        return totp.verify(code)

    def get_current_code(self, secret: str) -> str:
 
        totp = self.create_totp(secret)
        return totp.now()

    def get_provisioning_uri(self, secret: str, email: str) -> str:
        
        totp = self.create_totp(secret)
        return totp.provisioning_uri(
            name=email,
            issuer_name=settings.PROJECT_NAME
        )

    def generate_qr_code(self, secret: str, email: str) -> str:
        
        uri = self.get_provisioning_uri(secret, email)
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

totp_service = TOTPService()