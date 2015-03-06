var React = require('react');
var Reflux = require('reflux');
var Check = require('check-types');
var RouterState = require('react-router').State;

var PostStore = require('../stores/post');
var AuthorStore = require('../stores/author');
var ContentViewer = require('./contentviewer');
var ContentCreator = require('./contentcreator');

// Represents a user's Profile view. It should only display a list
// of posts created by the author. If no authorId has been specified in the
// uri, this will display the logged in user's profile.
var Author = React.createClass({

  mixins: [Reflux.connect(AuthorStore), RouterState],

  getInitialState: function() {
    return {
      currentAuthor: AuthorStore.getCurrentAuthor()
    };
  },

  render: function() {
    // this comes from the RouterState mixin and lets us pull an author id out
    // of the uri so we can fetch their posts.
    var authorId = this.getParams().authorId;
    var currentAuthor = this.state.currentAuthor;
    var profile = false, contentCreator;

    // if the logged in author is trying to view his own page
    if (Check.object(currentAuthor) && authorId == currentAuthor.id) {
      contentCreator = <ContentCreator authorId={authorId} />;
      profile = true;
    }

    return (
      <div className="col-md-12" id="author">
        {contentCreator}
        <ContentViewer authorId={authorId} isProfile={profile} />
      </div>
    );
  }
});

module.exports = Author;
