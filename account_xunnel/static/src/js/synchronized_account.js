odoo.define('account_xunnel.synchronized_accounts', (require) => {
    "use strict";

    const Action = require('web.AbstractAction');
    const core = require('web.core');

    const SyncrhonizedAccounts = Action.extend({
        template: 'account_xunnel.synchronized_accounts',
        init(parent, ctx){
            this.message = ctx.message;
            this.message_class = ctx.message_class;
            return this._super.apply(this, arguments);
        }, _close_action(){
            this.do_action({type: 'ir.actions.act_window_close'});
        }, renderButtons($node) {
            this.$buttons = $(core.qweb.render("account_xunnel.synchronized_accounts_footer", {'widget': this}));
            this.$buttons.find('.js_cancel').click(() => this.do_action({type: 'ir.actions.act_window_close'}));
            this.$buttons.appendTo($node);
        }
    });

    core.action_registry.add('account_xunnel.syncrhonized_accounts', SyncrhonizedAccounts)
})
