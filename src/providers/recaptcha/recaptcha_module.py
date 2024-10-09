from nest.core import Module
from .recaptcha_service import RecaptchaService

@Module(
    providers=[RecaptchaService],   
)
class RecaptchaModule:
    pass
        