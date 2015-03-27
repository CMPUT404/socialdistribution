import config from '../config.json';

export function  API() {
  if (config.env === 'dev') {
    return 'http://localhost:8000';
  } else {
    return 'http://socshizzle-api.herokuapp.com';
  }
}
