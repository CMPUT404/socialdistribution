import Reflux from 'reflux';
import Async from './async';

export default Reflux.createActions({
  'update'               : Async,
  'register'             : Async,
  'logout'               : {},
  'login'                : Async,
  'checkAuth'            : {},
  'fetchAuthor'          : Async,
  'createPost'           : Async,
  'deletePost'           : Async,
  'createComment'        : Async,
  'addFriend'            : Async,
  'followFriend'         : Async,
  'unfollowFriend'       : Async,
  "getAuthors"           : Async,
});
