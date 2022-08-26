class InvalidKey(Exception):
    pass


class InvalidTransId(Exception):
    pass


class InvalidCallbackUri(Exception):
    pass


class InvalidToken(Exception):
    pass


class InvalidPrice(Exception):
    pass


class PurchaseDeclined(Exception):
    pass


class PurchaseCanceled(Exception):
    pass


class PurchaseAlreadyMade(Exception):
    pass


class RefundFailed(Exception):
    pass


class NotEnoughBalance(Exception):
    pass


class UnknownHandled(Exception):
    pass
