import React, { useState, useEffect } from "react";
import { Navbar, Nav, NavDropdown, Container } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import { InternalUser } from "./Types";
import { logo } from "./Constants";

interface DashboardNavbarProps {
  user: InternalUser;
}

const DashboardNavbar: React.FC<DashboardNavbarProps> = ({ user }) => {
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
        <Navbar.Brand href="/">
          <img src={logo} width="80" alt="logo" />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="dashboard-navbar-nav" />
        <Navbar.Collapse id="dashbaord-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="/">Home</Nav.Link>
            {/* Add more navigation links as needed */}
          </Nav>
          <Nav>
            {/* <small>Today is {formattedDateTime}</small> */}
            {user && (
              <NavDropdown title={`Hi ${user.email}`} id="basic-nav-dropdown">
                <NavDropdown.Item href="#">
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
