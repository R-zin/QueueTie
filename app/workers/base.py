from abc import ABC,abstractmethod

class BaseWorker(ABC):
    @abstractmethod
    async def process(self,job:dict):
        pass
