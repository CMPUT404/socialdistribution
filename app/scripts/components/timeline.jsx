var React = require('react');
var Reflux = require('reflux');

var AuthorStore = require('../stores/author');
var ContentCreator = require('./contentcreator');
var ContentViewer = require('./contentviewer');

var Timeline = React.createClass({

  getInitialState: function() {
    return {
      author_id: AuthorStore.getCurrentAuthorId()
    };
  },

  render: function() {
    return (
      <div className="col-md-6 col-md-offset-3" id="timeline">
        <ContentCreator authorId={this.state.author_id} />
        <ContentViewer authorId={this.state.author_id} />
      </div>
    );
  }
});

module.exports = Timeline;
