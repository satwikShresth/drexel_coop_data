import './App.css'

import NavBar from "./components/navbar";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CoopForm from './page/coopform';
import Table from './page/table';
import './App.css';

export default function App() {
   const links = [
      { to: '/form/salary', label: 'Salary Form' }
   ]
   return (
      <div>
         <Router>
            <NavBar links={links} />
            <div className="container mx-auto p-4 pt-16">
               <Routes>
                  <Route path="/" element={<Table />} />
                  <Route path="/form/salary" element={<CoopForm />} />
               </Routes>
            </div>
         </Router>
      </div>
   );
};
