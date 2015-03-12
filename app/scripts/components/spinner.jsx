import React from 'react';
import { addons } from 'react/addons';

export default React.createClass({
  mixins: [addons.PureRenderMixin],

  render: function() {
    return (
      <div className= "spinner">
        <i className="fa fa-refresh fa-spin fa-5x"></i>
      </div>
    );
  }
});
