# Copyright 2024 ForgeFlow
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models


class AccountBankStatementLine(models.Model):

    _inherit = "account.bank.statement.line"

    def action_open_journal_entry(self):
        self.ensure_one()
        if not self:
            return {}
        result = self.env["ir.actions.act_window"]._for_xml_id(
            "account.action_move_line_form"
        )
        res = self.env.ref("account.view_move_form", False)
        result["views"] = [(res and res.id or False, "form")]
        result["res_id"] = self.move_id.id
        return result


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    def open_entries(self):
        self.ensure_one()
        return {
            "name": _("Journal Items"),
            "view_mode": "tree,form",
            "res_model": "account.move.line",
            "view_id": False,
            "type": "ir.actions.act_window",
            "context": {"search_default_group_by_move": 1, "expand": 1},
            "search_view_id": self.env.ref("account.view_account_move_line_filter").id,
            "domain": [
                "&",
                ("parent_state", "=", "posted"),
                ("statement_id", "=", self.id),
            ],
        }
