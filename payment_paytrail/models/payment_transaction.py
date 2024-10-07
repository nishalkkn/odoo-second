# -*- coding: utf-8 -*-

import datetime
import logging
import pprint

from werkzeug import urls

from odoo import _, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return Paytrail-specific rendering values.
        :param dict processing_values: The generic and specific processing values of the transaction
        :return: The dict of provider-specific rendering values
        :rtype: dict
        """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'paytrail':
            return res
        base_url = self.provider_id.get_base_url()
        redirect_url = urls.url_join(base_url, '/payment/paytrail/return')
        dt = datetime.datetime.now()
        items = []
        for line in self.sale_order_ids[0].order_line:
            items.append({
                'unitPrice': int(line.price_total) * 91,
                'units': line.product_uom_qty,
                'vatPercentage': line.tax_id.amount,
                'productCode': line.product_template_id.name,
                'deliveryDate': str(datetime.date.today())
            })
            line.price_total = int(line.price_total) * 91
            print('price total : ', line.price_total)

        amount = int(processing_values['amount']) * 91
        payload = {
            "stamp": str(dt.timestamp()),
            "reference": processing_values['reference'],
            "amount": amount,
            "currency": "EUR",
            "language": "EN",
            "items": items,
            "customer": {"email": "test.customer@example.com"},
            "redirectUrls": {
                "success": redirect_url,
                "cancel": redirect_url
            }
        }
        _logger.info("sending '/payments' request for link creation:\n%s", pprint.pformat(payload))
        payment_data = self.provider_id._paytrail_make_request('/payments', data=payload)
        print("payment_data : ", payment_data)
        self.provider_reference = payment_data.get('transactionId')
        checkout_url = payment_data['href']
        parsed_url = urls.url_parse(checkout_url)
        url_params = urls.url_decode(parsed_url.query)
        return {'api_url': checkout_url, 'url_params': url_params}

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on Paytrail data.

        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'paytrail' or len(tx) == 1:
            return tx

        tx = self.search(
            [('reference', '=', notification_data.get('checkout-reference')), ('provider_code', '=', 'paytrail')]
        )
        if not tx:
            raise ValidationError("Paytrail: " + _(
                "No transaction found matching reference %s.", notification_data.get('checkout-reference')
            ))
        return tx

    def _process_notification_data(self, notification_data):
        """ Override of payment to process the transaction based on Paytrail data.

        Note: self.ensure_one()

        :param dict notification_data: The notification data sent by the provider
        :return: None
        """
        super()._process_notification_data(notification_data)
        if self.provider_code != 'paytrail':
            return
        payment_status = notification_data.get('checkout-status')
        if payment_status in ['pending', 'delayed']:
            self._set_pending()

        elif payment_status == 'ok':
            self._set_done()
        elif payment_status == 'fail':
            self._set_canceled("Paytrail: " + _("Canceled payment with status: %s", payment_status))
        else:
            _logger.info(
                "received data with invalid payment status (%s) for transaction with reference %s",
                payment_status, self.reference
            )
            self._set_error(
                "Paytrail: " + _("Received data with invalid payment status: %s", payment_status)
            )
