import paypalrestsdk

PP_CLIENT_ID = 'AaPL5RDcdjfSTOQ4-plrBDKo4-wU4rxtzMH4Brqm2Pfg23ySf1Wqf9qiKGnW'
PP_CLIENT_SECRET = 'EM5skRB5NrmuvIXVGHra7r9W7181JVGuxAMSdOnnnd3fu53a-ulR7NySYUWo'

PP_URL_RETURN = 'http://localhost:8080/pay'
PP_URL_CANCEL = 'http://localhost:8080/'

paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": PP_CLIENT_ID,
    "client_secret": PP_CLIENT_SECRET
})

def createPayment(amt, description='', currency='SGD'):
    payment = paypalrestsdk.Payment({
        'intent': 'sale',
        'payer': {
            'payment_method': 'paypal'
        },
        'transactions': [{
            'amount': {
                'total': '%.2f'%float(amt),
                'currency': currency
            },
            'description': description
        }],
        'redirect_urls':{
            'return_url':PP_URL_RETURN,
            'cancel_url':PP_URL_CANCEL
        }
    })

    if payment.create():
        href = [str(l.href) for l in payment.links if l.method == 'REDIRECT'][0]
        return str(href)
    else:
        return payment.error

def executePayment(pid, uid):
    payment = paypalrestsdk.Payment.find(pid)

    if payment.execute({"payer_id": uid}):
        return str(payment.id)
    else:
        return payment.error

if __name__ == '__main__':
    print createPayment(2.00, 'Random stuff')
