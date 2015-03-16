import React from 'react';
import { addons } from 'react/addons';
import GitHubEvent from '../../mixins/github-event';

export default React.createClass({
  mixins: [addons.PureRenderMixin, GitHubEvent],

  render: function() {
    var ref      = this.props.data.payload.ref;
    var ref_type = this.props.data.payload.ref_type;

    return (
      <li className="media">
        <h6 className="event-time">{this.eventTime()}</h6>
        <div className="media-left">
          <span className="mega-octicon octicon-trashcan"></span>
        </div>
        <div className="media-body">
          <h6 className="media-heading">
            Deleted {ref_type} <code>{ref}</code> from <a href={this.repoUrl()}>{this.repo()}</a>
          </h6>
        </div>
      </li>
    );
  }
});
