import React, { useState, useEffect } from "react";
// import "./App.css";
import HomepageApp from "./components/HomepageApp";
import Error404Component from "./components/Error404Component";
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
// import { CustomRedirectTo } from "./components/Types";
import AppointmentCreationView from "./components/AppointmentCreationForm";

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
      <Router basename="/react">
        <Routes>
          <Route path="/" element={<HomepageApp />} />
          {/* Redirect '/homepage' and '/home' to '/' */}
          <Route path="/homepage" element={<Navigate replace to="/" />} />
          <Route path="/home" element={<Navigate replace to="/" />} />

          {/* Check if user visits 'employees/login/' */}
          <Route
            path="/employees/login"
            element={!isLoggedIn ? <DashboardView /> : <Navigate to="/dash/" />}
          />
          <Route path="/dash" element={<DashboardView />} />
          <Route path="/appts/create" element={<AppointmentCreationView />} />

          {/* New '/section' route */}
          <Route path="/section" element={<HomepageSection />} />

          <Route path="*" element={<Error404Component />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
