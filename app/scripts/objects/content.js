import _ from 'lodash';
import Moment from 'moment';

// represents our base content class
export default class {

  constructor (contentData) {
    this.id = contentData.id;
    // TODO: check if other and convert to class if not
    this.author = contentData.author;
    this.content = contentData.content;
    this.type = contentData.type;

    // make sure we have a timestamp
    if (_.isUndefined(contentData.timestamp)) {
      this.timestamp = Moment.unix()
    } else {
      this.timestamp = contentData.timestamp;
    }
  }

  getType () {
    return "Content";
  }
}
