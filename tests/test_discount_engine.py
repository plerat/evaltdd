import pytest

from exception.AlreadyValidated import AlreadyValidatedError
from exception.DiscountTooHigh import DiscountTooHigh
from exception.LockedCart import LockedCartError
from exception.ValidatedAndFreezeCart import ValidatedAndFreezeCart
from model.Article import Article
from model.DiscountEngine import DiscountEngine
from model.ShoppingCart import ShoppingCart


@pytest.fixture
def computer():
    return Article(1, "computer", 100, "STANDARD")

@pytest.fixture
def glass():
    return Article(2, "glass", 20, "STANDARD")

@pytest.fixture
def phone():
    return Article(3, "phone", 200, "STANDARD")

@pytest.fixture
def special():
    return Article(4, "special", 150, "SPECIAL")

@pytest.fixture
def clearance():
    return Article(5, "clearance", 150, "CLEARANCE")

@pytest.fixture
def cart(glass):
    return ShoppingCart(1,
                        [glass, glass, glass],
                        "OPEN",
                        0,
                        []
                        )
@pytest.fixture
def medium_cart(phone):
    return ShoppingCart(2,
                        [phone],
                        "OPEN",
                        0,
                        []
                        )
@pytest.fixture
def big_cart(phone, computer, glass):
    return ShoppingCart(3,
                        [computer, phone, glass],
                        "OPEN",
                        0,
                        []
                        )
@pytest.fixture
def enormous_cart(phone):
    return ShoppingCart(3,
                        [phone, phone, phone],
                        "OPEN",
                        0,
                        []
                        )
@pytest.fixture
def little_special_cart(special):
    return ShoppingCart(4,
                        [special],
                        "OPEN",
                        0,
                        []
                        )
@pytest.fixture
def big_special_cart(special, phone):
    return ShoppingCart(4,
                        [special, phone, phone],
                        "OPEN",
                        0,
                        []
                        )

@pytest.fixture
def empty_cart(computer, glass, phone):
    return ShoppingCart(2,
                        [],
                        'OPEN',
                        0,
                        []
                        )

@pytest.fixture
def cart_with_cleareance_article(clearance, glass):
    return ShoppingCart(6,
                        [clearance, clearance, clearance],
                        'OPEN',
                        0,
                        []
                        )

