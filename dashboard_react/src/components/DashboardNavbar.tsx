import React, { useState, useEffect } from "react";
import { Navbar, Nav, NavDropdown, Container } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.css";

const DashboardNavbar = ({ user }) => {
  const [datetime, setDateTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setDateTime(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // const formattedDateTime = `${dateTime.toLocaleDateString()}, ${dateTime.toLocaleTimeString()}`;

  return (
    <Navbar bg="light" expand="lg">
      <Container>
        <div className="d-flex align-items-center gap-lg-2 gap-1">
          <div className="logo-topbar">
            <a href="/" className="logo-light">
              <img
                src="https://storage.googleapis.com/2023_new_prolube76site/homepageapp/2022-Logo-Transparent-small.png"
                width="80"
                alt="logo"
              />
            </a>
          </div>
        </div>
        <ul className="topbar-menu d-flex align-items-center gap-3">
          <li className="nav-item">
            <a
              className="nav-link dropdown-toggle arrow-none"
              data-bs-toggle="dropdown"
              href="#"
              role="button"
              aria-haspopup="false"
              aria-expanded="false"
            >
              <img
                src="https://storage.googleapis.com/2023_new_prolube76site/dashboard/images/flags/us.jpg"
                alt="user-image"
                className="me-0 me-sm-1"
                height="12"
              />
              <span className="align-middle d-none d-lg-inline-block">
                English
              </span>{" "}
              <i className="mdi mdi-chevron-down d-none d-sm-inline-block align-middle"></i>
            </a>
          </li>
          <li className="dropdown">
            {user ? (
              <>
                <a
                  className="nav-link dropdown-toggle arrow-none nav-user px-2"
                  data-bs-toggle="dropdown"
                  href="#"
                  role="button"
                  aria-haspopup="false"
                  aria-expanded="false"
                >
                  <span className="account-user-avatar">
                    <img
                      src="https://storage.googleapis.com/2023_new_prolube76site/dashboard/images/users/avatar-1.jpg"
                      alt="user-image"
                      width="32"
                      className="rounded-circle"
                    />
                  </span>
                  <span className="d-lg-flex flex-column gap-1 d-none">
                    <h5 className="my-0">Hi {user.user_first_name}</h5>
                    <h6 className="my-0 fw-normal">Email: {user.email}</h6>
                  </span>
                </a>
                <div className="dropdown-menu dropdown-menu-end dropdown-menu-animated profile-dropdown">
                  <a href="/profile" className="dropdown-item">
                    <i className="mdi mdi-account-circle me-1"></i>
                    <span>My Profile - Employee Info</span>
                  </a>
                  <a href="/logout" className="dropdown-item">
                    <i className="mdi mdi-logout me-1"></i>
                    <span>Logout</span>
                  </a>
                </div>
              </>
            ) : (
              <span className="d-lg-flex flex-column gap-1 d-none">
                <h5 className="my-0">NO INFORMATION</h5>
                <h6 className="my-0 fw-normal">No internal user logged in.</h6>
              </span>
            )}
          </li>
        </ul>
      </Container>
    </Navbar>
  );
};

export default DashboardNavbar;
