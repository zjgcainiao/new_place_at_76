import "bootstrap/dist/css/bootstrap.css";
// import "mdb-react-ui-kit/dist/css/mdb.min.css";
import React, { useEffect, useState } from "react";
import ActiveRepairOrderList from "./ActiveRepairOrderList";

function ServiceAdvisorView() {
  // const [repairOrders, setRepairOrders] = useState([]);
  // const [error, setError] = useState([]);
  // const [isLoading, setIsLoading] = useState(true);
  const [repairOrders, setRepairOrders] = useState<any[]>([]);
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        let response = await fetch(
          "http://localhost/apis/repair_orders/?format=json"
        );
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setRepairOrders(data);
        setIsLoading(false);
      } catch (error) {
        if (error instanceof Error) {
          setError(error);
        } else {
          setError(new Error("An unexpected error occurred."));
        }
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  return <ActiveRepairOrderList repairOrders={repairOrders} />;
}

export default ServiceAdvisorView;
