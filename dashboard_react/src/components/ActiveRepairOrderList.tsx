import {
  MDBContainer,
  MDBTable,
  MDBTableBody,
  MDBTableHead,
} from "mdb-react-ui-kit";
import PhoneList from "./PhoneList";
import EmailList from "./EmailList";
import AddressList from "./AddressList";
import DataTable from "react-data-table-component";

interface PhoneProps {
  phone_desc: { phone_desc: string };
  phone_number: string;
}

interface AddressProps {
  address_line_01: string;
  address_city: string;
  address_state: string;
  address_zip_code: string;
}

interface EmailProps {
  email_address: string;
}

interface OrderProps {
  repair_order_id: string;
  repair_order_service_status: string;
  repair_order_last_updated_date: string;
  repair_order_customer?: {
    customer_first_name: string;
    customer_last_name: string;
    phones: PhoneProps[];
    emails: EmailProps[];
    addresses: AddressProps[];
  };
}

interface ActiveRepairOrderListProps {
  repairOrders: OrderProps[];
}

const ActiveRepairOrderList: React.FC<ActiveRepairOrderListProps> = ({
  repairOrders,
}) => {
  return (
    <>
      <MDBContainer className="mt-5">
        <h2 className="text-center mb-4">Work Station - Service Advisor</h2>
        <MDBTable className="table-light table-hover">
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
            {repairOrders.length > 0 ? (
              repairOrders.map((order) => (
                <tr key={order.repair_order_id}>
                  <td>{order.repair_order_id}</td>
                  <td>{order.repair_order_service_status}</td>
                  <td>
                    {order.repair_order_customer
                      ? `${order.repair_order_customer.customer_first_name} ${order.repair_order_customer.customer_last_name}`
                      : ""}
                  </td>
                  <td>
                    {order.repair_order_customer && (
                      <PhoneList phones={order.repair_order_customer.phones} />
                    )}
                  </td>
                  <td>
                    {order.repair_order_customer && (
                      <EmailList emails={order.repair_order_customer.emails} />
                    )}
                  </td>
                  <td>
                    {order.repair_order_customer && (
                      <AddressList
                        addresses={order.repair_order_customer.addresses}
                      />
                    )}
                  </td>
                  <td>
                    {new Date(
                      order.repair_order_last_updated_date
                    ).toLocaleDateString()}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={7}>There are no results found.</td>
              </tr>
            )}
          </MDBTableBody>
        </MDBTable>
      </MDBContainer>
    </>
  );
};

export default ActiveRepairOrderList;
