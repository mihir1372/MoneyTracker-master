import React, { Component,Fragment } from 'react'
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { getGroups,deleteGroup } from "../../actions/groups";

export class GroupsList extends Component {

  static propTypes = {
    groups: PropTypes.array.isRequired,
    getGroups: PropTypes.func.isRequired,
    deleteGroup: PropTypes.func.isRequired
  };

  componentDidMount() {
    this.props.getGroups();
  }

  render() {
    return (
      <div>
        <Fragment>
        <h1>
            Groups List 
        </h1>
        <h6>  </h6>
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Group Name</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            {this.props.groups.map(group => (
              <tr key={group.id}>
                <td>{group.name},{group.id}</td>
                <td> {group.expense_map.expenses} </td>
                
                <td>
                  <button 
                  onClick={this.props.deleteGroup.bind(this, group.id)} 
                    className="btn btn-danger btn-sm"> 
                    Delete 
                  </button>

           
                </td>

              </tr>
            ))}
          </tbody>
        </table>
      </Fragment>
      </div>
    )
  }
}

const mapStateToProps = state => ({
  groups: state.groups.groups
});

export default connect(mapStateToProps,{ getGroups,deleteGroup } )(GroupsList);