import React, { useState } from "react";
import {
  handleInternalUserLogin,
  handleInternalUserLogout,
} from "./authService";
import {
  Container,
  Row,
  Col,
  Card,
  Form,
  Button,
  InputGroup,
  FormControl,
  Alert,
} from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { ExternalCSS } from "./ExternalCSS";
import { homepageAppExternalCSS, logo } from "./Constants";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

interface InternalUserLoginFormProps {
  handleLogin: (username: string, password: string) => void;
  logoUrl?: string;
}

const InternalUserLoginForm: React.FC<InternalUserLoginFormProps> = ({
  handleLogin,
}) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    handleLogin(username, password);

    if (rememberMe) {
      const tenDays = 10 * 24 * 60 * 60 * 1000; // 10 days in milliseconds
      const expiryDate = new Date(new Date().getTime() + tenDays);

      localStorage.setItem("username", username);
      localStorage.setItem("expiry", expiryDate.toString());
    } else {
      localStorage.removeItem("username");
      localStorage.removeItem("expiry");
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center vh-100">
      {/* <ExternalCSS href={homepageAppExternalCSS} /> */}
      <Card style={{ width: "24rem" }} className="card-hover card-border">
        <Card.Header className="text-center bg-dark">
          <a href="/">
            <img src={logo} alt="logo" />
          </a>
        </Card.Header>
        <Card.Body>
          <div className="text-center w-75 m-auto">
            <h4 className="text-dark-50 pb-0 fw-bold">Employee Login</h4>
            <p className="text-muted mb-3">
              Enter your email address and password. First Time employee will
              have to Sign Up using the link at the bottom.
            </p>
          </div>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Enter Email</Form.Label>
              <FormControl
                type="email" //type can be email or text. use email for better validation
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Use the contact email you submit in your employment docs."
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Password</Form.Label>
              <InputGroup>
                <FormControl
                  type={showPassword ? "text" : "password"} //"password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Password"
                />
                {/* The password-eye functionality is missing, as it requires additional scripting */}
                <InputGroup.Text onClick={() => setShowPassword(!showPassword)}>
                  <span className="password-eye">
                    <FontAwesomeIcon icon={showPassword ? faEyeSlash : faEye} />
                  </span>
                </InputGroup.Text>
              </InputGroup>
              <Form.Text className="text-muted float-end">
                <a href="/password-reset">Forgot your password?</a>
              </Form.Text>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Check
                type="checkbox"
                label="Remember me"
                checked={rememberMe} // <-- this line ensures the checkbox reflects the state
                onChange={(e) => setRememberMe(e.target.checked)}
              />
            </Form.Group>
            <Button variant="outline-primary" type="submit" className="w-100">
              Log In
            </Button>
          </Form>
        </Card.Body>
        <Card.Footer className="text-center">
          First-time Employee Login?{" "}
          <a href="/register" className="ms-1">
            <b>Sign Up</b>
          </a>
        </Card.Footer>
      </Card>
    </Container>
  );
};

export default InternalUserLoginForm;
