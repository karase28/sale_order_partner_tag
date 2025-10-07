from odoo import models, fields, api
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # --- Główna metoda generująca nazwę ---
    def _assign_custom_name(self):
        for order in self:
            # Partner może być jeszcze nieustawiony
            if not order.partner_id:
                _logger.info("⚠️ Brak partnera - pomijam numerację dla %s", order.id)
                continue

            partner_tag = (order.partner_id.partner_tag or "XXX").upper()
            now = datetime.now()
            year = now.strftime("%Y")
            month = now.strftime("%m")

            # Sekwencja wewnętrzna (może być własna)
            seq_code = 'sale.order.sequence'
            next_number = self.env['ir.sequence'].next_by_code(seq_code) or '00000'

            # Format numeru: 2025/TAG/MM/00001
            order.name = f"{year}/{partner_tag}/{month}/{next_number}"
            _logger.info("🟢 Nadano nowy numer zamówienia: %s", order.name)

    # --- Nadpisanie create(), by użyć naszej numeracji zamiast Odoo ---
    @api.model
    def create(self, vals):
        order = super().create(vals)

        # Jeśli numer to standardowy Odoo (SO...), zamieniamy go
        if not order.name or order.name.startswith("SO"):
            _logger.info("🟡 Zastępuję numer Odoo własnym formatem dla zamówienia %s", order.id)
            order._assign_custom_name()

        return order

    # --- Dodatkowo: jeśli użytkownik zmieni partnera, nadaj numer ponownie ---
    def write(self, vals):
        res = super().write(vals)
        if 'partner_id' in vals:
            for order in self:
                # tylko jeśli numer to jeszcze SO... (czyli nie był nadany)
                if not order.name or order.name.startswith("SO"):
                    _logger.info("🟣 Partner zmieniony - ponowna numeracja dla %s", order.id)
                    order._assign_custom_name()
        return res
