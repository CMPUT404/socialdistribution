import Promise from 'bluebird';
import SuperAgent from 'superagent';

SuperAgent.Request.prototype.promise = function() {
  var self = this;

  return new Promise( function(resolve, reject) {
    self
      .set('Accept', 'application/json')
      .end( (res) => {
        if (res.ok) {
          resolve(res.body);
        } else {
          reject(res.body);
        }
      } );
  } );
};

export default SuperAgent;
