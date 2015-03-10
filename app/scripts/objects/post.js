import Check from 'check-types';
import Moment from 'moment';

import Content from './content';
import Comment from './comment';

export default class extends Content {

  constructor (postData) {
    super(postData);

    this.comments = [];

    // if we have any comment data, marshal it into comment classes
    if (!Check.undefined(postData.comments)) {
      for (let comment of postData.comments) {
        this.comments.push(new Comment(comment));
      }
    }
  }

  addComment (comment) {
    this.comments.push(comment);
  }

  removeComment (comment) {
    var index = this.comments.indexOf(comment);
    this.comments.slice(index, 1);
  }

  hasComments () {
    return this.comments.length > 0;
  }

  getComments () {
    return this.comments;
  }

  getType() {
    return "Post";
  }
}
