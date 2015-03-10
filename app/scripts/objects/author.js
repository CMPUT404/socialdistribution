import _ from 'lodash';

export default class {

  constructor(data, subscriptionStore) {

    if (_.isEmpty(data)) {
      throw "Empty data object passed to Author constructor";
    }

    this.id = data.id;
    this.name = data.name;
    this.github = data.github;
    this.bio = data.bio;
    this.image = data.image;
    this.notifications = data.notifications;
    this.subscriptionCount = data.subscriptions.length;
    this.subscriptionStore = subscriptionStore;

    // create or update list of subscriptions for each author this author is
    // subscribed to
    for (let authorId of data.subscriptions) {
      var subscriptions = this.subscriptionStore.get(authorId);
      if (_.isUndefined(subscriptions)) {
        this.subscriptionStore.set(authorId, [this.id]);
      } else {
        subscriptions.push(this.id);
      }
    }
  }

  getImage () {
    return _.isUndefined(this.image) ? 'images/placeholder.jpg' : this.image;
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
    var subscriptions = this.subscriptionStore.get(author.id);

    // if author has no subscriptions then nope
    if (_.isUndefined(subscriptions)) {
      return false;
    }

    // otherwise try and find it in the list
    for (let subscriberId of subscriptions) {
      if (subscriberId == this.id) {
        return true;
      }
    }
    return false;
  }

  subscribeTo (author) {
    var subscriptions = this.subscriptionStore.get(author.id);
    if (_.isUndefined(subscriptions)) {
      this.subscriptionStore.set(author.id, [this.id]);
    } else {
      subscriptions.push(this.id);
    }
    this.subscriptionCount++;
  }

  unsubscribeFrom (author) {
    var subscriptions = this.subscriptionStore.get(author.id);

    // remove the author id using splice
    var index = subscriptions.indexOf(this.id);
    subscriptions.splice(index, 1);
    this.subscriptionCount--;
  }

  getSubscriptions () {
    return this.subscriptionStore.get(this.id);
  }

  getSubscriptionCount() {
    return this.subscriptionCount;
  }

  // This one we can't track through the Author because subscriptions are
  // coming from outside
  getSubscriberCount () {
    var subscriptions = this.getSubscriptions();
    return _.isUndefined(subscriptions) ? 0 : subscriptions.length;
  }
}
