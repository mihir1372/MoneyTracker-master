import { combineReducers } from 'redux';
import groups from './groups';
import auth from './auth';

export default combineReducers({
   groups,
   auth
});