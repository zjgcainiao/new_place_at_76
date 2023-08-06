export interface InternalUser {
  email: string;
  password?: string;
  is_technician?: boolean;
  // Add any other fields you might have
}

export interface Message {
  id: number; // unique identifier to manage the removal from the list
  type: "info" | "error" | "success"; // assuming these are the message types, you can add or adjust as needed
  content: string;
}

export interface ServiceIcon {
  id: number;
  imgSrc: string;
  title: string;
  alt: string;
}
