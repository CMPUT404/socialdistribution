import Reflux from 'reflux';

var Author = Reflux.createActions({
  'update': {},
  'register': { asyncResult: true },
  'logout': {},
  'login': { asyncResult: true },
  'getAuthorNameList': {},
  'checkAuth': {},
  'fetchDetails': { asyncResult: true },
  'getAuthorAndListen': {},
  'unbindAuthorListener': {},
  'subscribeTo': {},
  'unsubscribeFrom': {}
});

export default Author;
