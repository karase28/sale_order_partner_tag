import re
import string
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_tag = fields.Char(string="Tag/Nick", copy=False, index=True)

    @api.model
    def create(self, vals):
        """Po utworzeniu nowego kontrahenta — automatycznie przypisz unikalny TAG."""
        record = super().create(vals)
        if not record.partner_tag:
            record.partner_tag = record._generate_unique_tag()
        return record

    def _generate_unique_tag(self):
        """Generuje unikalny, 3-literowy tag z nazwy partnera."""

        def clean_name(name):
            # usuń frazy typu "sp. z o.o.", "s.c.", "ltd" itd.
            remove_words = [
                "sp", "z", "oo", "s.c", "s.a", "llc", "ltd", "inc",
                "gmbh", "sa", "co", "company", "corp", "corporation"
            ]
            name = re.sub(r"[^A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż ]", " ", name)
            parts = [p for p in name.upper().split() if p.lower() not in remove_words]
            return parts

        def from_multiple_words(parts):
            # np. "Inox Solution" → ISN
            letters = "".join([p[0] for p in parts])
            if len(letters) >= 3:
                return letters[:3]
            elif len(parts) == 2 and len(parts[1]) > 1:
                return (letters + parts[1][1])[:3]
            return (letters + "XXX")[:3]

        def from_single_word(word):
            # np. "Rubikon" → RBK (spółgłoski)
            word = re.sub(r"[^A-ZĄĆĘŁŃÓŚŹŻ]", "", word.upper())
            consonants = [c for c in word if c not in "AEIOUYĄĘÓ"]
            if len(consonants) >= 3:
                return "".join(consonants[:3])
            # jeśli mało spółgłosek — dopełnij literami
            return ("".join(consonants + list(word)))[:3]

        name = (self.name or "").strip()
        if not name:
            return "XXX"

        parts = clean_name(name)
        if len(parts) > 1:
            base_tag = from_multiple_words(parts)
        else:
            base_tag = from_single_word(parts[0])

        # jeśli unikalny — gotowe
        if not self.search([('partner_tag', '=', base_tag)], limit=1):
            return base_tag

        # w przeciwnym razie znajdź następny dostępny alfabetem (np. RBK → RBL)
        letters = string.ascii_uppercase
        for c in letters:
            candidate = base_tag[:2] + c
            if not self.search([('partner_tag', '=', candidate)], limit=1):
                return candidate

        raise ValueError("Brak dostępnych unikalnych 3-literowych tagów.")
