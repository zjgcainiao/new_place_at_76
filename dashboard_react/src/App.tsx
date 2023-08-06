import React, { useState, useEffect } from "react";
import LoginForm from "./components/LoginForm";
import TechnicianView from "./components/TechnicianView";
import ServiceAdvisorView from "./components/ServiceAdvisorView";
import DashboardNavbar from "./components/DashboardNavbar"; // import the DashboardNavbar component

interface User {
  email: string;
  password: string;
  is_technician: boolean;
  // Add other possible properties of a user here
}

function App() {
  // const [user, setUser] = useState(null);
  const [user, setUser] = useState<User | null>(null);

  const handleLogin = async (email: string, password: string) => {
    const response = await fetch("http://localhost/apis/internal_user_login/", {
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
          <LoginForm handleLogin={handleLogin} />
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

export default App;
