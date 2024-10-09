from .detran_rn_crawler_model import DetranRnCrawler
from .detran_rn_crawler_entity import DetranRnCrawler as DetranRnCrawlerEntity
from nest.core.decorators.database import db_request_handler
from nest.core import Injectable


@Injectable
class DetranRnCrawlerService:

    @db_request_handler
    async def add_detran_rn_crawler(self, detran_rn_crawler: DetranRnCrawler):
        new_detran_rn_crawler = DetranRnCrawlerEntity(
            **detran_rn_crawler.dict()
        )
        await new_detran_rn_crawler.save()
        return new_detran_rn_crawler.id

    @db_request_handler
    async def get_detran_rn_crawler(self):
        return await DetranRnCrawlerEntity.find_all().to_list()
