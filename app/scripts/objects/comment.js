import Content from './content';

export default class extends Content {
  constructor (commentData) {
    super(commentData);

    this.comment = commentData.comment;
  }

  getType () {
    return "Comment";
  }
}
