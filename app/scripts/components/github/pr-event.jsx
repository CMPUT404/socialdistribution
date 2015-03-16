import React from 'react';
import { addons } from 'react/addons';
import GitHubEvent from '../../mixins/github-event';

export default React.createClass({
  mixins: [addons.PureRenderMixin, GitHubEvent],

  render: function() {
    var pr, icon;
    var payload = this.props.data.payload;

    var url = <a href={payload.pull_request.html_url}>
                {this.repo() + '#' + payload.number}
              </a>;

    if (payload.action === 'closed' && payload.merged === true) {
      pr = (
        <span>
          Merged pull request {url}
        </span>
      );

      icon = <span className="mega-octicon octicon-git-merge"></span>;
    } else {
      pr = (
        <span>
          <span className="text-capitalize">{payload.action}</span>
          <span> pull request {url}</span>
        </span>
      );

      icon = <span className="mega-octicon octicon-git-pull-request"></span>;
    }

    return (
      <li className="media">
        <h6 className="event-time">{this.eventTime()}</h6>
        <div className="media-left">
          {icon}
        </div>
        <div className="media-body">
          <h6 className="media-heading">
            {pr}
          </h6>
        </div>
      </li>
    );
  }
});
