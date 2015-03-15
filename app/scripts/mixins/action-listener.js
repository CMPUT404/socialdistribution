// mixin for components that want to use Action listeners

export default {
  listen: function(action, callback) {
    this.listeners.push(action.listen(callback));
  },

  componentDidMount: function() {
    this.listeners = [];
  },

  componentWillUnmount: function() {
    this.listeners.forEach((l) => l());
  }
};
