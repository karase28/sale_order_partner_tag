from odoo import models, api
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)
_logger.warning("✅ sale_order.py został ZAŁADOWANY do Odoo!")

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        _logger.warning("🟡 CREATE z sale_order_partner_tag: %s", vals)
        order = super().create(vals)

        # --- jeśli brak partnera, pomijamy numerację ---
        if not order.partner_id:
            _logger.warning("⚠️ Brak partnera w zamówieniu %s", order.id)
            return order

        # --- pobranie taga klienta ---
        tag = (order.partner_id.partner_tag or "XXX").upper()
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")

        # --- pobranie następnego numeru z sekwencji ---
        seq_code = 'sale.order'  # standardowa sekwencja zamówień
        next_seq = self.env['ir.sequence'].next_by_code(seq_code)

        if not next_seq:
            _logger.warning("⚠️ Brak zdefiniowanej sekwencji %s – używam fallbacku", seq_code)
            next_seq = f"{order.id:05d}"

        # --- budowanie numeru ---
        order.name = f"{year}/{tag}/{month}/{next_seq}"
        _logger.warning("🟢 Nadano numer zamówienia: %s", order.name)

        return order
