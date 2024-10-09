from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo import _


from odoo import http
from odoo.http import request


class CustomerPortal(payment_portal.PaymentPortal):

    @http.route(['/my/orders/<int:order_id>/confirm'], type='http', auth="public", methods=['POST'], website=True)
    def portal_quote_confirm(self, order_id, access_token=None):
        order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        order_sudo.with_context(send_email=True).action_confirm()
        redirect_url = order_sudo.get_portal_url(query_string="&message=sign_ok")


        _message_post_helper(
            'sale.order',
            order_sudo.id,
            _('Your Quotation is confirmed'),
            token=access_token,
        )

        return request.redirect(redirect_url)
