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

function ServiceAdvisorView() {
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

  return (
    <>
      <h2>Service Advisor Dashboard React</h2>

      <MDBContainer className="py-5">
        <h2 className="text-center mb-4">Active Repair Order</h2>
        <MDBTable hover>
          <MDBTableHead>
            <tr>
              <th>Order ID</th>
              <th>Order Status</th>
              <th>Customer Name</th>
              <th>Phone Nbr</th>
              <th>Email Addresses</th>
              <th>Customer Address</th>
              <th>Updated Date</th>
            </tr>
          </MDBTableHead>
          <MDBTableBody>
            {repairOrders.map((order) => (
              <tr key={order.repair_order_id}>
                <td>{order.repair_order_id}</td>
                <td>{order.repair_order_service_status}</td>
                <td>
                  {order.customer_first_name} {order.customer_last_name}
                </td>
                <td>
                  {order.phones.map((phone) => (
                    <p key={phone.phone_id}>
                      {phone.phone_desc}: {phone.phone_number}
                    </p>
                  ))}
                </td>
                <td>
                  {order.emails.map((email) => (
                    <p key={email.email_id}>{email.email_address}</p>
                  ))}
                </td>
                <td>
                  {order.addresses.map((address) => (
                    <p key={address.address_id}>
                      {address.address_line_01}, {address.address_city},{" "}
                      {address.address_state} {address.address_zip_code}
                    </p>
                  ))}
                </td>
                <td>
                  {new Date(order.repair_order_last_updated_date).getFullYear()}
                </td>
              </tr>
            ))}
          </MDBTableBody>
        </MDBTable>
        {repairOrders.length === 0 && <p>There are no results found.</p>}
      </MDBContainer>
    </>
  );
}

export default ServiceAdvisorView;
