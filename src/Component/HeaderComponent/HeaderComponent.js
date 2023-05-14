import React from "react";
import { Container, Nav, Navbar } from "react-bootstrap";

function HeaderComponent() {
  return (
    <Navbar bg="light" expand="lg">
      <Container>
        <Navbar.Brand href="#home">Pizza App</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />        
      </Container>
    </Navbar>
  );
}

export default HeaderComponent;
