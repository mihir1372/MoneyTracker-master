import React, { Component,Fragment } from 'react'
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { addUserProfile } from "../../actions/userprofile";
import { Link, useNavigate } from 'react-router-dom';



export class UserProfile extends Component {
  
  

  state={
    name: '',
    email: '',
  }

  static propTypes = {
    addUserProfile: PropTypes.func.isRequired
  };

  

  onChange = e => this.setState({ [e.target.name]: e.target.value });

  onSubmit = e => { e.preventDefault(); 
    const { name, email } = this.state;
    const userprofile = { name, email };
    
    this.props.addUserProfile( userprofile);  
    
  };

  render() {
    const { name, email} = this.state;
    return (
      <div className="card card-body mt-4 mb-4">
        <h2>Create  User Profile</h2>

        <form onSubmit={this.onSubmit}>
          <div className="form-group">
            <label>Name</label>
            <input
              className="form-control"
              type="text"
              name="name"
              onChange={this.onChange}
              value={name}
            />
          </div>
          
          <div className="form-group">
            <label>Email</label>
            <input
              className="form-control"
              type="text"
              name="email"
              onChange={this.onChange}
              value={email}
            />
          </div>
          
          &nbsp;
          <div className="form-group">
            
            <button type="submit" className="btn btn-primary">
              Submit
            </button>

            <Link to="/group">
            <button className="btn btn-primary">
              Go to Groups
            </button>
            </Link>

          </div>
        </form>
      </div>
    );
  }
}

export default connect(null,{ addUserProfile })(UserProfile);