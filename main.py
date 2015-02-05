import web
import paypalv2 as paypal

urls = [
    '/create', 'PaymentCreate',
    '/pay', 'PaymentExecute',
    '/payout', 'PayoutCreate',
    '/payout/(.*)', 'PayoutInfo'
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

class PayoutCreate:
    def GET(self):
        i = web.input()
        if not i.get('amts') or not i.get('usrs'):
            return web.badrequest()
        amts = i.get('amts').split(';')
        usrs = i.get('usrs').split(';')

        payout = paypal.createPayout(amts, usrs)
        if payout:
            web.seeother('/payout/%s'%payout.batch_header.payout_batch_id)

class PayoutInfo:
    def GET(self, pid):
        payout = paypal.getPayout(pid)
        payout.api = None
        return payout.__dict__

if __name__ == '__main__':
    app.run()
