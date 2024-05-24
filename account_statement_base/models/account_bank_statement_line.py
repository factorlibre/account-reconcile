from odoo import _, models


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
