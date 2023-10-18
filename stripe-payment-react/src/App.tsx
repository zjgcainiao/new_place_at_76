import { useState } from "react";
import reactLogo from "./assets/react.svg";
import "./App.css";
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
import StripePaymentForm from "./components/";
import { Elements } from "@stripe/react-stripe-js";
import { loadStripe } from "@stripe/stripe-js";

function App() {
  const [count, setCount] = useState(0);
  const stripePromise = loadStripe("your_stripe_public_key");
  return (
    <div className="App">
      <Elements stripe={stripePromise}>
        <StripePaymentForm />
      </Elements>
    </div>
    // end of app
  );
}

export default App;
