from datetime import datetime
from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        """Nadpisanie metody create, by dodać numer wg taga partnera."""
        record = super().create(vals)
        record._assign_custom_name()
        return record

    def _assign_custom_name(self):
        """Generuje numerację: ROK/TAG/MIESIĄC/NUMER"""
        for order in self:
            if order.name and order.name != 'New':
                continue  # nie nadpisuj istniejących

            # ustal tag partnera
            partner_tag = (order.partner_id.partner_tag or "XXX").upper()

            # ustal bieżący rok i miesiąc
            now = datetime.now()
            year = now.strftime("%Y")
            month = now.strftime("%m")

            # znajdź sekwencję bazową
            seq_code = 'sale.order.sequence'
            next_number = self.env['ir.sequence'].next_by_code(seq_code) or '00000'

            order.name = f"{year}/{partner_tag}/{month}/{next_number}"
