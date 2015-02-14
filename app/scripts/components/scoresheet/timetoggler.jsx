var React = require('react');

var TimeToggler = React.createClass({

  render: function() {

    var classString = "btn btn-block btn-";
    var text = "";

    if (this.props.running) {
      classString += "danger";
    } else {
      classString += "success";
    }

    return (
      <button type="button" className={classString} onClick={this.props.onClick}>{this.props.time}</button>
    );
  }
});

module.exports = TimeToggler;
