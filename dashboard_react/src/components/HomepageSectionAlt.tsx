import React from "react";
import { Container, Row, Col, Image } from "react-bootstrap";
import { RichTextElement } from "./Types";

interface SectionProps {
  richTextContent?: RichTextElement[];
  imageUrl?: string;
}

const HomepageSection2: React.FC<SectionProps> = ({
  richTextContent = [],
  imageUrl,
}) => {
  return (
    <Container fluid className="my-5">
      <Row>
        {/* Left Part (Rich Text Content) */}
        <Col lg={6} md={12} sm={12}>
          {richTextContent.map((element, index) => {
            switch (element.type) {
              case "p":
                return (
                  <p key={index} className="fs-lg text-dark opacity-70">
                    {element.content}
                  </p>
                );
              case "ul":
                return (
                  <ul key={index} className="fs-lg text-dark opacity-70">
                    {element.content.map((item, liIndex) => (
                      <li key={liIndex}>{item}</li>
                    ))}
                  </ul>
                );
              case "ol":
                return (
                  <ol key={index} className="fs-lg text-dark opacity-70">
                    {element.content.map((item, liIndex) => (
                      <li key={liIndex}>{item}</li>
                    ))}
                  </ol>
                );
              default:
                return null;
            }
          })}
        </Col>

        {/* Right Part (Image) */}
        <Col
          lg={6}
          md={12}
          sm={12}
          className="d-flex align-items-center justify-content-center"
        >
          <Image src={imageUrl} alt="Car Image" fluid />
        </Col>
      </Row>
    </Container>
  );
};

export default HomepageSection2;
