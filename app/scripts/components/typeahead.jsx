import _ from 'lodash';
import React from 'react';
import { Input } from 'react-bootstrap';

export default React.createClass({

  getInitialState: function () {
    return {
      value: new String(),
      optionIndex: -1,
      searchResults: []
    };
  },

  // handles filtering results from the provided options using a really
  // simple regex
  filter: function (value, options) {

    if (this.state.value.length == 0) {
      return new Array();
    }

    var reg = new RegExp(value + '.*', 'i');
    return options.filter(function (option) {
      return reg.test(option);
    });
  },

  // any time a change occurs in the text, we update our own version,
  // and then call the user's callback so they can do whatever they need to
  // in order to update the options list
  onChange: function () {

    var newValue = this.refs.typeahead.getValue();

    var state = {
      value: newValue,
      searchResults: _.isFunction(this.props.filter) ?
        this.props.filter(newValue, this.props.options) : this.filter(newValue, this.props.options)
    };

    // if no search results, unset index
    if (state.searchResults.length === 0) {
      state.optionIndex = -1;
    }

    this.setState(state);

    // hook so the user can do something intelligent dynamically while the
    // user types
    if (_.isFunction(this.props.onChange)) {
      this.props.onChange(this.state.value);
    }
  },

  // Handle key presses for selection
  onKeyDown: function (event) {
    var keyCode = event.keyCode;

    // if no search results, don't bother
    if (this.state.searchResults.length == 0) {
      return;
    }

    switch (keyCode) {
      // down
      case 40:
        if (this.state.optionIndex < this.state.searchResults.length - 1) {
          this.setState({optionIndex: this.state.optionIndex + 1});
        }
        break;
      // up
      case 38:
        if (this.state.optionIndex > -1) {
          this.setState({optionIndex: this.state.optionIndex - 1});
        }
        break;
      case 13:
        this.onClick(event);
        break;
    }
  },

  onClick: function (event) {
    // return the currently default or selected search result
    if (this.state.optionIndex == -1) {
      this.props.onSelect(event.target.textContent);
    } else {
      this.props.onSelect(this.state.searchResults[this.state.optionIndex]);
    }
  },

  render: function () {

    var opts = this.state.searchResults.map(function (option, index) {
      var className = "unselected";
      if (this.state.optionIndex >= 0 && this.state.optionIndex === index) {
        className = "selected";
      }
      return (<li key={option} className={className} onClick={this.onClick} >{option}</li>);
    }.bind(this));

    return (
      <div className="typeahead">
        <Input type="text"
          placeholder={this.props.placeholder}
          value={this.state.value}
          onChange={this.onChange}
          onKeyDown={this.onKeyDown}
          ref="typeahead" />
        <ul className="typeahead-options">
          {opts}
        </ul>
      </div>
    );
  }
});
