// import React from 'react';
// import { Link } from 'react-router-dom';
// import './Navbar.css';

// const Navbar = ({ isAuthenticated, onLogout }) => {
//   return (
//     <nav className="navbar navbar-expand-lg ">
//       <div className="container-fluid">
//         <Link className="navbar-brand" to="/">MyApp</Link>
//         <button
//           className="navbar-toggler"
//           type="button"
//           data-bs-toggle="collapse"
//           data-bs-target="#navbarNav"
//           aria-controls="navbarNav"
//           aria-expanded="false"
//           aria-label="Toggle navigation"
//         >
//           <span className="navbar-toggler-icon"></span>
//         </button>
//         <div className="collapse navbar-collapse" id="navbarNav">
//           <div className="navbar-left me-auto">
//             <Link className="nav-link" to="/">Home</Link>
//             <Link className="nav-link" to="/about">About Us</Link>
//             <Link className="nav-link" to="/benefits">Benefits</Link>
//           </div>
//           <div className="navbar-right">
//             {isAuthenticated ? (
//               <>
//                 <Link className="nav-link" to="/dashboard">Dashboard</Link>
//                 <button className="btn nav-link" onClick={onLogout}>Logout</button>
//               </>
//             ) : (
//               <>
//                 <Link className="nav-link" to="/signup">Signup</Link>
//                 <Link className="nav-link" to="/login">Login</Link>
//               </>
//             )}
//           </div>
//         </div>
//       </div>
//     </nav>
//   );
// };

// export default Navbar;


import React from 'react';
import { Link, useNavigate } from 'react-router-dom'; // useNavigate for redirect
import axios from 'axios';  // axios for API calls
import './Navbar.css';

const Navbar = ({ isAuthenticated, onLogout }) => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      // Get the token from localStorage
      const token = localStorage.getItem('token');
      
      if (token) {
        // Make the logout API call
        const response = await axios.post('http://127.0.0.1:8000/api/logout/', {}, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.status === 200) {
          // On success, clear the token from localStorage
          localStorage.removeItem('token');
          // Update authentication state
          onLogout();
          // Redirect to the Home page
          navigate('/');
        }
      }
    } catch (error) {
      console.error("Logout error:", error);
      alert('Error during logout. Please try again.');
    }
  };

  return (
    <nav className="navbar navbar-expand-lg">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">MyApp</Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <div className="navbar-left me-auto">
            <Link className="nav-link" to="/">Home</Link>
            <Link className="nav-link" to="/about">About Us</Link>
            <Link className="nav-link" to="/benefits">Benefits</Link>
          </div>
          <div className="navbar-right">
            {isAuthenticated ? (
              <>
                <Link className="nav-link" to="/dashboard">Dashboard</Link>
                <button className="btn nav-link" onClick={handleLogout}>Logout</button>
              </>
            ) : (
              <>
                <Link className="nav-link" to="/signup">Signup</Link>
                <Link className="nav-link" to="/login">Login</Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