class TestDiscountEngine:

    def test_is_cart_id(self, empty_cart):
        assert empty_cart.get_id() == 2

    def test_is_list_of_article(self, empty_cart):
        assert empty_cart.get_articles() == []

    def test_is_gross_total(self, empty_cart):
        assert empty_cart.get_gross_total() == 0

    def test_is_net_total(self, empty_cart):
        assert empty_cart.get_net_total() == 0

    def test_is_status(self, empty_cart):
        assert empty_cart.get_status() == 'OPEN'

    def test_is_discount(self, empty_cart):
        assert empty_cart.get_discount() == 0

    def test_history(self, empty_cart):
        assert empty_cart.get_history() == []

    def test_is_article_id(self, computer):
        assert computer.get_id() == 1

    def test_is_article_label(self, computer):
        assert computer.get_label() == "computer"

    def test_is_article_price(self, computer):
        assert computer.get_price() == 100

    def test_is_article_type(self, computer):
        assert computer.get_type() == "STANDARD"

    ## RULE ONE ###

    def test_if_status_open_can_modify_rules(self, cart):
        discount_engine = DiscountEngine(cart)
        assert discount_engine.get_cart().get_status() == "OPEN"
        discount_engine.modify_discount(10)
        assert discount_engine.get_cart().get_discount() == 10

    def test_if_status_validated_no_new_rules(self, cart):
       discount_engine = DiscountEngine(cart)
       discount_engine.get_cart().set_status("VALIDATED")
       with pytest.raises(AlreadyValidatedError, match="Error. Cart already validated"):
            discount_engine.modify_discount(10)

    def test_if_status_closed_no_modification(self, cart):
        discount_engine = DiscountEngine(cart)
        discount_engine.get_cart().set_status("LOCKED")
        with pytest.raises(LockedCartError, match="Error. Cart already locked"):
            discount_engine.modify_discount(10)

    ### RULES TWO DISCOUNT ###

    def test_if_total_inferior_to_hundred_discount_is_0(self, cart):
        discount_engine = DiscountEngine(cart)
        discount_engine.calcul_discount()
        assert discount_engine.get_cart().get_discount() == 0

    def test_if_total_superior_to_hundred_discount_is_5(self, medium_cart):
        discount_engine = DiscountEngine(medium_cart)
        discount_engine.calcul_discount()
        assert discount_engine.get_cart().get_discount() == 5

    def test_if_total_superior_to_three_hundred_discount_is_eight(self, big_cart):
        discount_engine = DiscountEngine(big_cart)
        discount_engine.calcul_discount()
        assert discount_engine.get_cart().get_discount() == 8

    def test_if_total_superior_to_fixe_hundred_discount_is_10(self, enormous_cart):
        discount_engine = DiscountEngine(enormous_cart)
        discount_engine.calcul_discount()
        assert discount_engine.get_cart().get_discount() == 10

    ### Rules IF SPECIAL ARTICLE ###

    def test_if_at_least_one_article_special_plus_three_discount(self, little_special_cart):
        discount_engine = DiscountEngine(little_special_cart)
        discount_engine.calcul_discount()
        assert little_special_cart.get_discount() == 8

    def test_if_at_least_one_article_special_plus_three_discount_plus_five_hundred_total(self, big_special_cart):
        discount_engine = DiscountEngine(big_special_cart)
        discount_engine.calcul_discount()
        assert big_special_cart.get_discount() == 18

    ### Rules 4 : Quantity Effect identic articles

    def test_if_more_than_3_identitcal_articles_cheaper_become_free(self, cart):
        discount_engine = DiscountEngine(cart)
        articles = discount_engine.get_cart().get_articles()
        assert articles[0].get_label() == articles[1].get_label()
        assert articles[1].get_label() == articles[2].get_label()
        assert articles[0].get_label() == articles[2].get_label()
        price_one_article = articles[0].get_price()
        expected_price = price_one_article * 2
        assert discount_engine.calcul_gross_total() == expected_price

    ###RULE 5 : Cleareance article
    #
    # def test_if_article_clearance_cant_be_free_and_not_participate_in_discount(self, cart_with_cleareance_article):
    #     discount_engine = DiscountEngine(cart_with_cleareance_article)
    #     articles = cart_with_cleareance_article.get_articles()
    #     assert articles[0].get_type() == "CLEARANCE"
    #     discount = cart_with_cleareance_article.get_discount()
    #     assert discount == 0
    #
    #     articles = cart_with_cleareance_article.get_articles()
    #     assert articles[0].get_label() == articles[1].get_label()
    #     assert articles[1].get_label() == articles[2].get_label()
    #     assert articles[0].get_label() == articles[2].get_label()
    #     expected_price = articles[0].get_price * 3
    #     assert cart_with_cleareance_article.get_gross_total == expected_price

    ### RUles 6 ceiling global for discount


    def test_discount_cant_be_superior_than_30_of_gross_total(self, cart):
        discount_engine = DiscountEngine(cart)
        discount_engine.modify_discount(35)
        assert discount_engine.get_cart().get_discount() == 30

    ### RULE 7 Automatic cart freeze
    def test_freeze_cart_if_discount_superior_25(self, cart):
        discount_engine = DiscountEngine(cart)
        discount_engine.modify_discount(26)
        assert discount_engine.get_cart().get_status() == "VALIDATED"
        with pytest.raises(AlreadyValidatedError, match="Error. Cart already validated"):
            discount_engine.modify_discount(15)

    ### Rule 8 History
    def test_cant_modify_history(self, cart):
        discount_engine = DiscountEngine(cart)
        discount_engine.calcul_discount()
        history = discount_engine.get_cart().get_history()
        with pytest.raises(TypeError):
            history[0][1] = "REFUSED"

    def test_chronological_order_history(self, big_cart):
        discount_engine = DiscountEngine(big_cart)
        discount_engine.calcul_discount()
        discount_engine.add_articles(Article(1, "computer", 100, "STANDARD"))
        discount_engine.calcul_discount()
        discount_engine.add_articles(Article(1, "computer", 100, "STANDARD"))
        discount_engine.calcul_discount()
        history = discount_engine.get_cart().get_history()
        assert history[0][4] <= history[1][4] <= history[2][4]



