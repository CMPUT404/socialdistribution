import Router from 'react-router';
import Config from '../config.json';

var API;
var RouterLocation;

if (Config.env === 'dev') {
  API            = () => 'http://localhost:8000';
  RouterLocation = () => Router.HashLocation;
}

if (Config.env === 'prod') {
  API            = () => 'http://socshizzle-api.herokuapp.com';
  RouterLocation = () => Router.HistoryLocation;
}

export { API, RouterLocation }
