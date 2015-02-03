var Action = require('./Action');
var AppDispatcher = require('../dispatcher/AppDispatcher');

/**
 * A base class for all server actions.
 */
module.exports = class ServerAction extends Action {
    handle() {
        AppDispatcher.handleServerAction(this);
    }
};
