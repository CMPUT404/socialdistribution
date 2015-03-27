import React from 'react';
import { Route, DefaultRoute, NotFoundRoute } from 'react-router';

import Layout from './components/routes/layout';
import Timeline from './components/routes/timeline';
import Author from './components/routes/author';
import Login from './components/routes/login';
import Register from './components/routes/register';
import Posts from './components/routes/posts';
import NotFound from './components/routes/not-found';

export default (
	<Route path="/" name="layout" handler={Layout}>
		<DefaultRoute name="timeline" handler={Timeline} />
		<Route name="author" path="/author/:id/:host?" handler={Author} />
		<Route name="login" handler={Login} />
		<Route name="register" handler={Register} />
		<Route name="posts" handler={Posts} />
		<NotFoundRoute handler={NotFound} />
	</Route>
);
