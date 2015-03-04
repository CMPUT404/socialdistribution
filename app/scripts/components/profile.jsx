var RouterState = require('react-router').State;
var React = require('react');
var Reflux = require('reflux');
var PostStore = require('../stores/post');
var ContentViewer = require('./contentviewer');
var ContentCreator = require('./contentcreator');

var Profile = React.createClass({

  mixins: [Reflux.connect(PostStore), RouterState],

  getInitialState: function() {
      return {
      };
  },

  render: function() {

    var profile = true;
    var authorId = this.getParams().authorId;

    if (typeof authorId === 'undefined') {
      profile = false;
    }

    return (
      <div className="col-md-6 col-md-offset-3">
        <ContentCreator type="" />
        <ContentViewer authorId={this.props.authorId} isProfile={profile} />
      </div>
    );
  }
});

module.exports = Profile;
