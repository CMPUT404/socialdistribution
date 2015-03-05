var React = require('react');
var Reflux = require('reflux');
var Markdown = require('markdown').markdown;
var Input = require('react-bootstrap').Input;
var PostActions = require('../actions/post');
var AuthorStore = require('../stores/author');
var Moment = require('moment');
var Link = require('react-router').Link;

// Responsible for creating posts/comments and notifying the Post store when
// this happens.
var ContentCreator = React.createClass({

    getInitialState: function() {
        return {
            content: this.defaultContent(),
            author: AuthorStore.getCurrentAuthor()
        };
    },

    defaultContent: function () {
        return {
            format: "markdown",
            content: ""
        };
    },

    formatChange: function(event) {
        this.setState({format: event.target.value});
    },

    contentChange: function(event) {
        this.setState({content: event.target.value});
    },

    submitContent: function() {

        // capture the current content in our inputs
        var content = {
            content: this.state.content,
            format: this.state.format,
            timestamp: Moment.unix()
        };

        // reset content state now that we have it stored
        this.setState(this.getInitialState());

        // populate content with appropriate metadata
        if (this.props.forComment) {
            content["post"] = this.props.post;
            PostActions.newComment(content);
        } else {
            content["comments"] = [];
            PostActions.newPost(content);
        }
    },

    render: function() {
        return (
            <div className="media">
                <div className="media-left">
                    <Link to="profile">
                        <img className="media-object author-image" src={this.state.author.author_image}/>
                    </Link>
                </div>
                <div className="media-body content-creator">
                    <Input type="textarea" placeholder="Say something witty..." value={this.state.content.content} onChange={this.contentChange} />
                    <Input type="select" label='Format' value={this.state.content.format} onChange={this.formatChange}>
                        <option value="markdown">Markdown</option>
                        <option value="text">Text</option>
                        <option value="HTML">HTML</option>
                    </Input>
                    <Input type="submit" value="Post" onClick={this.submitContent} />
                </div>
            </div>
        );
    }
});

module.exports = ContentCreator;
