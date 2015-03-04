var RouterState = require('react-router').State;
var React = require('react');
var Reflux = require('reflux');
var PostStore = require('../stores/post');
var ContentViewer = require('./contentviewer');
var ContentCreator = require('./contentcreator');

// Represents a user's Profile view. It should only display a list
// of posts created by the author. If no authorId has been specified in the
// uri, this will display the logged in user's profile.
var Profile = React.createClass({

  mixins: [Reflux.connect(PostStore), RouterState],

  getInitialState: function() {
      return {
      };
  },

  render: function() {

    // this comes from the RouterState mixin and lets us pull an author id out
    // of the uri so we can fetch their posts.
    var authorId = this.getParams().authorId;
    var profile = true;

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
