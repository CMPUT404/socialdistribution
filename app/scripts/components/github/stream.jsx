import _ from 'lodash';
import React from 'react';
import { addons } from 'react/addons';
import { Alert } from 'react-bootstrap';

import PREvent from './pr-event';
import PushEvent from './push-event';
import DeleteEvent from './delete-event';
import CreatEevent from './create-event';

export default React.createClass({
  mixins: [addons.PureRenderMixin],

  render: function() {

    if (_.isNull(this.props.events) ||
        !_.isArray(this.props.events) ||
        _.isEmpty(this.props.events)) {
      return (
        <Alert bsStyle="info">
          <strong>No Activity</strong>
        </Alert>
      );
    }

    var events = this.props.events.map((event) => {
        switch(event.type) {
          case 'PushEvent': return <PushEvent key={event.id} data={event} />;
          case 'DeleteEvent': return <DeleteEvent key={event.id} data={event} />;
          case 'PullRequestEvent': return <PREvent key={event.id} data={event} />;
          case 'CreateEvent': return <CreatEevent key={event.id} data={event} />
          default: return undefined;
        }
    });
    return (
      <ul className="media-list events">
        {events}
      </ul>
    );
  }
});
