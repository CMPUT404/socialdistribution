import React from 'react';
import { Route, DefaultRoute, NotFoundRoute } from 'react-router';

import NotFound from './routes/not-found';
import Register from './routes/register';
import Timeline from './routes/timeline';
import Layout from './routes/layout';
import Author from './routes/author';
import Login from './routes/login';
import Posts from './routes/posts';
import Users from './routes/users';

export default (
	<Route path="/" name="layout" handler={Layout}>
		<DefaultRoute name="timeline" handler={Timeline} />
		<Route name="author" path="/author/:id/:host?" handler={Author} />
		<Route name="login" handler={Login} />
		<Route name="register" handler={Register} />
		<Route name="posts" handler={Posts} />
		<Route name="users" handler={Users} />}
		<NotFoundRoute handler={NotFound} />
	</Route>
);
