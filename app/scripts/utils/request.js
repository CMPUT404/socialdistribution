import _ from 'lodash';
import Promise from 'bluebird';
import SuperAgent from 'superagent';

var __API__ = 'http://localhost:8000/';

SuperAgent.Request.prototype.promise = function createPromise(done, fail) {
  var self = this;
  return new Promise(function(resolve, reject) {
    self
      .set('Accept', 'application/json')
      .end( (res) => {
        var data = res.body;

        if (res.ok) {
          resolve(data);
        } else {
          if (_.has(data, 'detail')) {
            if (_.isString(data.detail)) {
              reject(data.detail);
            } else if (_.isArray(data.detail)) {
              reject(data.detail.join(' </br>'));
            } else {
              reject(_.keys(data.detail)
                      .map( k => k + ": " + res.body.detail[k] )
                      .join('</br>'));
            }
          } else if (_.has(data, 'message')){
            // GitHub error
            reject(data.message);
          } else {
            reject('Unrecognized error format!');
          }
        }
      } );
  }).then(done).catch(fail);
};

SuperAgent.Request.prototype.token = function(token) {
  if (!_.isNull(token)) {
    return this.set('Authorization', 'Token ' + token);
  } else {
    return this;
  }
};

SuperAgent.Request.prototype.host = function(host) {
  if (!_.isUndefined(host) && host !== __API__) {
    return this.set('Author-Host', host);
  } else {
    return this;
  }
};

export default SuperAgent;
