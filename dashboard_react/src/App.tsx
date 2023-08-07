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
  Navigate,
  Link,
  RouteMatch,
} from "react-router-dom";
import { ExternalCSS } from "./components/ExternalCSS";
import DashboardView from "./components/DashboardView";
import { homepageAppExternalCSS } from "./components/Constants";
import { RedirectTo } from "./components/Types";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);

  // This useEffect will simulate checking if the user is "remembered"
  // You'll likely replace this with actual logic to check e.g. local storage or an auth token.
  useEffect(() => {
    const rememberedUser = localStorage.getItem("username");
    if (rememberedUser) {
      setIsLoggedIn(true);
    }
  }, []);

  return (
    <>
      {/* this is the homepageapp's main theme css.  */}
      <ExternalCSS href={homepageAppExternalCSS} />
      <Router>
        <Routes>
          <Route path="/" element={<HomepageApp />} />
          {/* Redirect '/homepage' and '/home' to '/' */}
          <Route path="/homepage" element={<RedirectTo to="/" />} />
          <Route path="/home" element={<RedirectTo to="/" />} />

          {/* Check if user visits 'employees/login/' */}
          <Route
            path="employees/login/"
            element={!isLoggedIn ? <DashboardView /> : <Navigate to="/dash/" />}
          />
          <Route path="/dash" element={<DashboardView />} />

          {/* New '/section' route */}
          <Route path="/section" element={<HomepageSection />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
