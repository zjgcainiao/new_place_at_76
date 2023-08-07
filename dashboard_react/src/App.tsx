import React, { useState, useEffect } from "react";
// import "./App.css";
import HomepageApp from "./components/HomepageApp";
import HomepageSection from "./components/HomepageSection";
import {
  createBrowserRouter,
  BrowserRouter as Router,
  Routes, // instead of "Switch"
  Route,
  redirect,
  useNavigate,
  Link,
  RouteMatch,
} from "react-router-dom";
import { ExternalCSS } from "./components/ExternalCSS";
import DashboardView from "./components/DashboardView";

// custom component to do redirect
const RedirectTo: React.FC<{ to: string }> = ({ to }) => {
  const navigate = useNavigate();
  React.useEffect(() => {
    navigate(to);
  }, [to, navigate]);

  return null;
};

function App() {
  return (
    <>
      {/* this is the homepageapp's main theme css  */}
      <ExternalCSS href="https://storage.googleapis.com/2023_new_prolube76site/homepageapp/css/theme.min.css" />
      <Router>
        <Routes>
          <Route path="/" element={<HomepageApp />} />
          {/* Redirect '/homepage' and '/home' to '/' */}
          <Route path="/homepage" element={<RedirectTo to="/" />} />
          <Route path="/home" element={<RedirectTo to="/" />} />
          <Route path="/dash" element={<DashboardView />} />

          {/* New '/section' route */}
          <Route path="/section" element={<HomepageSection />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
