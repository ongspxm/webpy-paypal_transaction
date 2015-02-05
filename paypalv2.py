import time
import paypalrestsdk

PP_CLIENT_ID = '<client_id>'
PP_CLIENT_SECRET = '<client_secret>'

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
            'return_url': PP_URL_RETURN,
            'cancel_url': PP_URL_CANCEL
        }
    })

    if payment.create():
        href = [str(l.href) for l in payment.links if l.method == 'REDIRECT'][0]
        return str(href)
    else:
        return payment.error

def getPayment(pid):
    try:
        return paypalrestsdk.Payment.find(pid)
    except paypalrestsdk.ResourceNotFound as e:
        return None

def executePayment(pid, uid):
    payment = getPayment(pid)

    if not payment:
        return None

    if payment.execute({"payer_id": uid}):
        return str(payment.id)
    else:
        return payment.error

def createPayout(amts, usrs, subject='You have a payment', note='Thank you.', currency='SGD'):
    if type(usrs) != list:
        usrs = [usrs]

    if type(amts) != list:
        amts = [amts]*len(usrs)

    if len(usrs)!=len(amts):
        raise Exception('Malformed function call')

    items = []
    for usr, amt in zip(usrs, amts):
        items.append({
            'recipient_type': 'EMAIL',
            'amount':{
                'value': amt,
                'currency': currency
            },
            'receiver': usr,
            'note': note,
            'sender_item_id': 'item_%d'%len(items)
        })

    payout = paypalrestsdk.Payout({
        'sender_batch_header':{
            'sender_batch_id': str(int(time.time())),
            'email_subject': subject
        },
        'items': items
    })

    if payout.create():
        print 'Payout success'
        return payout
    else:
        print payout.error

def getPayout(pid):
    try:
        payout = paypalrestsdk.Payout.find(pid)
        return payout
    except paypalrestsdk.ResourceNotFound as e:
        return None

if __name__=='__main__':
    payout = createPayout(1.0, 'ongspxm@gmail.com')
    print payout.batch_header.payout_batch_id
