import React, { Component } from 'react'
import { Link } from 'react-router-dom'

export class Header extends Component {
  render() {
    return (
        <nav className="navbar navbar-expand-sm bg-body-tertiary">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">Money Trackers</a>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
       
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav">
              <li className="nav-item">
                <a className="nav-link active" aria-current="page" href="#">Documentation</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#">API Collection</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#">Documentation</a>
              </li>
              <li className="nav-item">
                <a className="nav-link">Creator</a>
              </li>

              <li className="nav-item">
                <a className="nav-link">
                 <Link to="/login">Login</Link>
                  </a>
              </li>
            
              <li className="nav-item">
                <a className="nav-link">
                 <Link to="/register">Register</Link>
                  </a>
              </li>
            
            </ul>
          </div>
       
        </div>
      </nav>
    )
  }
}

export default Header