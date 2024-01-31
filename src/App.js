import './App.css';
import { AppProvider } from "./context/AppContext";
import Inicio from "./components/Inicio";
function App() {
  return (
    <div className="App">
      <AppProvider> 
        <Inicio />
      </AppProvider> 
    </div>
  );
}

export default App;
