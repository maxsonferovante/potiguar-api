from beanie import Document
        
        
class DetranRnCrawler(Document):
    name: str
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Example Name",
            }
        }
