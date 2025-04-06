import React from "react";
import {Route, Routes} from "react-router-dom";
import {Header} from "./components/header.tsx";
import Home from "./pages/Home.tsx";
import {StartPage} from "./pages/StartPage.tsx";
import {Parameters} from "./pages/Parameters.tsx";

const App: React.FC = () => {
  return (
      <>
          <Header />
          <Routes>
              <Route path="/" element={<StartPage />} />
              <Route path="/simulate" element={<Home />} />
              <Route path="/parametrs" element={<Parameters />} />
          </Routes>
      </>
  );
};

export default App;