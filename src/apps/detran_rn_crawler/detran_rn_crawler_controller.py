from nest.core import Controller, Get, Post

from .detran_rn_crawler_service import DetranRnCrawlerService
from .detran_rn_crawler_model import DetranRnCrawler


@Controller("detran_rn_crawler")
class DetranRnCrawlerController:

    def __init__(self, detran_rn_crawler_service: DetranRnCrawlerService):
        self.service = service

    @Get("/")
    async def get_detran_rn_crawler(self):
        return await self.detran_rn_crawler_service.get_detran_rn_crawler()

    @Post("/")
    async def add_detran_rn_crawler(self, detran_rn_crawler: DetranRnCrawler):
        return await self.detran_rn_crawler_service.add_detran_rn_crawler(detran_rn_crawler)
 