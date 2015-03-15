import Reflux from 'reflux';
import Promise from 'bluebird';
import { start } from './router';

Reflux.setPromise(Promise);

start();
