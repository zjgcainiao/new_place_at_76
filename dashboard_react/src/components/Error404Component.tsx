import React, { CSSProperties } from "react";

const Error404Component: React.FC = () => {
  return (
    <div style={styles.container}>
      <h1 style={styles.code}>404</h1>
      <p style={styles.message}>Page Not Found</p>
    </div>
  );
};

const styles: { [key: string]: CSSProperties } = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    height: "100vh",
    background: "#f7f7f7",
  },
  code: {
    fontSize: "5rem",
    fontWeight: "bold",
    color: "#333",
  },
  message: {
    fontSize: "1.5rem",
    color: "#555",
  },
};

export default Error404Component;
