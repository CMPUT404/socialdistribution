/**
 * * Entry point into the app.
 * *
 * */

"use strict";

var React = require('react');
var Router = require('react-router');
var App = require('./components/Core/App.jsx');
var Home = require('./components/Home.jsx');

// TODO: move this to it's own file
var routes = (
    <Route handler={App} path="/">
        <DefaultRoute handler={Home} />
        <NotFoundRoute handler={NotFound}/>
    </Route>
);

Router.run(routes, Router.HistoryLocation, function (Handler) {
    React.render(<Handler/>, document.getElementById("app"));
});
