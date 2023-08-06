import React from "react";

interface EmailListProps {
  emails: { email_address: string }[];
}

const EmailList: React.FC<EmailListProps> = ({ emails }) => {
  return (
    <>
      {emails.map((email, i) => (
        <p key={i}>{email.email_address}</p>
      ))}
    </>
  );
};

export default EmailList;
