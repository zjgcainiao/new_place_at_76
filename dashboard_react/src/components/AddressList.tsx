import React from "react";

interface AddressProps {
  address_line_01: string;
  address_city: string;
  address_state: string;
  address_zip_code: string;
}

interface AddressListProps {
  addresses: AddressProps[];
}

const AddressList: React.FC<AddressListProps> = ({ addresses }) => {
  return (
    <>
      {addresses.map((address, i) => (
        <p key={i}>
          {address.address_line_01}, {address.address_city},
          {address.address_state} {address.address_zip_code}
        </p>
      ))}
    </>
  );
};

export default AddressList;
