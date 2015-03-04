var React = require('react');
var Reflux = require('reflux');
var Markdown = require('markdown').markdown;
var Moment = require('moment');
var ContentCreator = require('./contentcreator');
var CommentViewer = require('./commentviewer');
var Link = require('react-router').Link;

// Represents an individual comment or post.
var Content = React.createClass({

    convertMarkdown: function(markdown) {
        return Markdown.toHTML(markdown);
    },

    render: function() {

        console.log("shit");

        var timestamp = Moment(this.props.data.timestamp).fromNow();

        // If we're dealing with a post, append comments and comment creator to
        // the bottom
        var commentViewer;
        if (this.props.isPost === true) {
            commentViewer = <CommentViewer postId={this.props.data.id} comments={this.props.data.comments} />;
        }

        console.log(this.props.data);
        return (
            <div className="media post">
                {/**<div className="media-left">
                    <Link to="profile">
                        <img className="media-object author-image" src={this.props.data.author_image}/>
                    </Link>
                </div>
                <div className="media-body">
                    <h4 className="media-heading">{this.props.data.author_name}</h4>
                    <p>{this.props.data.content}</p>
                    <h6 className="timestamp">{timestamp}</h6>
                </div>*/}
                {commentViewer}
            </div>
        );
    }
});

module.exports = Content;
