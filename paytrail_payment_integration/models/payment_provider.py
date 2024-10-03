import logging
import pprint

import requests
from werkzeug import urls

from odoo import _, fields, models, service
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('paytrail', 'Paytrail')], ondelete={'paytrail': 'set default'}
    )
    paytrail_api_key = fields.Char(
        string="Paytrail API Key",
        help="The Test or Live API Key depending on the configuration of the provider",
        required_if_provider="paytrail", groups="base.group_system"
    )
    paytrail_merchant_id = fields.Char(
        string="Merchant id",
        required_if_provider="paytrail", groups="base.group_system"
    )
    paytrail_secret_key = fields.Char(
        string="Secret key",
        required_if_provider="paytrail", groups="base.group_system"
    )


    # def _paytrail_make_request(self, endpoint, data=None, method='POST'):
    #     """ Make a request at mollie endpoint.
    #
    #     Note: self.ensure_one()
    #
    #     :param str endpoint: The endpoint to be reached by the request
    #     :param dict data: The payload of the request
    #     :param str method: The HTTP method of the request
    #     :return The JSON-formatted content of the response
    #     :rtype: dict
    #     :raise: ValidationError if an HTTP error occurs
    #     """
    #     self.ensure_one()
    #     endpoint = f'/v2/{endpoint.strip("/")}'
    #     url = urls.url_join('https:// services.paytrail.com', endpoint)
    #
    #     odoo_version = service.common.exp_version()['server_version']
    #     module_version = self.env.ref('base.module_payment_paytrail').installed_version
    #     headers = {
    #         "Accept": "application/json",
    #         "Authorization": f'Bearer {self.paytrail_api_key}',
    #         "Content-Type": "application/json",
    #         # See https://docs.mollie.com/integration-partners/user-agent-strings
    #         # "User-Agent": f'Odoo/{odoo_version} MollieNativeOdoo/{module_version}',
    #     }
    #
    #     try:
    #         response = requests.request(method, url, json=data, headers=headers, timeout=60)
    #         try:
    #             response.raise_for_status()
    #         except requests.exceptions.HTTPError:
    #             _logger.exception(
    #                 "Invalid API request at %s with data:\n%s", url, pprint.pformat(data)
    #             )
    #             raise ValidationError(
    #                 "Paytrail: " + _(
    #                     "The communication with the API failed. Paytrail gave us the following "
    #                     "information: %s", response.json().get('detail', '')
    #                 ))
    #     except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
    #         _logger.exception("Unable to reach endpoint at %s", url)
    #         raise ValidationError(
    #             "Mollie: " + _("Could not establish the connection to the API.")
    #         )
    #     return response.json()
