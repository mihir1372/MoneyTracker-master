import React from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

const PrivateRoute = ({auth: {isAuthenticated}}) => {
    

    return (
    isAuthenticated ? <Outlet /> : <Navigate to="/login" />
  );
}
  
   

const mapStateToProps = (state) => ({
  auth: state.auth,
});

export default connect(mapStateToProps)(PrivateRoute);