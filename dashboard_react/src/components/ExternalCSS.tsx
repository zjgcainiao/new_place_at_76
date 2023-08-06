import React, { useEffect } from "react";

type ExternalCSSProps = {
  href: string;
  type?: string;
  media?: string;
};

export const ExternalCSS: React.FC<ExternalCSSProps> = ({
  href,
  type = "text/css",
  media = "all",
}) => {
  useEffect(() => {
    const link = document.createElement("link");
    link.href = href;
    link.rel = "stylesheet";
    link.type = type;
    link.media = media;

    // Event listener for error handling (optional)
    link.onerror = () => {
      console.error(`Failed to load stylesheet: ${href}`);
    };

    document.head.appendChild(link);

    // Clean-up function
    return () => {
      document.head.removeChild(link);
    };
  }, [href, type, media]);

  return null; // This component doesn't render anything
};
