import React from "react";
import HomepageNavbar from "./HomepageNavbar";
import HomepageBody from "./HomepageBody";
import { ServiceIcon, Message } from "./Types";
import { ExternalCSS } from "./ExternalCSS";

// Sample data for HomepageApp - you can pass these as props if they're coming from higher-level components or context.
const serviceIcons: ServiceIcon[] = [
  {
    id: 1,
    imgSrc: "/path/to/icon1.png",
    title: "Service 1",
    alt: "Service Icon 1",
  },
  {
    id: 2,
    imgSrc: "/path/to/icon2.png",
    title: "Service 2",
    alt: "Service Icon 2",
  },
];

const messages: Message[] = [
  { id: 1, type: "info", content: "This is an informational message." },
  { id: 2, type: "error", content: "This is an error message." },
];

const HomepageApp: React.FC = () => {
  return (
    <div className="homepage-app">
      <ExternalCSS href="https://storage.googleapis.com/2023_new_prolube76site/homepageapp/css/theme.min.css" />
      <HomepageNavbar />
      <HomepageBody messages={messages} serviceIcons={serviceIcons} />
      {/* Add other components like <Footer /> if you have them */}
    </div>
  );
};

export default HomepageApp;
