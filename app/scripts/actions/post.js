import Reflux from 'reflux';
import Async from './async';

export default Reflux.createActions({
  "getTimeline"    : Async,
  "getPublicPosts" : Async
});
