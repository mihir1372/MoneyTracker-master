import axios from "axios";

import { GET_GROUPS, DELETE_GROUP, ADD_GROUP } from "./types";

import { tokenConfig } from "./auth";

// GET_GROUPS

export const getGroups = () => (dispatch, getState) => {
  axios
    .get('/groups/', tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: GET_GROUPS,
        payload: res.data.payload,
      });
      console.log(res.data);
    })
    .catch((err) => console.log(err));
};

// DELETE_GROUP
export const deleteGroup= (id) => (dispatch, getState) => {
  axios
    .delete(`/groups/${id}/`, tokenConfig(getState))
    .then((res) => {
      console.log({ deleteGroup: 'GroupDeleted' });
      dispatch({
        type: DELETE_GROUP,
        payload: id,
      });
    })
    .catch((err) => console.log(err));
};

// ADD Group
export const addGroup= (Group) => (dispatch, getState) => {
  axios
    .post('/groups/', Group, tokenConfig(getState))
    .then((res) => {
      console.log({ addGroup: 'GroupAdded',"data":res.data });
      dispatch({
        type: ADD_GROUP,
        payload: res.data,
      });
    })
    .catch((err) => console.log(err));
};