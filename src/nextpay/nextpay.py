from typing import Literal, Union, Optional, TypedDict, Dict, Any

import requests

import exceptions


class PurchageKWargs(TypedDict):
    currency:  Optional[Literal['IRT', 'IRR']]
    phone: str
    custom_json_fields: Dict[Any, Any]  # I'm not sure about keys and values for this item
    payer_name: str
    payer_desc: str
    auto_verify: Literal[True]
    allowed_card: str
  

class NextPay:
    # setting headers
    headers = {
        'User-Agent': 'PostmanRuntime/7.26.8',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # get token and money amount from user
    def __init__(
            self,
            token: str,
            amount: Union[str, int],
            callback_uri: str
    ):
        """
        Create purchase instance.\n
        Params:
            token (str): your nextpay token.\n
            amount (str | int): amount of your purchase.\n
            callback_uri (str): the address to your domain or ip for callback from nextpay.\n
        """
        self.token, self.amount, self.callback_uri = token, amount, callback_uri

    # creating the purchase page
    def purchase(
            self,
            order_id: str,
            **kwargs: PurchageKWargs
    ):
        """
        Send purchase request to NextPay api.\n
        Params:
            order_id (str): unique id for purchase.

        Kwargs:
            currency ('IRT' | 'IRR'): Currency type.\n
            phone (str): Phone number of user.\n
            custom_json_fields(dict): a dict to pass to the api.\n
            payer_name(str): name of the payer.\n
            payer_desc(str): description of payer.\n
            auto_verify(True): automatically verify the request.\n
            allowed_card(str): only allow this card to purchase.\n

        """

        url = "https://nextpay.org/nx/gateway/token"

        # creating data for url
        data = {
            'api_key': self.token,
            'amount': self.amount,
            'order_id': order_id,
            'callback_uri': self.callback_uri
        }

        for key, value in kwargs.items():
            if key in ['currency', 'phone', 'custom_json_fields', 'payer_name', 'payer_desc', 'auto_verify', 'allowed_card']:
                data[key] = value
            else:
                raise exceptions.InvalidKey(f"key {key} is invalid for NextPay.org")

        respond = requests.post(url, data, headers=self.headers)
        result = respond.json()

        # if page created successfully
        if result['code'] == -1:
            # purchase_page = f"https://nextpay.org/nx/gateway/payment/{result['trans_id']}"
            return result['trans_id']  # type: str

        elif result['code'] == -32:
            raise exceptions.InvalidCallbackUri("callback_uri is invalid")

        elif result['code'] == -73:
            raise exceptions.InvalidCallbackUri("callback_uri has a server error or its too long")

        elif result['code'] in [-33, -35, -38, -39, -40, -47]:
            raise exceptions.InvalidToken(f"Token {self.token} is invalid. error code : {result['code']}")

        else:
            raise exceptions.UnknownHandled(f"Un-handled error code : {result['code']}")

    # verifying the purchase
    def verify(
            self,
            trans_id: str,
            currency: Optional[Literal['IRT', 'IRR']] = None
    ) -> bool:
        """
            Verifying the user purchase.\n
            Params:
                trans_id (str): the trans_id your got from purchase function.\n
                currency ('IRT' | 'IRR'): Currency type.
            Returns: bool

        """

        url = "https://nextpay.org/nx/gateway/verify"

        # creating data for url
        data = {
            'api_key': self.token,
            'amount': self.amount,
            'trans_id': trans_id
        }

        # giving external data if user provided it
        if currency in ['IRT', 'IRR']:
            data['currency'] = currency

        respond = requests.post(url, data, headers=self.headers)
        result = respond.json()

        if result['code'] == 0:
            return True

        elif result['code'] == -2:
            raise exceptions.PurchaseDeclined("Purchase declined by user or bank")

        elif result['code'] == -4:
            raise exceptions.PurchaseCanceled("Purchase canceled")

        elif result['code'] == -24:
            raise exceptions.InvalidPrice("Entered price is invalid")

        elif result['code'] == -25:
            raise exceptions.PurchaseAlreadyMade("Purchase is already finished and paid")

        elif result['code'] == -27:
            raise exceptions.InvalidTransId("trans_id is invalid")

        else:
            raise exceptions.UnknownHandled(f"Un-handled error code : {result['code']}")

    def refund(self, trans_id: str) -> bool:
        url = "https://nextpay.org/nx/gateway/verify"

        # creating data for url
        data = {
            'api_key': self.token,
            'amount': self.amount,
            'trans_id': trans_id,
            'refund_request': 'yes_money_back'
        }

        respond = requests.post(url, data, headers=self.headers)
        result = respond.json()

        if result['code'] == -90:
            return True

        elif result['code'] in [-91, -92]:
            raise exceptions.RefundFailed("Refund failed")

        elif result['code'] == -93:
            raise exceptions.NotEnoughBalance('Not enough balance to refund')

        elif result['code'] == -27:
            raise exceptions.InvalidTransId("trans_id is invalid")

        else:
            raise exceptions.UnknownHandled(f"Un-handled error code : {result['code']}")
