import React,{Component,Fragment} from "react";  
import reactDom from "react-dom";
import { HashRouter as Router,Route,Routes,Redirect } from "react-router-dom";

import Header from "./layout/Header";
import Groups from "./Dashboard/Group";

import Login from "./Forms/login";
import Register from "./Forms/register";
import UserProfile from "./Forms/UserProfile";

import PrivateRoute from "./PrivateRoutes";
import { loadUser } from "../actions/auth";

import { Provider } from "react-redux";
import store from "../store";

class App extends React.Component {

    componentDidMount() {
        store.dispatch(loadUser());
    }

    render() {
        return (
        <Provider store={store}>
            < Router >
           <Fragment>
                <Header />

                <div className="container">  
               
                <Routes>
                    <Route element={<PrivateRoute/>} >
                        <Route exact path="/" element={<UserProfile/>} />
                        <Route exact path="/group" element={<Groups/>} />
                        
                    </Route>

                    <Route exact path="/login" element={<Login/>} />
                    <Route exact path="/register" element={<Register/>} />
                </Routes>
                    
                </div>

           </Fragment>
           </Router>
        </Provider>
        );
    }
}

reactDom.render(<App />, document.getElementById("app"));