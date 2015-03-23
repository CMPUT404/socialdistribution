import Reflux from 'reflux';
import Async from './async';

export default Reflux.createActions({
  'update'               : {},
  'register'             : Async,
  'logout'               : {},
  'login'                : Async,
  'checkAuth'            : Async,
  'fetchDetails'         : Async,
  'fetchPosts'           : Async,
  'createPost'           : Async,
  'deletePost'           : Async,
  'createComment'        : Async,
  'addFriend'            : {},
  'followFriend'         : Async
  // unfollow, unfriend?
});
