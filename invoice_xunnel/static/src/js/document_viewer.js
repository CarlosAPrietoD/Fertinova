odoo.define('invoice_xunnel.document_viewer', (require) => {

    const DocumentsViewer = require('mail.DocumentViewer');
    const ajax = require('web.ajax');
    const { qweb } = require('web.core');

    DocumentsViewer.include({
        xmlDependencies: [
            '/invoice_xunnel/static/src/xml/templates.xml'
        ],
         events: Object.assign({
            'click pre.prettyprint .atn, pre.prettyprint .atv': 'copy_attribute'
        }, DocumentsViewer.prototype.events)
        , init(parent, attachments, activeAttachmentID){
            this._super.apply(this, arguments);
            this.attachment = _.filter(attachments, function(attachment) {
                var match = attachment.type == 'url' ? attachment.url.match("(youtu|.png|.jpg|.gif)") : attachment.mimetype.match("(image|video|application/pdf|text)");
                if (match) {
                    attachment.type = match[1];
                    if (match[1].match("(.png|.jpg|.gif)")) {
                        attachment.type = 'image';
                    }
                    if (match[1] === 'youtu') {
                        var youtube_array = attachment.url.split('/');
                        var youtube_token = youtube_array[youtube_array.length-1];
                        if (youtube_token.indexOf('watch') !== -1) {
                            youtube_token = youtube_token.split('v=')[1];
                            var amp = youtube_token.indexOf('&')
                            if (amp !== -1){
                                youtube_token = youtube_token.substring(0, amp);
                            }
                        }
                        attachment.youtube = youtube_token;
                    }
                    return true;
                } else{
                    const match = attachment.type == 'url' ? false : attachment.mimetype.match("application/xml");
                    if (match) {
                        return true;
                    }
                }
            });
            this.activeAttachment = _.findWhere(attachments, {id: activeAttachmentID});
            this._reset();
        }, start(){
            this._super.apply(this, arguments);
            this._updateContent();
        }, _updateContent(){
            this._super.apply(this, arguments);
            let xmlViewer = $('.o_viewer_xml').eq(0);
            if(xmlViewer.length){
                const route = xmlViewer.data('src');
                ajax.post(route, {}).then((view) => {
                    const html = qweb.render('invoice_xunnel.xml_preview', { view });
                    xmlViewer.html(PR.prettyPrintOne(html.trim()));
                });
            }
        }, _onClose(ev){
            const target = $(ev.target);
            if(target.parents('.prettyprint').length || target.hasClass('prettyprint')){
                return true;
            }
            this._super(ev);
        }, copy_attribute(ev){
            ev.preventDefault();
            ev.stopPropagation();
            const target = $(ev.currentTarget);
            const text = target.hasClass('atv')
                ? this.get_target_value(target)
                : this.get_target_value(target.next().next());
            this.copy(text);
        }, get_target_value(element){
            return element.text().replace(/\"/g, '');
        }, copy(textContent) {
            const input = $("#copy");
            input.val(textContent);
            input.focus();
            input.select();
            document.execCommand("copy");
            $.notify('Data copied.', {
                className: 'alert alert-warning'
            });
        }
    });

    return DocumentsViewer;
});
