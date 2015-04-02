import _ from 'lodash';
import Post from './post';

class Author {

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

    if (!_.isEmpty(author.friends)) {
      this.friends = author.friends.map(responseToAuthor)
    }

    if (!_.isEmpty(author.following)) {
      this.following = author.following.map(responseToAuthor)
    }

    if (!_.isEmpty(author.requests)) {
      this.requests = author.requests.map(responseToAuthor)
    }

    if (!_.isEmpty(author.pending)) {
      this.pending = author.pending.map(responseToAuthor)
    }

    if (_.isNull(this.image) ||
        _.isEmpty(this.image) ||
        _.isUndefined(this.image)) {
      this.image = '/images/placeholder.jpg';
    }
  }

  getName() {
    return this.first_name + ' ' + this.last_name;
  }

  isAuthor (authorId) {
    return this.id == authorId;
  }

  getGithubUrl () {
    return this.github_username ? 'http://github.com/' + this.github_username : null;
  }

  inList (list, author) {
    if (list in this) {
      return _.findIndex(this[list], a => a.id === author.id) === -1 ? false : true;
    } else {
      return false;
    }
  }

  removeFrom(list, author) {
    if(list in this) {
      _.remove(this[list], a => a.id == author.id);
    }
  }

  addTo(list, author) {
    if (!this.inList(list, author)) {
      this[list].push(author);
    }
  }

  sortedPosts () {
    return _.sortByOrder(this.posts, ['pubDate'], [false]);
  }
}

function responseToAuthor(authorData) {
  return new Author(authorData);
}

export default Author;
