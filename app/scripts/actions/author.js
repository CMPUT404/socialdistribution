import Reflux from 'reflux';
import Request from '../utils/request';

var Author = Reflux.createActions({
  'update': {},
  'register': { asyncResult: true},
  "logout": { asyncResult: true },
  'login': { asyncResult: true},
  "getAuthorNameList": {}
});

Author.login.listen(function(username, password) {
  Request
    .get('http://localhost:8000/author/login/') //TODO: remove host
    .auth(username, password)
    .promise()
    .then( this.completed )
    .catch( this.failed );
} );

export default Author;
