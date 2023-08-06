import React from "react";

import { Message } from "./Types";
// type Message = {
//   text: string;
//   type: "info" | "warning" | "error" | "debug"; // Add more types if needed
// };

const HomepageNotifications: React.FC<{ messages: Message[] }> = ({
  messages,
}) => {
  return (
    <div className="pt-5">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`alert alert-${message.type} alert-dismissible fade show justify-content-center justify-content-between`}
          role="alert"
        >
          {message.content}
          <button
            type="button"
            className="close"
            data-bs-dismiss="alert"
            aria-label="Close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
      ))}
    </div>
  );
};

export default HomepageNotifications;
