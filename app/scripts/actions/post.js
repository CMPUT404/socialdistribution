var Reflux = require('reflux');

var Actions = Reflux.createActions([
  "newPost",
  "editPost",
  "deletePost",
  "newComment",
  "editComment",
  "deleteComment",
  "refreshPosts"
]);

module.exports = Actions;
