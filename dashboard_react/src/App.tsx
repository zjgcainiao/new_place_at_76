import React, { useState, useEffect } from "react";
import LoginForm from "./components/LoginForm";
import TechnicianView from "./components/TechnicianView";
import ServiceAdvisorView from "./components/ServiceAdvisorView";
import Navbar from "./components/Navbar"; // import the Navbar component

function App() {
  const [user, setUser] = useState(null);

  const handleLogin = async (email, password) => {
    const response = await fetch(
      "http://192.168.1.48/apis/internal_user_login/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      }
    );

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
          <Navbar user={user} />
          <TechnicianView />
        </>
      ) : (
        <ServiceAdvisorView />
      )}
    </>
  );
}

export default App;
