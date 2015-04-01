import _ from 'lodash';
import Moment from 'moment';

import Content from './content';
import Comment from './comment';

export default class extends Content {

  constructor (postData) {
    super(postData);

    this.title = postData.title;
    this.source = postData.source;
    this.origin = postData.origin;
    this.content = postData.content;
    this.contentType = postData['content-type'];
    this.visibility = postData.visibility;
    this.image = postData.image;
    this.comments = [];

    // if we have any comment data, marshal it into comment classes
    if (!_.isUndefined(postData.comments)) {
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
