import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import PrivateRoute from "./routes/PrivateRoute";
import Layout from "./components/Layout";

import Login from "./pages/Login/Login";
import Dashboard from "./pages/Dashboard/Dashboard";
import Employees from "./pages/Employees/Employees";
import Departments from "./pages/Departments/Departments";
import Attendance from "./pages/Attendance/Attendance";
import Leaves from "./pages/Leaves/Leaves";

function Protected({ children }) {
  return (
    <PrivateRoute>
      <Layout>{children}</Layout>
    </PrivateRoute>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Protected><Dashboard /></Protected>} />
          <Route path="/employees" element={<Protected><Employees /></Protected>} />
          <Route path="/departments" element={<Protected><Departments /></Protected>} />
          <Route path="/attendance" element={<Protected><Attendance /></Protected>} />
          <Route path="/leaves" element={<Protected><Leaves /></Protected>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
