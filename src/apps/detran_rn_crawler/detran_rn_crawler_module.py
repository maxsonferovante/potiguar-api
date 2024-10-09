from nest.core import Module
from .detran_rn_crawler_controller import DetranRnCrawlerController
from .detran_rn_crawler_service import DetranRnCrawlerService


@Module(
    controllers=[DetranRnCrawlerController],
    providers=[DetranRnCrawlerService],
    imports=[]
)   
class DetranRnCrawlerModule:
    pass

    