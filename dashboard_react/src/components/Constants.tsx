import { RichTextElement } from "./Types";
import React, { useState, useEffect } from "react";

export const logo =
  "https://storage.googleapis.com/2023_new_prolube76site/homepageapp/2022-Logo-Transparent-small.png";

export const homepageBackgroundURL =
  "https://storage.googleapis.com/2023_new_prolube76site/homepageapp/img/home/hero-bg.png";

export const homepageImageCar =
  "https://storage.googleapis.com/2023_new_prolube76site/homepageapp/img/2023-05-27-tesla-roadster-sports-car-tesla-motors-car.png";

export const homepageButtonLink = "/appts/create";
export const homepageButtonText = "Service Appointment";
export const homepageImageUrl =
  "https://storage.googleapis.com/2023_new_prolube76site/homepageapp/img/2023-05-27-tesla-roadster-sports-car-tesla-motors-car.png";

export const homepageAppExternalCSS =
  "https://storage.googleapis.com/2023_new_prolube76site/homepageapp/css/theme.min.css";

export const InternalUserLoginAPI =
  "http://localhost/apis/internal_user_login/";

export const RepairOrderAPI =
  "http://localhost/apis/repair_orders/?format=json";

export const homepageRichTextContent: RichTextElement[] = [
  {
    type: "p",
    content:
      "We strive to offer a seamless and transparent service experience. Our integrated system unifies appointments, repair orders, and customer information, enabling real-time tracking of active work orders and appointments. Be it an early part arrival or an unforeseen delay, we keep you updated.",
  },
  {
    type: "p",
    content:
      "Our mission surpasses that of traditional dealerships - we pledge to keep you informed frequently about your car's repair status.",
  },
  {
    type: "p",
    content: "Our unique strengths include:",
  },
  {
    type: "ul",
    content: [
      "Vertical Integration: Real-time tracking of repair status and online payments.",
      "Automation: Eliminating repetitive tasks to boost efficiency.",
      "AI-Driven Solutions: Leveraging AI to answer customer queries, set to launch in 2024.",
    ],
  },
  {
    type: "p",
    content:
      "Start your journey with us by booking an online service appointment for issues like oil changes, A/C issues, etc.",
  },
];
