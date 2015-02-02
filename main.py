import web
import paypal

urls = [
    '/create', 'PaymentCreate',
    '/pay', 'PaymentExecute'
]
app = web.application(urls, globals())

class PaymentCreate:
    def GET(self):
        i = web.input()

        if not i.get('amt') or not i.get('des'):
            return web.badrequest()
        amt = i.amt
        des = i.des

        res = paypal.createPayment(amt, des)
        if type(res) == str:
            return web.seeother(res)
        else:
            return web.notfound()

class PaymentExecute:
    def GET(self):
        i = web.input()
        if not i.get('paymentId') or not i.get('PayerID'):
            return web.badrequest()
        id_payment = i.get('paymentId')
        id_payer = i.get('PayerID')

        res = paypal.executePayment(id_payment, id_payer)
        if type(res) is str:
            return { 'success': True }
        else:
            return { 'error': res }

if __name__ == '__main__':
    app.run()
