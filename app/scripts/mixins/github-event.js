import Moment from 'moment';

// mixin for GitHub event components that need to compute common url pattern
export default {
  repo: function() {
    return this.props.data.repo.name;
  },

  repoUrl: function() {
    return 'https://github.com/' + this.repo();
  },

  eventTime: function() {
    return Moment(this.props.data.created_at).fromNow();
  }
};
