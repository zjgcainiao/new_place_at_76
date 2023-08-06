import React, { useState, useEffect } from "react";
import LoginForm from "./components/LoginForm";
import TechnicianView from "./components/TechnicianView";
import ServiceAdvisorView from "./components/ServiceAdvisorView";
import DashboardNavbar from "./components/DashboardNavbar"; // import the DashboardNavbar component
import {
  createBrowserRouter,
  BrowserRouter as Router,
  Routes, // instead of "Switch"
  Route,
  Link,
  RouteMatch,
} from "react-router-dom";
import HomepageApp from "./components/HomepageApp";
import DashboardView from "./components/DashboardView";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomepageApp />} />
        {/* <HomepageApp /> */}
        <Route path="/dash">
          <DashboardView />
        </Route>
        {/* Add more routes as needed */}
      </Routes>
    </Router>
  );
}

export default App;
