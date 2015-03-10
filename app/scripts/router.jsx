import React from 'react';
import { default as Router, Route, DefaultRoute } from 'react-router';

import Layout from './components/layout';
import Timeline from './components/timeline';
import Author from './components/author';
import Login from './components/login';

var routes = (
	<Route path="/" name="timeline" handler={Layout}>
    <DefaultRoute handler={Timeline} />
    <Route name="author" path="/author/:id?" handler={Author} />
    <Route name="login" handler={Login} />
	</Route>
);

// Don't touch this, define routes above
export function start() {
	// TODO: Use Router.HistoryLocation for prod
	// Gulp webserver doesn't support this properly for dev
  Router.run(routes, function (Handler) {
		React.render(<Handler />, document.body);
	});
}
