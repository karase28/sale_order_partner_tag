from odoo import models, api
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)
_logger.warning("✅ sale_order.py został ZAŁADOWANY do Odoo!")

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        _logger.warning("🟡 CREATE z sale_order_partner_tag: %s", vals)
        order = super().create(vals)

        if not order.partner_id:
            _logger.warning("⚠️ Brak partnera w zamówieniu %s", order.id)
            return order

        tag = (order.partner_id.partner_tag or "XXX").upper()
        now = datetime.now()
        order.name = f"{now.year}/{tag}/{now.month:02d}/{order.id:05d}"
        _logger.warning("🟢 Nadano numer: %s", order.name)
        return order
