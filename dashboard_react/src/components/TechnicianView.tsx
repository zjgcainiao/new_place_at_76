import "bootstrap/dist/css/bootstrap.css";
import "mdb-react-ui-kit/dist/css/mdb.min.css";
import React, { useEffect, useState } from "react";
import {
  MDBBtn,
  MDBCard,
  MDBCardBody,
  MDBCol,
  MDBContainer,
  MDBInput,
  MDBRow,
  MDBTable,
  MDBTableBody,
  MDBTableHead,
} from "mdb-react-ui-kit";

function TechnicianView() {
  const [repairOrders, setRepairOrders] = useState([0]);
  const [error, setError] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        let response = await fetch(
          "http://192.168.1.48/apis/repair_orders/?format=json"
        );
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setRepairOrders(data);
        setIsLoading(false);
      } catch (error) {
        setError(error);
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const markAsFinished = (id) => {
    // implement functionality to mark a task as finished
  };

  const deleteTask = (id) => {
    // implement functionality to delete a task
  };

  return (
    <>
      <div className="container py-5">
        <h2 className="text-center mb-4">Technician Task List</h2>
        <table className="table">
          <thead>
            <tr>
              <th scope="col">Order ID</th>
              <th scope="col">Vehicle Location</th>
              <th scope="col">Service Status</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            {repairOrders.map((task) => (
              <tr key={task.repair_order_id}>
                <td>{task.repair_order_id}</td>
                <td>{task.repair_order_serviced_vehicle_location}</td>
                <td>{task.repair_order_service_status}</td>
                <td>
                  <button type="button" className="btn btn-success me-2">
                    Mark as finished
                  </button>
                  <button type="button" className="btn btn-primary">
                    Add Comment
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}

export default TechnicianView;
