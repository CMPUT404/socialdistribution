import _ from 'lodash';
import Moment from 'moment';

// represents our base content class
export default class {

  constructor (contentData) {
    this.guid = contentData.guid;
    this.author = contentData.author;
    this.pubDate = contentData.pubDate;
  }

  getType () {
    return "Content";
  }
}
