import Reflux from 'reflux';
import Marked from 'marked';
import Promise from 'bluebird';
import Highlight from 'highlight.js';

import { start } from './router';

Reflux.setPromise(Promise);

Marked.setOptions({
  highlight: (code) => Highlight.highlightAuto(code).value
});

start();
