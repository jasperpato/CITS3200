from abc import ABC, abstractmethod

class Algorithm(ABC):
    
    @abstractmethod
    def similarity(self, post, posts, n):
        pass 



    