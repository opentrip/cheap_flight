from .web_searcher import Searcher as WebSearcher
from .api_searcher import Searcher as APISearcher

Searcher = [WebSearcher, APISearcher]

__all__ = ['Searcher']
