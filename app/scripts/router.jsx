var React = require('react');
var Router = require('react-router');
var Route = Router.Route;
var DefaultRoute = Router.DefaultRoute;

var Layout = require('./components/layout');
var Timeline = require('./components/timeline');
var Profile = require('./components/profile');

var routes = (
	<Route name="timeline" path="/" handler={Layout}>
		<DefaultRoute handler={Timeline} />
		<Route name="profile" path="" handler={Profile} />
		<Route name="author" path=":authorId" handler={Profile} />
	</Route>
);

// Don't touch this, define routes above
exports.start = function() {
  Router.run(routes, function (Handler) {
		React.render(<Handler />, document.getElementById("app"));
	});
}
