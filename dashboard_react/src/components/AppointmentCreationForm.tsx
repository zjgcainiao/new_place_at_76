import React, { useState } from "react";
// allows customer user, signed in or not, to create an appointment request. future sub for Django's appointments app. 2023-08-07 created.

interface AppointmentFormData {
  appointmentEmail: string;
  appointmentPhoneNumber: string;
  appointmentFirstName: string;
  appointmentLastName: string;
  appointmentRequestedDatetime: Date;
  appointmentReasonForVisit: string;
  appointmentVehicleYear: number;
  appointmentVehicleMake: string;
  appointmentVehicleModel: string;
  appointmentConcernDescription: string;
}

const initialFormData: AppointmentFormData = {
  appointmentEmail: "",
  appointmentPhoneNumber: "",
  appointmentFirstName: "",
  appointmentLastName: "",
  appointmentRequestedDatetime: new Date(),
  appointmentReasonForVisit: "",
  appointmentVehicleYear: new Date().getFullYear(),
  appointmentVehicleMake: "",
  appointmentVehicleModel: "",
  appointmentConcernDescription: "",
};

const AppointmentCreationView: React.FC = () => {
  const [formData, setFormData] = useState(initialFormData);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("here is the appointment form information submitted.");
    console.log(formData);
    // Submit logic here, like sending data to an API endpoint
  };

  return (
    <form onSubmit={handleSubmit} className="form-horizontal">
      {/* Time and Contact Info */}
      <fieldset>
        <legend>Time and Contact Info</legend>
        <div className="row p-1">
          <div className="col-md-6">
            <input
              type="email"
              name="appointmentEmail"
              value={formData.appointmentEmail}
              onChange={handleChange}
              className="form-control"
              placeholder="Email"
            />
          </div>
          <div className="col-md-6">
            <input
              type="tel"
              name="appointmentPhoneNumber"
              value={formData.appointmentPhoneNumber}
              onChange={handleChange}
              className="form-control"
              style={{ backgroundColor: "#cfe2f3" }}
              placeholder="Phone Number"
            />
          </div>
        </div>
        <div className="row p-1">
          {/* ... similar structure for other fields ... */}
        </div>
      </fieldset>

      <hr />

      {/* Vehicle & Concern */}
      <fieldset>
        <legend>Vehicle & Concern</legend>
        {/* ... */}
      </fieldset>

      <hr />

      {/* ... additional sections ... */}

      <hr />

      <div className="row p-1 m-1">
        <div className="col-md-6">
          <button type="submit" className="btn btn-outline-primary">
            Submit
          </button>
        </div>
        {/* ... reset button or other controls ... */}
      </div>
    </form>
  );
};

export default AppointmentCreationView;
