odoo.define('invoice_xunnel.DocumentsKanbanModel', (require) => {
    "use strict";

    const KanbanModel = require('documents.DocumentsKanbanModel');

    KanbanModel.include({
        /**
         * @overrided This function was copy and pasted to override the original load of the
         * Documents's Kanban Model.
         *
         * The above in order to allow the Documents's kanban to be opened in a default folder.
         */
        load: function (params) {
            var self = this;
            var _super = this._super.bind(this);
            return this._fetchFolders(params.context).then(function (folders) {
                var defaultFolderID = folders.length ? folders[0].id : false;
                // Modified code.
                defaultFolderID = params.context.defaultFolderId || defaultFolderID;
                // Modified code end.
                params = _.extend({}, params, {
                    folderID: defaultFolderID,
                    folders: folders,
                });
                params.domain = params.domain || [];
                params.searchDomain = params.domain;
                params.domain = self._addFolderToDomain(params.domain, params.folderID);
                var def = _super(params);
                return self._fetchAdditionalData(def, params).then(function (dataPointID) {
                    var dataPoint = self.localData[dataPointID];
                    dataPoint.folderID = params.folderID;
                    dataPoint.folders = params.folders;
                    dataPoint.isRootDataPoint = true;
                    dataPoint.searchDomain = params.searchDomain;
                    return dataPointID;
                });
            });
        },

        /**
         * @overrided This function was copy and pasted to override the original _addFolderToDomain of the
         * Documents's Kanban Model.
         *
         * The above in order to to prevent a domain [&] with two different folder_id
         */
        _addFolderToDomain: function (domain, folderID) {
            const found = domain.find(element => element[0] == 'folder_id' & element[1] == '=');
            
            if(!_.isArray(found))
                return domain.concat([['folder_id', '=', folderID]]);

            return domain;
        },
    });

    return KanbanModel;
});
