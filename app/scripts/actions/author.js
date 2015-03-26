import Reflux from 'reflux';
import Async from './async';

export default Reflux.createActions({
  'update'               : {},
  'register'             : Async,
  'logout'               : {},
  'login'                : Async,
  'checkAuth'            : Async,
  'fetchAuthor'          : Async,
  'createPost'           : Async,
  'deletePost'           : Async,
  'createComment'        : Async,
  'addFriend'            : Async,
  'followFriend'         : Async,
  'unfollowFriend'       : Async,

  // unfollow, unfriend?
});
