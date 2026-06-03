import math

from exception.AlreadyValidated import AlreadyValidatedError
from exception.LockedCart import LockedCartError
from model.Article import Article
from model.ShoppingCart import ShoppingCart
from datetime import datetime
import copy


class DiscountEngine:
    def __init__(self, cart: ShoppingCart):
        self._cart = cart

    def get_cart(self):
        return self._cart

    def get_freeze_history(self):
        return copy.copy(self._cart.get_history())

    def modify_status(self, new_status: str):
        self._cart.set_status(new_status)

    def modify_discount(self, new_discount: int):
        if self._cart.get_status() == "VALIDATED":
            self._cart.get_history().append(("VALIDATED CART", "IF CART VALIDATED", new_discount, "REFUSED", datetime.today()))
            raise AlreadyValidatedError("Error. Cart already validated")
        if self._cart.get_status() == "LOCKED":
            self._cart.get_history().append(
                ("LOCKED CART", "IF CART LOCKED", new_discount, "REFUSED", datetime.today()))
            raise LockedCartError("Error. Cart already locked")
        if new_discount > 30:
            new_discount = 30
            self._cart.get_history().append(("CEILING", "IF DISCOUNT > 30", 30, "APPLIED", datetime.today()))
        if new_discount > 25:
            self._cart.set_status("VALIDATED")
            self._cart.get_history().append(("VALIDATED CART", "IF DISCOUNT > 25", 25, "APPLIED", datetime.today()))
        self._cart.set_discount(new_discount)

    def add_articles(self, new_article: Article):
        if self._cart.get_status() == "VALIDATED":
            raise AlreadyValidatedError("Error. Cart already validated")
        if self._cart.get_status() == "LOCKED":
            raise LockedCartError("Error. Cart already locked")
        articles = self._cart.get_articles()
        articles.append(new_article)

    def calcul_gross_total_with_quantity_rule(self):
        articles = self._cart.get_articles()
        gross_total_before_discount = self._cart.get_gross_total()
        for article in set(articles):
            if articles.count(article) >= 3:
                gross_total_before_discount -= article.get_price()
        return gross_total_before_discount

    def calcul_net_total(self):
        gross_total = self.calcul_gross_total_with_quantity_rule()
        return gross_total *  math.ceil(1 - (self._cart.get_discount() / 100))

    def calcul_discount(self):
        total_gross = 0
        total_discount = 0
        discount_special = False
        for article in self._cart.get_articles():
            if article.get_type() != "CLEARANCE":
                total_gross += article.get_price()
        if 100 <= total_gross < 300:
            total_discount = 5
            self._cart.get_history().append(("CLASSIC_DISCOUNT", "IF 100 <= TOTAL_GROSS < 300", 5, "APPLIED", datetime.today()))
        elif 300 <= total_gross < 500:
            total_discount = 8
            self._cart.get_history().append(("CLASSIC_DISCOUNT", "IF 300 <= TOTAL_GROSS < 500", 8, "APPLIED", datetime.today()))
        elif 500 <= total_gross:
            total_discount = 10
            self._cart.get_history().append(
                ("CLASSIC_DISCOUNT", "IF 500 < TOTAL_GROSS", 10, "APPLIED", datetime.today()))
        else:
            total_discount = 0
            self._cart.get_history().append(("CLASSIC_DISCOUNT", "IF 0 <= TOTAL_GROSS < 100", 0, "APPLIED", datetime.today()))
        for article in self._cart.get_articles():
            if article.get_type() == "SPECIAL" and discount_special == False and self.calcul_gross_total_with_quantity_rule() >= 500:
                total_discount += 8
                discount_special = True
                self._cart.get_history().append(
                    ("SPECIAL_DISCOUNT", "IF TOTAL_GROSS => 500 AND SPECIAL", 8, "APPLIED", datetime.today()))
            if article.get_type() == "SPECIAL" and discount_special == False:
                total_discount += 3
                discount_special = True
                self._cart.get_history().append(
                    ("SPECIAL_DISCOUNT", "IF TOTAL_GROSS < 500 AND SPECIAL", 3, "APPLIED", datetime.today()))
        if total_discount == 0:
            total_discount = 1
        self.modify_discount(total_discount)



# if __name__ == '__main__':>