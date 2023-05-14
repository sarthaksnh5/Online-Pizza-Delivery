import React from "react";
import { Button, Card } from "react-bootstrap";

function PizzaCardComponent({ url, title, summary, onClick }) {
  return (
    <Card style={{ width: "18rem" }}>
      <Card.Img variant="top" src={url} />
      <Card.Body>
        <Card.Title>{title}</Card.Title>
        <Card.Text>{summary}</Card.Text>
        <Button variant="primary" onClick={onClick}>
          Order
        </Button>
      </Card.Body>
    </Card>
  );
}

export default PizzaCardComponent;
