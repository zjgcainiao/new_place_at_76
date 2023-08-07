import { Container } from "react-bootstrap";
import PhoneList from "./PhoneList";
import EmailList from "./EmailList";
import AddressList from "./AddressList";
import DataTable, { TableColumn } from "react-data-table-component";
// import { DataGrid, GridColDef, GridValueGetterParams } from "@mui/x-data-grid";
import _ from "lodash";
import { debounce } from "lodash";

interface PhoneProps {
  phone_desc: { phone_desc: string };
  phone_number: string;
}

interface PhonesProps {
  phones: PhoneProps[];
}

interface EmailProps {
  email_address: string;
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
  repair_order_customer: {
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

const columns: TableColumn<OrderProps>[] = [
  {
    name: "Order ID",
    selector: (row: OrderProps) => row.repair_order_id,
    sortable: true,
  },
  {
    name: "Order Status",
    selector: (row: OrderProps) => row.repair_order_service_status,
    sortable: true,
  },
  {
    name: "Customer Name",
    cell: (row: OrderProps) => {
      if (row.repair_order_customer) {
        const names = _.startCase(
          row.repair_order_customer.customer_first_name +
            " " +
            row.repair_order_customer.customer_last_name
        )
          .trim()
          .split(" ");
        const firstName = names.slice(0, -1).join(" ");
        const lastName = names.slice(-1).join(" ");
        return (
          <>
            {firstName} &nbsp;&nbsp;<strong>{lastName}</strong>
          </>
        );
      }
      return "";
    },
    sortable: true,
  },
  {
    name: "Phones",
    cell: (row: OrderProps) =>
      row.repair_order_customer ? (
        <PhoneList phones={row.repair_order_customer.phones} />
      ) : null,
  },
  {
    name: "Email Addresses",
    cell: (row: OrderProps) =>
      row.repair_order_customer ? (
        <EmailList emails={row.repair_order_customer.emails} />
      ) : null,
  },
  {
    name: "Customer Address",
    cell: (row: OrderProps) =>
      row.repair_order_customer ? (
        <AddressList addresses={row.repair_order_customer.addresses} />
      ) : null,
  },
  {
    name: "Updated Date",
    selector: (row: OrderProps) =>
      new Date(row.repair_order_last_updated_date).toLocaleDateString(),
    sortable: true,
  },
];
// Explicitly declared the type for the selectedRows parameter in the handleChange function.
const handleChange = ({ selectedRows }: { selectedRows: OrderProps[] }) => {
  // You can set state or dispatch with something like Redux so we can use the retrieved data
  console.log("Selected Rows: ", selectedRows);
};

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
          selectableRows
          onSelectedRowsChange={handleChange}
        />
      </Container>
    </>
  );
};

export default ActiveRepairOrderList;
