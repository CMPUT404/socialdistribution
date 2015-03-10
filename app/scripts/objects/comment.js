import Content from './content';

export default class extends Content {
  constructor (commentData) {
    super(commentData);
  }

  getType () {
    return "Comment";
  }
}
