import React, { useEffect, useRef, useState } from "react";
import {
  Button,
  Col,
  Container,
  ProgressBar,
  Row,
  Spinner,
  Table,
} from "react-bootstrap";
import { userOrderURL } from "../../constants/URLs";

function OrderListComponent() {
  const [isLoading, setIsLoading] = useState(true);
  const [orders, setOrders] = useState([]);
  const webSocket = useRef();
  const [isWebsocket, setIsWebsocket] = useState(false);

  useEffect(() => {
    webSocket.current = new WebSocket(`${userOrderURL}/sarthak`);

    webSocket.current.onopen = () => {
      setIsWebsocket(true);
    };

    webSocket.current.onmessage = (message) => {
      console.log(JSON.parse(message.data));
      if (message !== undefined) {
        setOrders(JSON.parse(message.data));
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

  const deleteMyOrder = (order_id) => {
    webSocket.current.send(
      JSON.stringify({
        action: "delete",
        order_id,
      })
    );
  };

  return (
    <Container className="mt-3">
      <Row>
        <hr />
        <h3>Orders</h3>
        <Row>
          <Col>Websocket {isWebsocket ? "Yes" : "NO"}</Col>
        </Row>
        <Col>
          {isLoading ? (
            <Spinner variant="primary" />
          ) : (
            <Table responsive striped>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Order ID</th>
                  <th>Name</th>
                  <th>Amount</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {orders.length > 0 ? (
                  orders.map((item, index) => {
                    return (
                      <tr key={item.order_id}>
                        <td>{index + 1}</td>
                        <td>{item.order_id}</td>
                        <td>{item.pizza}</td>
                        <td>{item.amount}</td>
                        <td>
                          <Row>
                            <Col>
                              <Button
                                variant={
                                  parseInt(item.progress) === 100
                                    ? "success"
                                    : "primary"
                                }
                              >
                                {item.status}
                              </Button>
                            </Col>
                            <Col>
                              <ProgressBar
                                animated
                                variant={
                                  parseInt(item.progress) === 100
                                    ? "success"
                                    : "primary"
                                }
                                now={parseInt(item.progress)}
                              />
                            </Col>
                          </Row>
                        </td>
                        <td>
                          <Row>
                            <Col>
                              <Button variant="primary" onClick={() => {}}>
                                View
                              </Button>
                            </Col>
                            <Col>
                              <Button
                                variant="danger"
                                onClick={() => {
                                  deleteMyOrder(item.order_id);
                                }}
                              >
                                Delete
                              </Button>
                            </Col>
                          </Row>
                        </td>
                      </tr>
                    );
                  })
                ) : (
                  <p className="text-success">No orders yet book now</p>
                )}
              </tbody>
            </Table>
          )}
        </Col>
      </Row>
    </Container>
  );
}

export default OrderListComponent;
