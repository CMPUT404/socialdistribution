'use strict';

var to5 = require("6to5");
var fs = require('fs');


/**
 * This preprocessor is for Jest testing.
 */

var ReactTools = require('react-tools');

module.exports = {
  process: function(src) {
    return ReactTools.transform(src);
  }
};
