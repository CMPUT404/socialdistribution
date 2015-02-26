var React = require('react');
var Reflux = require('reflux');
var Markdown = require('markdown').markdown;
var Moment = require('moment');
var ContentCreator = require('./contentcreator');
var CommentViewer = require('./commentviewer');

var Content = React.createClass({

    getInitialState: function () {
        return {
        };
    },

    convertMarkdown: function(markdown) {
        return Markdown.toHTML(markdown);
    },

    render: function() {
        var timestamp = Moment(this.props.data.timestamp).fromNow();

        // If we're dealing with a post, append comments and comment creator to
        // the bottom
        var commentViewer;
        if (typeof this.props.isPost === 'undefined') {
            commentViewer = <CommentViewer postId={this.props.data.id} comments={this.props.data.comments} />;
        }

        return (
            <li className="media post">
                <div className="media-left">
                    <img className="img-thumbnail author_image" src={this.props.data.author_image}/>
                </div>
                <div className="media-body">
                    <h4 className="media-heading">{this.props.data.author_name}</h4>
                    <p>{this.props.data.content}</p>
                    <h6 className="timestamp">{timestamp}</h6>
                </div>
                {commentViewer}
            </li>
        );
    }
});

module.exports = Content;
