import React from 'react';
import { addons } from 'react/addons';
import { Input } from 'react-bootstrap';

export default React.createClass({
  mixins: [addons.PureRenderMixin],

  getInitialState: function() {
    return {
      fileName: 'Select Image',
      remove: false
    };
  },

  componentDidMount: function() {
    this.refs.imgFile.getDOMNode().addEventListener('change', this.imageChange, false);
  },

  componentWillUnmount: function() {
    this.refs.imgFile.getDOMNode().removeEventListener('change', this.imageChange, false);
  },

  imageChange: function(e) {
    var reader = new FileReader();
    var file   = e.target.files[0];

    if (!file.type.match('image.*')) {
      this.setState({fileName: 'Invalid format'});
      return;
    }

    if (file.size > (2*Math.pow(10, 6))) {
      this.setState({fileName: 'Image too big'});
      return;
    }

    this.setState({fileName: file.name});

    reader.onload = () => {
      this.setState({remove: true});

      if (this.props.onComplete) {
        this.props.onComplete(reader.result);
      }
    }

    reader.readAsDataURL(file);
  },

  reset: function() {
    this.setState(this.getInitialState());
  },

  imageRemove: function() {
    this.reset();

    if (this.props.onComplete) {
      this.props.onComplete('');
    }
  },

  render: function() {
    var label;
    var remove;

    if (this.props.label) {
      label = (<label className="control-label">{this.props.label}</label>);
    }

    if (this.state.remove) {
      remove = (
        <span className="btn btn-danger btn-file" onClick={this.imageRemove}>
            Remove
        </span>
      );
    }
    return (
      <div className="form-group">
        {label}
        <div className="input-group">
            <span className="input-group-btn">
                <span className="btn btn-default btn-file">
                    Browse&hellip; <input ref="imgFile" type="file" />
                </span>
                {remove}
            </span>
            <Input type="text" className="form-control" value={this.state.fileName} readOnly />
        </div>
      </div>
    );
  }
});
