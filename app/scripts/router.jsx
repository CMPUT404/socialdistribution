import React from 'react';
import { default as Router, Route, DefaultRoute } from 'react-router';

import Layout from './components/routes/layout';
import Timeline from './components/routes/timeline';
import Author from './components/routes/author';
import Login from './components/routes/login';
import Register from './components/routes/register';
import Posts from './components/routes/posts';

var routes = (
	<Route path="/" name="layout" handler={Layout}>
		<DefaultRoute name="timeline" handler={Timeline} />
		<Route name="author" path="/author/:id/:host?" handler={Author} />
		<Route name="login" handler={Login} />
		<Route name="register" handler={Register} />
		<Route name="posts" handler={Posts} />
	</Route>
);

// Don't touch this, define routes above
export function start() {
	// TODO: Use Router.HistoryLocation for prod
	// Gulp webserver doesn't support this properly for dev
  Router.run(routes, function (Handler) {
		React.render(<Handler />, document.getElementById('app'));
	});
}
