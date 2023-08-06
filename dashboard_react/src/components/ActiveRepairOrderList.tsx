import { Container } from "react-bootstrap";
import PhoneList from "./PhoneList";
import EmailList from "./EmailList";
import AddressList from "./AddressList";
import DataTable from "react-data-table-component";
import { DataGrid, GridColDef, GridValueGetterParams } from "@mui/x-data-grid";

interface PhoneProps {
  phone_desc: { phone_desc: string };
  phone_number: string;
}

interface PhonesProps {
  phones: PhoneProps[];
}

interface EmailsProps {
  emails: { email_address: string }[];
}

interface AddressProps {
  address_line_01: string;
  address_city: string;
  address_state: string;
  address_zip_code: string;
}

interface AddressesProps {
  addresses: AddressProps[];
}

interface OrderProps {
  repair_order_id: string;
  repair_order_service_status: string;
  repair_order_last_updated_date: string;
  repair_order_customer?: {
    customer_first_name: string;
    customer_last_name: string;
    phones: PhonesProps[];
    emails: EmailsProps[];
    addresses: AddressesProps[];
  };
}

interface ActiveRepairOrderListProps {
  repairOrders: OrderProps[];
}

const columns = [
  {
    name: "Order ID",
    selector: (row) => row.repair_order_id,
    sortable: true,
  },
  {
    name: "Order Status",
    selector: (row) => row.repair_order_service_status,
    sortable: true,
  },
  {
    name: "Customer Name",
    selector: (row: OrderProps) =>
      row.repair_order_customer
        ? `${row.repair_order_customer.customer_first_name} ${row.repair_order_customer.customer_last_name}`
        : "",
  },
  {
    name: "Phone Nbr",
    selector: (row) =>
      row.repair_order_customer && (
        <PhoneList phones={row.repair_order_customer.phones} />
      ),
    sortable: false,
  },
  {
    name: "Email Addresses",
    selector: (row) =>
      row.repair_order_customer && (
        <EmailList emails={row.repair_order_customer.emails} />
      ),
    sortable: false,
  },
  {
    name: "Customer Address",
    selector: (row) =>
      row.repair_order_customer && (
        <AddressList addresses={row.repair_order_customer.addresses} />
      ),
    sortable: false,
  },
  {
    name: "Updated Date",
    selector: (row) =>
      new Date(row.repair_order_last_updated_date).toLocaleDateString(),
    sortable: true,
  },
];

const ActiveRepairOrderList: React.FC<ActiveRepairOrderListProps> = ({
  repairOrders,
}) => {
  return (
    <>
      <Container className="mt-5">
        <h2 className="text-center mb-4">Work Station - Service Advisor</h2>
        <DataTable
          // title=""
          columns={columns}
          data={repairOrders}
          pointerOnHover={true}
          noHeader
          pagination
          highlightOnHover
          striped
          noDataComponent="There are no results found."
        />
      </Container>
    </>
  );
};

export default ActiveRepairOrderList;
