import React, { Component,Fragment } from 'react'
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { addGroup } from "../../actions/groups";

export class Groups extends Component {


  state={
    name: '',
    members: '',
  }

  static propTypes = {
    addGroup: PropTypes.func.isRequired
  };

  onChange = e => this.setState({ [e.target.name]: e.target.value });
  
  onSubmit = e => { e.preventDefault(); 
    const { name, members } = this.state;
    const group = { name, members };
    // console.log(group);
    this.props.addGroup(group);  
  };

  render() {
    const { name, members} = this.state;
    return (
      <div className="card card-body mt-4 mb-4">
        <h2>Create Group</h2>
        
        <form onSubmit={this.onSubmit}>
          <div className="form-group">
            <label>Group Name</label>
            <input
              className="form-control"
              type="text"
              name="name"
              onChange={this.onChange}
              value={name}
            />
          </div>
          
          <div className="form-group">
            <label>Members</label>
            <input
              className="form-control"
              type="text"
              name="members"
              onChange={this.onChange}
              value={members}
            />
          </div>
          
          &nbsp;
          <div className="form-group">
            
            <button type="submit" className="btn btn-primary">
              Submit
            </button>
          </div>
        </form>
      </div>
    );
  }
}

export default connect(null,{ addGroup })(Groups);