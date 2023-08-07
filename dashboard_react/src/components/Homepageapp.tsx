import React from "react";
import HomepageNavbar from "./HomepageNavbar";
import HomepageBody from "./HomepageBody";
import { serviceIcons, Message } from "./Types";

const messages: Message[] = [
  //   { id: 1, type: "info", content: "This is an informational message." },
  //   { id: 2, type: "error", content: "This is an error message." },
];

const HomepageApp: React.FC = () => {
  return (
    <div className="homepage-app">
      <HomepageNavbar />
      <HomepageBody messages={messages} serviceIcons={serviceIcons} />
      {/* Add other components like <Footer /> if you have them */}
    </div>
  );
};

export default HomepageApp;
