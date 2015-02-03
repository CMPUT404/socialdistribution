/*
 * * AppDispatcher
 * *
 * * A singleton that operates as the central hub for application updates.
 * */
"use strict";

var Dispatcher = require('flux').Dispatcher;

// Shim for ES6 Object.assign. Merges objects together.
var assign = require('object-assign');
var AppDispatcher = assign(new Dispatcher(), {

    /**
    * A bridge function between the views and the dispatcher, marking the action
    * as a view action. Another variant here could be handleServerAction.
    * @param {object} action The data coming from the view.
    */
    handleViewAction: function(action) {
        this.dispatch(action);
    },
    /**
    * @param {object} action The server generate action.
    */
    handleServerAction: function(action) {
        this.dispatch(action);
    }
});

module.exports = AppDispatcher;
