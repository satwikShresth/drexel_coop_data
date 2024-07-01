import './App.css'

import NavBar from "./components/navbar";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Table from './components/table';
import './App.css';

export default function App() {
   return (
      <div>
         <Router>
            <NavBar />
            <div className="container mx-auto p-4 pt-16">
               <Routes>
                  <Route path="/" element={<Table />} />
               </Routes>
            </div>
         </Router>
      </div>
   );
};
