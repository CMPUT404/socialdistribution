import _ from 'lodash';
import Post from './post';

export default class {

  constructor(author, token = null) {

    if (_.isEmpty(author)) {
      throw "Empty data object passed to Author constructor";
    }

    this.token           = token;
    this.id              = author.id;
    this.bio             = author.bio;
    this.url             = author.url;
    this.image           = author.image;
    this.host            = author.host;
    this.email           = author.email;
    this.first_name      = author.first_name;
    this.last_name       = author.last_name;
    this.displayname     = author.displayname;
    this.github_username = author.github_username;

    this.posts     = [];
    this.friends   = [];
    this.following = [];
    this.requests  = [];
    this.pending   = [];

    if (!_.isUndefined(author.posts) && !_.isEmpty(author.posts)) {
      this.posts = author.posts;
    }

    // this.notifications = data.notifications;
  }

  getName() {
    return this.first_name + ' ' + this.last_name;
  }

  getImage () {
    return (_.isNull(this.image) ||
            _.isEmpty(this.image) ||
            _.isUndefined(this.image))
             ?
            'images/placeholder.jpg' : this.image;
  }

  isAuthor (authorId) {
    return this.id == authorId;
  }

  getGithubUrl () {
    return this.github_username ? 'http://github.com/' + this.github_username : null;
  }

  hasFriend (author) {
    return _.indexOf(this.friends, author.id) === -1 ? false : true;
  }

  follows (author) {
    return _.indexOf(this.following, author.id) === -1 ? false : true;
  }

  pendingFriend (author) {
    return _.indexOf(this.pending, author.id) === -1 ? false : true;
  }

  sortedPosts() {
    return _.sortByOrder(this.posts, ['pubDate'], [false]);
  }
}
