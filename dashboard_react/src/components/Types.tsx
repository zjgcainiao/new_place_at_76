import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export interface InternalUser {
  email: string;
  password?: string;
  is_technician?: boolean;
  is_talent_management?: boolean;
  // Add any other fields you might have
}
import logo from "https://storage.googleapis.com/2023_new_prolube76site/homepageapp/2022-Logo-Transparent-small.png"; // Adjust the path accordingly

export interface Message {
  id: number; // unique identifier to manage the removal from the list
  type: "info" | "error" | "success"; // assuming these are the message types, you can add or adjust as needed
  content: string;
}
export type ServiceIcon = {
  id: number;
  imgSrc: string;
  title: string;
  alt: string;
};

export const serviceIcons: ServiceIcon[] = [
  {
    id: 1,
    imgSrc:
      "https://storage.googleapis.com/2023_new_prolube76site/homepageapp/img/svgs/car-maintenance-icon.svg",
    alt: "car car-maintenance-oil-change",
    title: "Oil Changes",
  },
  {
    id: 2,
    imgSrc:
      "https://storage.googleapis.com/2023_new_prolube76site/homepageapp/img/svgs/air-conditioning-icon.svg",
    alt: "a/c-system-diagnosis-and-repair",
    title: "Air Conditioning Not Cooling & Heating",
  },
  {
    id: 3,
    imgSrc:
      "https://storage.googleapis.com/2023_new_prolube76site/homepageapp/img/svgs/engine-icon.svg",
    alt: "engine",
    title: "Engine Repair (w/ service lights on, overheating, etc)",
  },
  {
    id: 4,
    imgSrc:
      "https://storage.googleapis.com/2023_new_prolube76site/homepageapp/img/svgs/battery-svgrepo-com-icon.svg",
    alt: "Family MPV",
    title: "Car Battery Service",
  },
  {
    id: 5,
    imgSrc:
      "https://storage.googleapis.com/2023_new_prolube76site/homepageapp/img/svgs/electrical-service-icon.svg",
    alt: "Compact",
    title: "Electric Diagnosis",
  },
  {
    id: 6,
    imgSrc:
      "https://storage.googleapis.com/2023_new_prolube76site/homepageapp/img/svgs/brake-icon.svg",
    alt: "Convertible",
    title: "Brake Replacements",
  },
  {
    id: 7,
    imgSrc:
      "https://storage.googleapis.com/2023_new_prolube76site/homepageapp/img/svgs/spark-spark-plug-svgrepo-com-icon.svg",
    alt: "spark-plug",
    title: "Spark Plugs",
  },
  {
    id: 8,
    imgSrc:
      "https://storage.googleapis.com/2023_new_prolube76site/homepageapp/img/svgs/gear-shift-stick-svgrepo-com-icon.svg",
    alt: "transmission",
    title: "Transmission Service",
  },
  {
    id: 9,
    imgSrc:
      "https://storage.googleapis.com/2023_new_prolube76site/homepageapp/img/svgs/windshield-icon.svg",
    alt: "Windshield-Wipers",
    title: "Windshield Wiper",
  },
  {
    id: 10,
    imgSrc:
      "https://storage.googleapis.com/2023_new_prolube76site/homepageapp/img/svgs/suspension-icon.svg",
    alt: "suspension",
    title: "Suspension Service",
  },
];

export const homepageParagraphs = [
  "We strive to offer a seamless and transparent service experience. Our integrated system unifies appointments, repair orders, and customer information, enabling real-time tracking of active work orders and appointments. Be it an early part arrival or an unforeseen delay, we keep you updated.",

  "Our mission surpasses that of traditional dealerships - we pledge to keep you informed frequently about your car's repair status.",

  "Our unique strengths include:",

  "Vertical Integration: Real-time tracking of repair status and online payments.",
  "Automation: Eliminating repetitive tasks to boost efficiency.",
  "AI-Driven Solutions: Leveraging AI to answer customer queries, set to launch in 2024.",
  "Start your journey with us by booking an online service appointment for issues like oil changes, A/C issues, etc.",
];

export const paragraphListItems = [
  "Vertical Integration: Real-time tracking of repair status and online payments.",
  "Automation: Eliminating repetitive tasks to boost efficiency.",
  "AI-Driven Solutions: Leveraging AI to answer customer queries, set to launch in 2024.",
];

export type RichTextElement =
  | { type: "p"; content: string }
  | { type: "ul"; content: string[] }
  | { type: "ol"; content: string[] }; // You can extend this with more types if needed

// custom component to do redirect
export const CustomRedirectTo: React.FC<{ to: string }> = ({ to }) => {
  const navigate = useNavigate();
  React.useEffect(() => {
    navigate(to);
  }, [to, navigate]);

  return null;
};
