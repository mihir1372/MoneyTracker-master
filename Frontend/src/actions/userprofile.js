import axios from "axios";

import { GET_USERPROFILE, DELETE_USERPROFILE, ADD_USERPROFILE } from "./types";

import { tokenConfig } from "./auth";

// GET_USERPROFILE

export const getUserProfiles = (id) => (dispatch, getState) => {
  axios
    .get(`/userprofile/${id}/`, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: GET_USERPROFILE,
        payload: res.data.payload,
      });
      console.log(res.data);
    })
    .catch((err) => console.log(err));
};

// DELETE_USERPROFILE
export const deleteUserProfile= (id) => (dispatch, getState) => {
  axios
    .delete(`/userprofile/${id}/`, tokenConfig(getState))
    .then((res) => {
      console.log({ deleteUserProfile: 'UserProfileDeleted' });
      dispatch({
        type: DELETE_USERPROFILE,
        payload: id,
      });
    })
    .catch((err) => console.log(err));
};

// ADD UserProfile
export const addUserProfile= (UserProfile) => (dispatch, getState) => {
  axios
    .post('/userprofile/', UserProfile, tokenConfig(getState))
    .then((res) => {
      console.log({ addUserProfile: 'UserProfileAdded' });
      dispatch({
        type: ADD_USERPROFILE,
        payload: res.data,
      });
    })
    .catch((err) => console.log(err));
};