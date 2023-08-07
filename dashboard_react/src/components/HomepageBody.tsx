import React, { useEffect, useState } from "react";
import {
  Button,
  Card,
  Col,
  Container,
  Row,
  Image,
  TabContainer,
} from "react-bootstrap";
import HomepageSection from "./HomepageSection";
import HomepageSection2 from "./HomepageSectionAlt";
import HomepageNotifications from "./HomepageNotifications";
import {
  Message,
  paragraphListItems,
  homepageParagraphs,
  serviceIcons,
  ServiceIcon,
  homepageRichTextContent,
  RichTextElement,
} from "./Types";

import {
  homepageBackgroundURL,
  homepageImageCar,
  homepageButtonLink,
  homepageButtonText,
  homepageImageUrl,
} from "./Constants";

type HomepageBodyProps = {
  messages: Message[];
  serviceIcons: ServiceIcon[];
};

const HomepageBody: React.FC<HomepageBodyProps> = ({
  messages,
  serviceIcons,
}) => {
  const [currentMessages, setMessages] = useState<Message[]>([
    //   Sample messages
    // { id: 1, type: "info", content: "This is an informational message." },
    // { id: 2, type: "error", content: "This is an error message." },
  ]);

  // Event handler for closing messages
  const handleCloseMessage = (messageId: number) => {
    const updatedMessages = messages.filter((msg) => msg.id !== messageId);
    setMessages(updatedMessages);
  };

  // Event handler for clicking on a service icon
  const handleServiceIconClick = (iconId: number) => {
    // For demonstration purposes, we'll just log the icon clicked.
    // In real use, you might navigate to a service page, show a modal, etc.
    const icon = serviceIcons.find((icon: ServiceIcon) => icon.id === iconId);
    console.log(`Clicked on: ${icon?.title}`);
  };
  return (
    <>
      {messages && messages.length > 0 && (
        <HomepageNotifications messages={messages} />
      )}
      <HomepageSection
        bgImageBackground={homepageBackgroundURL}
        richTextContent={homepageRichTextContent}
        paragraphs={homepageParagraphs}
        listItems={paragraphListItems}
        imageSrc={homepageImageCar}
        buttonLink={homepageButtonLink}
        buttonText={homepageButtonText}
        header="Your Trustworthy AI-Driven Automotive Repair Shop"
      >
        {/* this is the section that list out all service list in the format of
        service icons */}
        <Container className="bg-top-center bg-repeat-0 pt-5">
          <Row className="align-items-center justify-content-between mb-3 mb-sm-4 pb-sm-2">
            <Col>
              <h2 className="h3 text-dark my-2 mb-sm-0">Popular Services</h2>
            </Col>
            <Col className="text-end">
              <Button variant="link" className="btn-dark fw-normal px-0">
                View all
              </Button>
            </Col>
          </Row>
          <Row className="g-2 g-md-4">
            {serviceIcons.map((icon: ServiceIcon) => (
              <Col key={icon.id} xs={6} sm={4} md={3} lg={2}>
                <Card className="card-body card-dark card-hover bg-transparent border-0 px-0 pt-0 text-center">
                  <img
                    className="d-block mx-auto mb-3"
                    src={icon.imgSrc}
                    width="160"
                    alt={icon.alt}
                  />
                  <Card.Text className="stretched-link fw-bold">
                    {icon.title}
                  </Card.Text>
                </Card>
              </Col>
            ))}
          </Row>
        </Container>
        {/* this is the end of children section in HomepageBody that will pass onto HomepageSection  */}
        {/* <HomepageSection2
          richTextContent={homepageRichTextContent}
          imageUrl={homepageImageUrl}
        ></HomepageSection2> */}
      </HomepageSection>
    </>
  );
};

export default HomepageBody;
