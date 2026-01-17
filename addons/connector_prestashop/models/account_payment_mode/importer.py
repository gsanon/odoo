# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class PaymentModeBatchImporter(Component):
    _name = "account.payment.mode.importer"
    _inherit = "prestashop.batch.importer"
    _apply_on = "account.payment.mode"

    def run(self, filters=None, **kwargs):
        if filters is None:
            filters = {}
        filters["display"] = "[id,payment]"
        return super().run(filters, **kwargs)

    def _import_record(self, record, **kwargs):
        """Create the missing payment method

        If we have only 1 bank journal, we link the payment method to it,
        otherwise, the user will have to create manually the payment mode.
        """
        payment_name = record["payment"]
        if self.binder_for().to_internal(payment_name):
            _logger.info("Payment mode '%s' already exists, skipping", payment_name)
            return

        method_xmlid = "account.account_payment_method_manual_in"
        payment_method = self.env.ref(method_xmlid, raise_if_not_found=False)
        if not payment_method:
            _logger.warning(
                "Cannot create payment mode '%s': manual payment method "
                "(%s) not found",
                payment_name,
                method_xmlid,
            )
            return

        journals = self.env["account.journal"].search(
            [
                ("type", "=", "bank"),
                ("company_id", "=", self.backend_record.company_id.id),
            ]
        )
        if len(journals) != 1:
            _logger.warning(
                "Cannot create payment mode '%s': expected exactly 1 bank journal "
                "for company '%s', found %d. Please configure exactly 1 bank journal "
                "or create the payment mode manually.",
                payment_name,
                self.backend_record.company_id.name,
                len(journals),
            )
            return

        self.model.create(
            {
                "name": payment_name,
                "company_id": self.backend_record.company_id.id,
                "bank_account_link": "fixed",
                "fixed_journal_id": journals.id,
                "payment_method_id": payment_method.id,
            }
        )
        _logger.info(
            "Created payment mode '%s' linked to journal '%s'",
            payment_name,
            journals.name,
        )
