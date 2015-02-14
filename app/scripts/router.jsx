var React = require('react');
var Router = require('react-router');
var Route = Router.Route;
var DefaultRoute = Router.DefaultRoute;

var Layout = require('./components/layout');
var Scoresheet = require('./components/scoresheet/scoresheet');

var routes = (
	<Route name="layout" path="/" handler={Layout}>
		<DefaultRoute handler={Scoresheet} />
	</Route>
);

exports.start = function() {
  Router.run(routes, function (Handler) {
		React.render(<Handler />, document.body);
	});
}
