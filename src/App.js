import HeaderComponent from "./Component/HeaderComponent/HeaderComponent";
import OrderListComponent from "./Component/OrderListComponent/OrderListComponent";
import PizzaComponent from "./Component/PizzaComponent/PizzaComponent";

function App() {
  return (
    <div className="App">
      <HeaderComponent />
      <PizzaComponent />
      <OrderListComponent />
    </div>
  );
}

export default App;
