odoo.define('invoice_xunnel.xunnel_sync', (require) => {
    'use strict';
    const viewRegistry = require('web.view_registry');
    const BillsListView = viewRegistry.get('account_bills_tree');
    const BillsListController = BillsListView.prototype.config.Controller;
    BillsListController.include({
        renderButtons() {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                this.$buttons.find('.o_button_xunnel_sync').click(() => {
                    this.do_action({
                        type: 'ir.actions.act_window',
                        res_model: 'xunnel.attachments.wizard',
                        target: 'new',
                        views: [[false, 'form']]
                    });
                });
            }
        }
    });
});
