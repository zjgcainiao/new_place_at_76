import React, { useState, useEffect } from "react";
import { Navbar, Nav, NavDropdown, Container } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.css";

const DashboardNavbar = ({ user }) => {
  const [datetime, setDateTime] = useState(new Date());
  const [formattedDateTime, setFormattedDateTime] = useState("");

  useEffect(() => {
    const interval = setInterval(() => {
      const newDateTime = new Date();
      setDateTime(newDateTime);
      setFormattedDateTime(
        `${newDateTime.toLocaleDateString()}, ${newDateTime.toLocaleTimeString()}`
      );
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Navbar bg="light" expand="lg" data-bs-theme="light">
      <Container>
        <Navbar.Brand href="#home">
          <img
            src="https://storage.googleapis.com/2023_new_prolube76site/dashboard/images/logo-2022.svg"
            width="80"
            alt="logo"
          />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="dashboard-navbar-nav" />
        <Navbar.Collapse id="dashbaord-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="#home">Home</Nav.Link>
            {/* Add more navigation links as needed */}
          </Nav>
          <Nav>
            {/* <small>Today is {formattedDateTime}</small> */}
            {user && (
              <NavDropdown title={`Hi ${user.email}`} id="basic-nav-dropdown">
                <NavDropdown.Item href="#action/3.1">
                  My Profile - Employee Info
                </NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item href="#action/3.4">Logout</NavDropdown.Item>
              </NavDropdown>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default DashboardNavbar;
