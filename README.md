# NextPay

This is a library for requesting to the https://nextpay.org purchase gateway.
### How to install :
`pip install nextpay`
### How to use :

First import `NextPay` from `nextpay`

`from nextpay import NextPay`

Then you need to create an instance from NextPay class and pass it's parameters to it  in a function


```python
from nextpay import NextPay


token = 'your_nextpay_token'
callback_uri = 'yourdomain.ir/verify'

def func():
    amount = '10000' # price of your product
    nextpay = NextPay(token, amount, callback_uri)
```

Then you need to use purchase function
```python
from nextpay import NextPay


token = 'your_nextpay_token'
callback_uri = 'yourdomain.ir/verify'

def func():
    amount = '10000' # price of your product
    nextpay = NextPay(token, amount, callback_uri)
    trans_id = nextpay.purchase(order_id)
```
 
Have in mind that `purchase` function take kwargs parameter. so read the docs.
If every thing goes good you get a trans_id from that function.
p.s : you have to create a gateway payment with that trans_id and give it to the client like this:

```python
from nextpay import NextPay


token = 'your_nextpay_token'
callback_uri = 'yourdomain.ir/verify'

def func():
    amount = '10000' # price of your product
    nextpay = NextPay(token, amount, callback_uri)
    trans_id = nextpay.purchase(order_id)
    link = f"https://nextpay.org/nx/gateway/payment/{trans_id}"
```

When your client complete the purchase nextpay will request to the address you gave to `callback_uri` variable
When it does verify the purchase in your request handler like this :

`nextpay.verify(trans_id)`

If everything goes good it will return True otherwise an exception will raise

You can also refund the payment like this :

`nextpay.refund(trans_id)`

If everything goes good it will return True otherwise an exception will raise

