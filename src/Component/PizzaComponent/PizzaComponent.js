import React, { useEffect, useRef, useState } from "react";
import { Col, Container, Row, Spinner } from "react-bootstrap";
import PizzaCardComponent from "../PizzaCardComponent/PizzaCardComponent";
import { pizzaURL } from "../../constants/URLs";

function PizzaComponent() {
  const [isLoading, setIsLoading] = useState(true);
  const webSocket = useRef(null);
  const [pizzas, setPizzas] = useState([]);
  const [isWebsocket, setIsWebsocket] = useState(false);

  useEffect(() => {
    webSocket.current = new WebSocket(pizzaURL);

    webSocket.current.onopen = () => {
      setIsWebsocket(true);
    };

    webSocket.current.onmessage = (message) => {
      if (message !== undefined) {
        setPizzas(JSON.parse(message.data));
        setIsLoading(false);
      }
    };

    webSocket.current.onerror = (error) => {
      console.log(error);
      setIsWebsocket(false);
    };

    webSocket.current.onclose = () => {
      // webSocket.current.connect()
      setIsWebsocket(false);
    };

    return () => {
      webSocket.current.close();
    };
  }, []);

  const addOrder = (pizza, amount) => {
    webSocket.current.send(
      JSON.stringify({
        action: "order",
        user: "sarthak",
        pizza: pizza,
        amount: amount,
      })
    );
  };

  return (
    <Container>
      <Row>Websocket: {isWebsocket ? 'Yes': 'NO'}</Row>
      <Row className="mt-3">
        {isLoading ? (
          <Spinner variant="primary" />
        ) : (
          <>
            {pizzas.length > 0 ? (
              pizzas.map((item) => {
                return (
                  <Col key={item.image}>
                    <PizzaCardComponent
                      url={item.image}
                      title={item.name}
                      summary={`Price: ${item.price}`}
                      onClick={() => {
                        addOrder(item.name, item.price);
                      }}
                    />
                  </Col>
                );
              })
            ) : (
              <p className="text-danger">No Pizzas Added Yet</p>
            )}
          </>
        )}
      </Row>
    </Container>
  );
}

export default PizzaComponent;
