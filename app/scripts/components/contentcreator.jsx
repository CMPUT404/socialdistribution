var React = require('react');
var Reflux = require('reflux');
var Markdown = require('markdown').markdown;
var TabbedArea = require('react-bootstrap').TabbedArea;
var TabPane = require('react-bootstrap').TabPane;
var Input = require('react-bootstrap').Input;
var PostActions = require('../actions/post');
var AuthorStore = require('../stores/author');
var moment = require('moment');

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
        var content = {
            content: this.state.content,
            format: this.state.format,
            timestamp: moment()
        };

        this.setState(this.getInitialState());

        if (this.props.forComment) {
            content["post_id"] = this.props.key;
            PostActions.newComment(content);
        } else {
            content["comments"] = [];
            PostActions.newPost(content);
        }
    },

    render: function() {
        return (
            <li className="col-md-12 media">
                <div className="media-left">
                    <img className="media-object" src={this.state.author.author_image}/>
                </div>
                <div className="media-body">
                    <h4 className="media-heading">New Post</h4>
                    <Input type="textarea" label="Content" value={this.state.content.content} onChange={this.contentChange} />
                    <Input type="select" label='Format' value={this.state.content.format} onChange={this.formatChange}>
                        <option value="markdown">Markdown</option>
                        <option value="text">Text</option>
                        <option value="HTML">HTML</option>
                    </Input>
                    <Input type="submit" value="Post" onClick={this.submitContent} />
                </div>
            </li>
        );
    }
});

module.exports = ContentCreator;
