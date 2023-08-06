import "bootstrap/dist/css/bootstrap.css";
import React, { useEffect, useState } from "react";

type WorkItem = {
  repair_order_id: number;
  repair_order_serviced_vehicle_location: string;
  repair_order_service_status: string;
  // Add any other properties as needed.
};

function TechnicianView() {
  //Use the RepairOrder type to define the type of your repairOrders state
  const [WorkItems, setWorkItems] = useState<WorkItem[]>([]);
  const [error, setError] = useState<Error | null>(null);
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
        setWorkItems(data);
        setIsLoading(false);
      } catch (error) {
        setError(error as Error);
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const markAsFinished = (id: string) => {
    // implement functionality to mark a task as finished
  };

  const deleteTask = (id: string) => {
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
            {WorkItems.map((workitem) => (
              <tr key={workitem.repair_order_id}>
                <td>{workitem.repair_order_id}</td>
                <td>{workitem.repair_order_serviced_vehicle_location}</td>
                <td>{workitem.repair_order_service_status}</td>
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
