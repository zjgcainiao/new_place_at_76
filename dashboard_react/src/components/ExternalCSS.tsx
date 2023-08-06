import React, { useEffect, useState } from "react";

export const ExternalCSS: React.FC<{ href: string }> = ({ href }) => {
  useEffect(() => {
    const link = document.createElement("link");
    link.href = href;
    link.rel = "stylesheet";
    document.head.appendChild(link);

    // Clean-up function
    return () => {
      document.head.removeChild(link);
    };
  }, [href]);

  return null; // This component doesn't render anything
};
