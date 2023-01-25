# © 2018 Eficent Business and IT Consulting Services S.L. (www.eficent.com)
# © 2022 FactorLibre - Hugo Santos <hugo.santos@factorlibre.com>
# © 2023 FactorLibre - Luis J. Salvatierra <luis.salvatierra@factorlibre.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, api
from odoo.osv import expression


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    def get_move_lines_for_reconciliation(
            self, partner_id=None, excluded_ids=None, str=False, offset=0,
            limit=None, additional_domain=None, overlook_partner=False):
        if additional_domain is None:
            additional_domain = []
        additional_domain = expression.AND([additional_domain, [
            ('account_id.exclude_bank_reconcile', '=', False)
        ]])
        am_lines = super(AccountBankStatementLine, self).\
            get_move_lines_for_reconciliation(
            partner_id=partner_id, excluded_ids=excluded_ids, str=str,
            offset=offset, limit=limit, additional_domain=additional_domain,
            overlook_partner=overlook_partner)
        return am_lines

    @api.multi
    def get_reconciliation_proposition(self, excluded_ids=None):
        ctx = self._context.copy()
        ctx["exclude_bank_reconcile"] = True
        return super(
            AccountBankStatementLine, self.with_context(ctx)
        ).get_reconciliation_proposition(excluded_ids=excluded_ids)

    def _get_common_sql_query(
        self, overlook_partner=False, excluded_ids=None, split=False
    ):
        query = super()._get_common_sql_query(
            overlook_partner=overlook_partner, excluded_ids=excluded_ids, split=split
        )
        if self._context.get("exclude_bank_reconcile", False):
            exclude_query = " AND acc.exclude_bank_reconcile IS NOT true"
            if split:
                select_clause, from_clause, where_clause = query
                where_clause += exclude_query
                query = (select_clause, from_clause, where_clause)
            else:
                query += exclude_query
        return query
