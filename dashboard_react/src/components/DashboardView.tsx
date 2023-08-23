import React, { useState, useEffect } from "react";
import InternalUserLoginForm from "./InternalUserLoginForm";
import TechnicianView from "./TechnicianView";
import ServiceAdvisorView from "./ServiceAdvisorView";
import DashboardNavbar from "./DashboardNavbar"; // import the DashboardNavbar component
import HomepageApp from "./HomepageApp";
import { InternalUser } from "./Types";
import { InternalUserLoginAPI } from "./Constants";
import {
  BrowserRouter as Router,
  Routes, // instead of "Switch"
  Route,
} from "react-router-dom";
import {
  handleInternalUserLogin,
  handleInternalUserLogout,
} from "./authService";
function DashboardView() {
  const [user, setUser] = useState<InternalUser | null>(null);

  const handleLogin = async (email: string, password: string) => {
    const response = await fetch(InternalUserLoginAPI, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });

    if (response.ok) {
      const user = await response.json();
      setUser(user);
    } else {
      console.error("Login failed. Please use the email in your employee form");
    }
  };

  return (
    <>
      {!user ? (
        <>
          <InternalUserLoginForm handleLogin={handleLogin} />
        </>
      ) : user.is_technician ? (
        <>
          <DashboardNavbar user={user} />
          <TechnicianView />
        </>
      ) : (
        <>
          <DashboardNavbar user={user} />
          <ServiceAdvisorView />
        </>
      )}
    </>
  );
}

export default DashboardView;
