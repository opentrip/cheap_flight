from .web_searcher import Searcher as WebSearcher
from .api_searcher import Searcher as APISearcher

# TODO failover
Searcher = [WebSearcher, APISearcher]

__all__ = ['Searcher']
