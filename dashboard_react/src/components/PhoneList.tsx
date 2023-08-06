import React from "react";

interface PhoneProps {
  phone_desc: { phone_desc: string };
  phone_number: string;
}

interface PhoneListProps {
  phones: PhoneProps[];
}

const PhoneList: React.FC<PhoneListProps> = ({ phones }) => {
  return (
    <>
      {phones.map((phone, i) => (
        <p key={i}>
          {phone.phone_desc.phone_desc}: {phone.phone_number}
        </p>
      ))}
    </>
  );
};

export default PhoneList;
