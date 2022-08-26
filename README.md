# NextPay

This is a library for requesting to the https://nextpay.org purchase gateway.<br>
<h3>How to install : </h3>
<code>pip install nextpay</code>
<h3>How to use : </h3>

First import <code>NextPay</code> from <code>nextpay</code><br><br>
<code>from nextpay import NextPay</code><br><br>
Then you need to create an instance from NextPay class and pass it's parameters to it  in a function<br><br>

<pre>
from nextpay import NextPay


token = 'your_nextpay_token'
callback_uri = 'yourdomain.ir/verify'

def func():
    amount = '10000' # price of your product
    nextpay = NextPay(token, amount, callback_uri)
</pre>

Then you need to use purchase function
<pre>
from nextpay import NextPay


token = 'your_nextpay_token'
callback_uri = 'yourdomain.ir/verify'

def func():
    amount = '10000' # price of your product
    nextpay = NextPay(token, amount, callback_uri)
    trans_id = nextpay.purchase(order_id)
</pre>
 
Have in mind that <code>purchase</code> function take kwargs parameter. so read the docs.<br>
If every thing goes good you get a trans_id from that function.<br>
p.s : you have to create a gateway payment with that trans_id and give it to the client like this:<br>

<pre>
from nextpay import NextPay


token = 'your_nextpay_token'
callback_uri = 'yourdomain.ir/verify'

def func():
    amount = '10000' # price of your product
    nextpay = NextPay(token, amount, callback_uri)
    trans_id = nextpay.purchase(order_id)
    link = f"https://nextpay.org/nx/gateway/payment/{trans_id}"
</pre>

When your client complete the purchase nextpay will request to the address you gave to <code>callback_uri</code> variable<br>
When it does verify the purchase in your request handler like this :<br><br>
<code>nextpay.verify(trans_id)</code><br><br>
If everything goes good it will return True otherwise an exception will raise

You can also refund the payment like this :<br><br>
<code>nextpay.refund(trans_id)</code><br><br>
If everything goes good it will return True otherwise an exception will raise

