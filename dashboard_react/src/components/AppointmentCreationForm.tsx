import React, { useState, ChangeEvent, FormEvent } from "react";
import {
  Form,
  Button,
  Row,
  Col,
  Container,
  InputGroup,
  FormControl,
} from "react-bootstrap";
// https://www.npmjs.com/package/react-datetime
import Datetime from "react-datetime";
import "react-datetime/css/react-datetime.css";
interface AppointmentFormData {
  appointment_email: string;
  appointment_phone_number: string;
  appointment_first_name?: string;
  appointment_last_name?: string;
  appointment_requested_datetime?: Date;
  appointment_reason_for_visit?: string;
  appointment_vehicle_year?: string;
  appointment_vehicle_make?: string;
  appointment_vehicle_model?: string;
  appointment_concern_description: string;
  appointment_images?: FileList | null;
}

const AppointmentCreationForm: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<number>(1);
  const nextStep = () => setCurrentStep((prevStep) => prevStep + 1);
  const prevStep = () => setCurrentStep((prevStep) => prevStep - 1);
  const [formData, setFormData] = useState<AppointmentFormData>({
    appointment_email: "",
    appointment_phone_number: "",
    appointment_first_name: "",
    appointment_last_name: "",
    appointment_requested_datetime: new Date(),
    appointment_reason_for_visit: "",
    appointment_vehicle_year: "",
    appointment_vehicle_make: "",
    appointment_vehicle_model: "",
    appointment_concern_description: "",
    appointment_images: null,
  });

  const handleInputChange = (
    e: ChangeEvent<HTMLTextAreaElement | HTMLSelectElement | HTMLInputElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prevData: AppointmentFormData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFormData((prevData: AppointmentFormData) => ({
      ...prevData,
      appointment_images: e.target.files,
    }));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    // Do your submission logic here...
  };

  return (
    <Container className="m-2 p-2 ">
      <Form onSubmit={handleSubmit} className="m-1 p-1">
        {/* Conditionally render steps based on currentStep state */}

        {/* Conditionally render steps based on currentStep state */}
        {currentStep === 1 && (
          <>
            <p className="m-1 p-1">
              Welcome to our appointment system! We value your time, and we've
              made this process straightforward to help you schedule a visit
              with ease. You're a few steps away from finalizing your
              appointment. Kindly provide the necessary details in the following
              pages to ensure a seamless experience.
            </p>

            <Form.Group as={Row}>
              <Col md={5} className="m-1 p-1">
                <Form.Control
                  type="datetime-local"
                  name="appointment_requested_datetime"
                  value={formData.appointment_requested_datetime
                    ?.toISOString()
                    .slice(0, 16)}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                    setFormData((prev) => ({
                      ...prev,
                      appointment_requested_datetime: new Date(e.target.value),
                    }));
                  }}
                />
              </Col>
              <Col md={5} className="m-1 p-1">
                <Form.Control
                  type="text"
                  name="appointment_reason_for_visit"
                  value={formData.appointment_reason_for_visit}
                  onChange={handleInputChange}
                  placeholder="choose from one of the following"
                />
              </Col>
              <Col md={5} className="m-1 p-1">
                <Form.Control
                  type="email"
                  name="appointment_email"
                  value={formData.appointment_email}
                  onChange={handleInputChange}
                  placeholder="Contact Email"
                  style={{ backgroundColor: "#cfe2f3" }}
                />
              </Col>
              <Col md={5} className="m-1 p-1">
                <Form.Control
                  type="tel"
                  name="appointment_phone_number"
                  value={formData.appointment_phone_number}
                  onChange={handleInputChange}
                  placeholder="Contact Phone Number"
                  style={{ backgroundColor: "#cfe2f3" }}
                />
              </Col>
              <Col md={5} className="m-1 p-1">
                <Form.Control
                  type="text"
                  name="appointment_first_name"
                  value={formData.appointment_first_name}
                  onChange={handleInputChange}
                  placeholder="First Name"
                />
              </Col>
              <Col md={5} className="m-1 p-1">
                <Form.Control
                  type="text"
                  name="aappointment_last_name"
                  value={formData.appointment_last_name}
                  onChange={handleInputChange}
                  placeholder="Last Name"
                />
              </Col>
              <Col md={5} className="m-1 p-1">
                <Form.Control
                  type="text"
                  name="appointment_vehicle_year"
                  value={formData.appointment_vehicle_year}
                  onChange={handleInputChange}
                  placeholder="enter full year, i.e. 2020"
                />
              </Col>
              <Col md={5} className="m-1 p-1">
                <Form.Control
                  type="form-select"
                  name="appointment_vehicle_make"
                  value={formData.appointment_vehicle_make}
                  onChange={handleInputChange}
                  placeholder="for instance, Toyota, Honda, Kia, etc."
                />
              </Col>
              <Col md={6} className="m-1 p-1">
                <Form.Control
                  type="text"
                  className="form-select"
                  name="appointment_vehicle_model"
                  value={formData.appointment_vehicle_model}
                  onChange={handleInputChange}
                  placeholder="choose one if you know. optional."
                />
              </Col>

              <Col md={6} className="m-1 p-1">
                <Form.Control
                  type="text"
                  name=" appointment_concern_description"
                  value={formData.appointment_concern_description}
                  onChange={handleInputChange}
                  placeholder="Examples: 1. I want to do a oil change for 2020 Toyota Sienna. Full Synthetic as usual. 2. My A/C system does not cool enough during a hot day. Last week, i drove to ... 3. The engine acted weird this morning, the car suddenly lost power on a freeway ramp..."
                />
              </Col>
            </Form.Group>

            <Button variant="outline-primary" onClick={nextStep}>
              Next
            </Button>
          </>
        )}

        {currentStep === 2 && (
          <div>
            {/* Image Upload Input */}
            <Form.Group as={Row} className="p-1 m-1">
              <Col md={6}>
                <Form.Control
                  type="file"
                  name="appointment_images"
                  onChange={handleInputChange}
                />
              </Col>
            </Form.Group>

            <Button variant="outline-secondary" onClick={prevStep}>
              Back
            </Button>
            <Button variant="outline-primary" onClick={nextStep}>
              Next
            </Button>
          </div>
        )}

        {currentStep === 3 && (
          <div>
            {/* Render all form data in a readable manner for the user to review */}
            <div>
              {Object.entries(formData).map(([key, value]) => (
                <p key={key}>
                  <strong>{key.charAt(0).toUpperCase() + key.slice(1)}:</strong>{" "}
                  {value}
                </p>
              ))}
              {/* ... repeat for all other fields ... */}
            </div>

            <Button variant="outline-secondary" onClick={prevStep}>
              Back
            </Button>
            <Button variant="outline-primary" type="submit">
              Submit
            </Button>
          </div>
        )}
        {/* <Form.Group as={Row} className="p-1">
          <Col md={6}>
            <Form.Control
              type="email"
              name="appointment_email"
              value={formData.appointment_email}
              onChange={handleInputChange}
              placeholder="Contact Email"
              style={{ backgroundColor: "#cfe2f3" }}
            />
          </Col>
          <Col md={6}>
            <Form.Control
              type="tel"
              name="appointment_phone_number"
              value={formData.appointment_phone_number}
              onChange={handleInputChange}
              placeholder="Contact Phone Number"
              style={{ backgroundColor: "#cfe2f3" }}
            />
          </Col>
        </Form.Group> */}
        {/* ... (Continue similarly for the rest of the fields) ... */}
        <hr />

        {/* <Form.Group as={Row} className="p-1 m-1">
          <Col md={6}>
            <Button type="submit" variant="outline-primary">
              Submit
            </Button>
          </Col>
        </Form.Group> */}
      </Form>
    </Container>
  );
};

export default AppointmentCreationForm;
