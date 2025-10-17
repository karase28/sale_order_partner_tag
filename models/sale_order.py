from odoo import models, api, _
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        """Nadpisanie tworzenia zamówienia sprzedaży, aby dodać tag klienta do numeru dokumentu."""
        order = super().create(vals)

        # --- jeśli nie ma partnera, pomiń ---
        if not order.partner_id:
            return order

        # --- pobierz kolejny numer z sekwencji Odoo ---
        # sequence_number = self.env['ir.sequence'].next_by_code('sale.order')
        # if not sequence_number:
        #     _logger.warning("❌ Nie udało się pobrać numeru z ir.sequence (sale.order)")
        #     return order

        # --- pobierz tag klienta (jeśli nie ma, użyj 'XXX') ---
        partner_tag = order.partner_id.partner_tag or 'XXX'
        old_name = order.name

        # --- wstaw tag po 'OI_ZAM/' jeśli występuje ---
        if "OI_ZAM/" in old_name:
            new_name = old_name.replace("OI_ZAM/", f"OI_ZAM/{partner_tag}/")
        else:
            # Jeśli format jest inny, spróbuj dodać po pierwszym '/' po roku
            parts = old_name.split('/')
            if len(parts) >= 3:
                parts.insert(2, partner_tag)
                new_name = '/'.join(parts)
            else:
                new_name = f"{old_name}/{partner_tag}"

        # --- ustaw nowy numer zamówienia ---
        order.name = new_name

        # --- logi dla diagnostyki ---
        _logger.info(f"🟡 Zastępuję numer Odoo własnym formatem dla zamówienia {order.id}")
        _logger.info(f"🟢 Nadano nowy numer zamówienia: {new_name}")

        return order
