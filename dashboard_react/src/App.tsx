// import reactLogo from "./assets/react.svg";
import "./App.css";

import React, { useEffect, useState } from "react";

function App() {
  const [repairOrders, setRepairOrders] = useState([]);

  useEffect(() => {
    fetch("/apis/repair_orders/")
      .then((response) => response.json())
      .then((data) => setRepairOrders(data));
  }, []);

  return (
    <>
      <h2>here is the react-based Dashboard View for Service Advisor</h2>
      {/* display your data here */}
      {repairOrders.map((order) => (
        <p>{order.repair_order_id}</p>
      ))}
    </>
  );
}

export default App;
