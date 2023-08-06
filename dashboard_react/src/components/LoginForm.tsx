import React, { useState } from "react";
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

interface LoginFormProps {
  handleLogin: (username: string, password: string) => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ handleLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    handleLogin(username, password);
  };

  return (
    <Container className="d-flex justify-content-center align-items-center vh-100">
      <Card style={{ width: "24rem" }}>
        <Card.Header className="text-center bg-light">
          <a href="/">
            <img src="/path/to/logo-174x150.png" alt="logo" />
          </a>
        </Card.Header>
        <Card.Body>
          <div className="text-center w-75 m-auto">
            <h4 className="text-dark-50 pb-0 fw-bold">Employee Login</h4>
            <p className="text-muted mb-4">
              Enter your email address and password. First Time employee will
              have to register first.
            </p>
          </div>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Username</Form.Label>
              <FormControl
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Password</Form.Label>
              <InputGroup>
                <FormControl
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Password"
                />
                {/* The password-eye functionality is missing, as it requires additional scripting */}
                <InputGroup.Text>
                  <span className="password-eye"></span>
                </InputGroup.Text>
              </InputGroup>
              <Form.Text className="text-muted float-end">
                <a href="/password-reset">Forgot your password?</a>
              </Form.Text>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Check type="checkbox" label="Remember me" />
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

export default LoginForm;
