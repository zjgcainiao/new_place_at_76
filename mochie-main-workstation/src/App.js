import {
  createBrowserRouter,
  RouterProvider,
  // Route,
  // Routes,
  Link,
} from 'react-router-dom'
import { useEffect, useState } from "react";
// import logo from './logo-2022.svg';
import './App.css';
import Header from './components/Header'
import NavBar from './components/Navbar';

import CustomerListPage from './pages/CustomerListPage';
import CustomerDetailPage from './pages/CustomerDetailPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <CustomerListPage />
  },
  {
    path: '/cust_detail/:customerName',
    loader: ({params}) =>{
      console.log ('Router: the customer name is ', params.customerName)
      return params.customerName.toString
    },
    // errorElement: ,
    element: <CustomerDetailPage  />
  },

]);
// const App = () =>{}
function App() {
  return ( 
        <div className="App">
          <Header />
          <RouterProvider router={router} />
 {/* 32         
          <Route exact path ='/'  element = {<CustomerListPage />} />
          <Route path ='/cust_detail/:customerName' element ={<CustomerDetailPage />} /> */}
          
        </div>

 
  );
}

export default App;
