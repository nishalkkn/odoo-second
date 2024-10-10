from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.portal.controllers.mail import _message_post_helper

from odoo import http, _
from odoo.http import request


class CustomerPortal(payment_portal.PaymentPortal):

    @http.route(['/my/orders/<int:order_id>/confirm'], type='http', auth="public", methods=['POST'], website=True)
    def portal_quote_confirm(self, order_id, access_token=None):
        """function working on confirm button"""
        order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        order_sudo.with_context(send_email=True).action_confirm()

        # redirect url to show confirm message on the window
        redirect_url = order_sudo.get_portal_url(query_string="&message=sign_ok")

        # message shown on portal chatter when order confirmed
        _message_post_helper(
            'sale.order',
            order_sudo.id,
            _('The Order has been confirmed by OdooBot'),
            token=access_token,
        )

        return request.redirect(redirect_url)
