import React from 'react';
import Reflux from 'reflux';
import Marked from 'marked';
import Routes from './routes'
import Promise from 'bluebird';
import Router from 'react-router';
import Highlight from 'highlight.js';

import { RouterLocation } from './settings';

Reflux.setPromise(Promise);

Marked.setOptions({
  highlight: (code) => Highlight.highlightAuto(code).value
});

Router.run(Routes, RouterLocation(),
           Handler => React.render(<Handler />, document.getElementById('app')));
