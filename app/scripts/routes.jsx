import React from 'react';
import { Route, DefaultRoute, NotFoundRoute } from 'react-router';

import Layout from './routes/layout';
import Timeline from './routes/timeline';
import Author from './routes/author';
import Login from './routes/login';
import Register from './routes/register';
import Posts from './routes/posts';
import NotFound from './routes/not-found';

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
