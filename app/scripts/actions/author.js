import Reflux from 'reflux';

var async = { children: ['complete', 'fail'] };

var Author = Reflux.createActions({
  'update'               : {},
  'register'             : async,
  'logout'               : {},
  'login'                : async,
  'getAuthorNameList'    : {},
  'checkAuth'            : async,
  'fetchDetails'         : async,
  'createPost'           : async,
  'createComment'        : async,
  'getAuthorAndListen'   : {},
  'unbindAuthorListener' : {},
  'subscribeTo'          : {},
  'unsubscribeFrom'      : {}
});

export default Author;
