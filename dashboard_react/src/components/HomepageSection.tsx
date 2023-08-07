import React from "react";
import {
  Button,
  Alert,
  Figure,
  Container,
  TabContainer,
} from "react-bootstrap";
import { RichTextElement } from "./Types";
import { Message, ServiceIcon } from "./Types";

import HomepageSection2 from "./HomepageSectionAlt";
import { homepageBackgroundURL } from "./Constants";
import Spinner from "react-bootstrap/Spinner";

export interface HomepageSectionProps {
  bgImageBackground?: string;
  header?: string; // add the ? to make the field optoinal
  children?: React.ReactNode;
  richTextContent?: RichTextElement[];
  paragraphs?: string[];
  listItems?: string[];
  buttonText?: string;
  buttonLink?: string;
  imageSrc?: string;
  imageAlt?: string;
  messages?: Message[];
  serviceIcons?: ServiceIcon[];
  onMessageClose?: (messageId: number) => void;
  onButtonClick?: () => void;
}

const HomepageSection: React.FC<HomepageSectionProps> = ({
  // bgImageBackground = homepageBackgroundURL,
  // assuming bgImagBackground will get value from props passed on from HomepageBody.
  bgImageBackground,
  header,
  children,
  richTextContent = [],
  paragraphs = [],
  listItems = [],
  buttonText,
  buttonLink,
  imageSrc,
  imageAlt,
  messages = [],
  onMessageClose,
  onButtonClick,
}) => {
  return (
    <section
      className="bg-top-center bg-repeat-0 pt-5"
      style={
        bgImageBackground
          ? {
              backgroundImage: `url(${bgImageBackground})`,
              backgroundSize: "cover",
            }
          : undefined
      }
    >
      {messages.length > 0 && (
        <div className="container pt-5">
          {messages.map((message) => (
            <Alert
              key={message.id}
              variant={message.type}
              onClose={() => onMessageClose && onMessageClose(message.id)}
              dismissible
            >
              {message.content}
            </Alert>
          ))}
        </div>
      )}
      <div className="container pt-2">
        <article className="row pt-lg-3 pt-xl-4">
          <section className="col-md-7 pt-3 pt-md-3 pt-lg-5">
            <header>
              <h2 className="text-dark pb-2 mb-4 me-md-n5">{header}</h2>
            </header>
            <div className="content-body">
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
              {buttonText && buttonLink && (
                <Button
                  variant="outline-primary"
                  size="sm"
                  onClick={onButtonClick}
                  href={buttonLink}
                >
                  {buttonText}
                </Button>
              )}
            </div>
          </section>
          {imageSrc && (
            <figure className="col-md-5 p-md-5">
              <img
                className="d-block mt-4 ms-auto"
                src={imageSrc}
                width="800"
                alt={imageAlt || ""}
              />
            </figure>
          )}
        </article>
      </div>
      {children} {/* Render the children prop content here */}
    </section>
  );
};

export default HomepageSection;
