import React from "react";
import { Link } from "react-router-dom"; // Import if you're using React Router for navigation
import { logo } from "./Constants";

const HomepageNavbar: React.FC = () => {
  return (
    <header
      className="navbar navbar-expand-lg navbar-light fixed-top"
      data-scroll-header
    >
      <div className="container">
        <Link className="navbar-brand me-1 me-xl-4" to="/">
          {" "}
          {/* Replace `/homepage` with your route */}
          <img
            className="d-block"
            src={logo}
            width="75"
            alt="Amazing Automan LLC"
          />
        </Link>
        <button
          className="navbar-toggler ms-auto"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <Link
          className="btn btn-link btn-dark btn-sm d-none d-lg-block order-lg-3"
          to="/employees/login"
        >
          {" "}
          {/* Replace with your route */}
          <i className="fi-login me-2"></i>Employee
        </Link>
        <Link
          className="btn btn-primary btn-sm ms-2 order-lg-3"
          to="/react/customer-register"
        >
          {" "}
          {/* Replace with your route */}
          <i className="fi-users me-2"></i>Create an Account
        </Link>
        <div className="collapse navbar-collapse order-lg-2" id="navbarNav">
          <ul
            className="navbar-nav navbar-nav-scroll"
            style={{ maxHeight: "20rem" }}
          >
            <li className="nav-item dropdown py-2 me-lg-2">
              <a
                className="nav-link dropdown-toggle align-items-center border-end-lg border-light py-1 pe-lg-4"
                href="#"
                data-bs-toggle="dropdown"
                role="button"
                aria-expanded="false"
              >
                <i className="fi-layers me-2"></i>Services
              </a>
              <ul className="dropdown-menu dropdown-menu-light">
                <li>
                  <Link className="dropdown-item" to="/services">
                    {" "}
                    {/* Replace with your route */}
                    <i className="fi-car me-2"></i>Service List
                  </Link>
                </li>
                <li className="dropdown-divider"></li>
                <li>
                  <Link className="dropdown-item" to="react/about-us">
                    {" "}
                    {/* Replace with your route */}
                    <i className="fi-friends fs-base me-2"></i>About Us
                  </Link>
                </li>
              </ul>
            </li>
            <li className="nav-item active">
              <Link className="nav-link" to="appts/create/">
                {" "}
                {/* Replace with your route */}
                Service Appointment
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </header>
  );
};

export default HomepageNavbar;
