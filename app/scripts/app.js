import React from 'react';
import Reflux from 'reflux';
import Marked from 'marked';
import Routes from './routes'
import Promise from 'bluebird';
import Router from 'react-router';
import Highlight from 'highlight.js';

Reflux.setPromise(Promise);

Marked.setOptions({
  highlight: (code) => Highlight.highlightAuto(code).value
});

// TODO: Use Router.HistoryLocation for prod
// Gulp webserver doesn't support this properly for dev
Router.run(Routes, Handler => React.render(<Handler />, document.getElementById('app')));
