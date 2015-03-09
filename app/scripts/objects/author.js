import Check from 'check-types';

export default class {

  constructor(data) {

    if (Check.emptyObject(data)) {
      throw "Empty data object passed to Author constructor";
    }

    this.id = data.id;
    this.name = data.name;
    this.github = data.github;
    this.bio = data.bio;
    this.image = data.image;
    this.notifications = data.notifications;

    this.subscriptions = new Map();
    for (let authorId of data.subscriptions) {
      this.subscriptions.set(authorId, true);
    }
  }

  getImage () {
    return Check.undefined(this.image) ? 'images/placeholder.jpg' : this.image;
  }

  isAuthor (authorId) {
    return this.id == authorId;
  }

  // checks whether both authors subscribe to each other
  hasFriend (author) {
    return this.follows(author.id) && author.follows(this.id) ? true : false;
  }

  followedBy (author) {
    return author.follows(this.id);
  }

  follows (author) {
    return this.subscriptions.has(author.id);
  }

  subscribeTo (author) {
    this.subscriptions.set(author.id, true);
  }

  unsubscribeFrom (author) {
    this.subscriptions.delete(author.id);
  }

  getSubscriptionCount () {
    return this.subscriptions.length;
  }

  findAuthorById (authors, id) {
    for (let author of authors) {
      if (author.id == id) {
        return true;
      }
    }
    return false;
  }
}
