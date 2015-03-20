import _ from 'lodash';
import Moment from 'moment';
import Author from './author';
// represents our base content class
export default class {

  constructor (contentData) {
    this.guid = contentData.guid;
    this.pubDate = contentData.pubDate;
    this.author = new Author(contentData.author);
  }

  getType () {
    return "Content";
  }
}
