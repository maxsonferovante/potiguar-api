from nest.core import Module
from .potiguar_lookup_service import PotiguarLookupService

from src.providers.recaptcha.recaptcha_module import RecaptchaModule

@Module(
    providers=[PotiguarLookupService],
    imports=[RecaptchaModule],
)
class PotiguarLookupModule:
    pass