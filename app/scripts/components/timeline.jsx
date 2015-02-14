var React = require('react');
var Reflux = require('reflux');

var AuthorStore = require('../stores/author');
var PostViewer = require('./postviewer');
var ContentCreator = require('./contentcreator');

var Timeline = React.createClass({

  getInitialState: function() {
    return {
      author: AuthorStore.getAuthor()
    };
  },

  render: function() {
    return (
      <div id="timeline">
        <h4>Your Timeline</h4>
        <ContentCreator authorId={this.state.author.id} />
        <PostViewer authorId={this.state.author.id} />
      </div>
    );
  }
});

module.exports = Timeline;
