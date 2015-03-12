import _ from 'lodash';
import Promise from 'bluebird';
import SuperAgent from 'superagent';

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
          if (_.has(data, 'error')) {
            if (_.isString(data.error)) {
              reject(data.error);
            } else if (_.isArray(data.error)) {
              reject(data.error.join(' </br>'));
            } else {
              reject(_.keys(data.error)
                      .map( k => k + ": " + res.body.error[k] )
                      .join('</br>'));
            }
          }  else {
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

export default SuperAgent;
