var React = require('react');
var Router = require('react-router');
var Route = Router.Route;
var DefaultRoute = Router.DefaultRoute;

var Layout = require('./components/layout');
var Timeline = require('./components/timeline');
var Author = require('./components/author');
var Login = require('./components/login');

var routes = (
	<Route name="timeline" path="/" handler={Layout}>
		<DefaultRoute handler={Timeline} />
		<Route name="author" path="/author/:authorId" handler={Author} />
		<Route name="login" handler={Login} />
	</Route>
);

// Don't touch this, define routes above
exports.start = function() {
	// TODO: Use Router.HistoryLocation for prod
	// Gulp webserver doesn't support this properly for dev
  Router.run(routes, function (Handler) {
		React.render(<Handler />, document.body);
	});
}
