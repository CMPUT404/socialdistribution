import React from 'react';
import { addons } from 'react/addons';
import GitHubEvent from '../../mixins/github-event';

export default React.createClass({
  mixins: [addons.PureRenderMixin, GitHubEvent],

  render: function() {
    var commits = this.props.data.payload.commits;

    commits = commits.map((commit) => {
      var url = this.repoUrl() + '/commit/' + commit.sha;

      return (
        <div key={commit.sha}>
          <h6><a href={url}>{commit.message}</a></h6>
        </div>
      );
    });

    return (
      <li className="media">
        <h6 className="event-time">{this.eventTime()}</h6>
        <div className="media-left">
          <span className="mega-octicon octicon-repo-push"></span>

        </div>
        <div className="media-body">
          <h6 className="media-heading">
            Pushed {commits.length} commit(s) into <a href={this.repoUrl()}>{this.repo()}</a>
          </h6>
          {commits}
        </div>
      </li>
    );
  }
});
