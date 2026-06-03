from enumeration.CartStatus import CartStatus
from model.Article import Article


class ShoppingCart:
    def __init__(self, id: int, articles: list, status: CartStatus, discount: int, history: list):
        self._id = id
        self._articles = articles
        self._gross_total = 0
        self._net_total = 0
        self._status = status
        self._discount = discount
        self.__history = history

    def get_id(self):
        return self._id

    def get_articles(self):
        return self._articles

    def add_article(self, articles: Article) -> list:
        self._articles.append(articles)
        return self._articles

    def set_articles(self, articles: list):
        self._articles = articles

    def get_gross_total(self):
        self._gross_total = 0
        if len(self._articles) >= 1:
            for article in self._articles:
                self._gross_total += article.get_price()
        return self._gross_total

    def get_net_total(self):
        return self._gross_total * self._discount

    def set_net_total(self, net_total):
        self._net_total = net_total

    def get_discount(self):
        return self._discount

    def set_discount(self, discount):
        self._discount = discount

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def get_history(self):
        return self.__history


