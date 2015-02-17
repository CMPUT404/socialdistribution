var React = require('react');
var Reflux = require('reflux');

var PostStore = require('../stores/post');
var ContentViewer = require('./contentviewer');

var Profile = React.createClass({

  mixins: [Reflux.connect(PostStore)],

  getInitialState: function() {
      return {
      };
  },

  render: function() {

    var profile = true;

    return (
      <div className="profile-view">
        <ContentViewer authorId={this.props.authorId} isProfile={profile} />
      </div>
    );
  }
});

module.exports = Profile;
