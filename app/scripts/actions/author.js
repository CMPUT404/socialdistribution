import Reflux from 'reflux';
import Async from './async';

export default Reflux.createActions({
  'update'               : {},
  'register'             : Async,
  'logout'               : {},
  'login'                : Async,
  'getAuthorNameList'    : {},
  'checkAuth'            : Async,
  'fetchDetails'         : Async,
  'createPost'           : Async,
  'createComment'        : Async,
  'getAuthorAndListen'   : {},
  'unbindAuthorListener' : {},
  'subscribeTo'          : {},
  'unsubscribeFrom'      : {}
});
