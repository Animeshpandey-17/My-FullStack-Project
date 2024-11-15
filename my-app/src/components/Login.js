// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// import './Login.css';

// const Login = ({ onLogin }) => { // Accept onLogin as a prop
//   const navigate = useNavigate();
//   const [formData, setFormData] = useState({
//     username: '',
//     password: '',
//   });

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setFormData({ ...formData, [name]: value });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
    
//     try {
//       const response = await fetch('http://127.0.0.1:8000/api/login/', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           username: formData.username,
//           password: formData.password,
//         }),
//       });

//       if (response.ok) {
//         const data = await response.json();
//         console.log("Login successful:", data);
        
//         // Example: Save the token to local storage if needed
//         // localStorage.setItem('token', data.token);
//         localStorage.setItem('token', data.token);

//         // Call the onLogin function to update the authentication state
//         onLogin();

//         // Redirect to the dashboard after successful login
//         navigate('/dashboard');
//       } else {
//         const errorData = await response.json();
//         console.error("Login error:", errorData);
//         alert(errorData.error || "Login failed. Please try again.");
//       }
//     } catch (error) {
//       console.error("Error during login:", error);
//       alert("An error occurred. Please try again later.");
//     }
//   };

//   return (
//     <div className="container mt-5">
//       <div className="login-card">
//         <h1 className="text-center">Login Page</h1>
//         <form onSubmit={handleSubmit}>
//           <div className="row mb-3">
//             <label htmlFor="username" className="col-sm-4 col-form-label">Username</label>
//             <div className="col-sm-8">
//               <input
//                 type="text"
//                 className="form-control"
//                 id="username"
//                 name="username"
//                 value={formData.username}
//                 onChange={handleChange}
//                 placeholder="Enter your username"
//                 required
//               />
//             </div>
//           </div>
//           <div className="row mb-3">
//             <label htmlFor="password" className="col-sm-4 col-form-label">Password</label>
//             <div className="col-sm-8">
//               <input
//                 type="password"
//                 className="form-control"
//                 id="password"
//                 name="password"
//                 value={formData.password}
//                 onChange={handleChange}
//                 placeholder="Enter your password"
//                 required
//               />
//             </div>
//           </div>
//           <div className="row mb-3">
//             <div className="col-sm-10 offset-sm-2">
//               <button type="submit" className="btn btn-primary w-100">Login</button>
//             </div>
//           </div>
//         </form>
//       </div>
//     </div>
//   );
// };

// export default Login;



import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Login.css';

const Login = ({ onLogin }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Login successful:", data);
        localStorage.setItem('token', data.token);
        onLogin();
        navigate('/dashboard');
      } else {
        const errorData = await response.json();
        alert(errorData.error || "Login failed. Please try again.");
      }
    } catch (error) {
      alert("An error occurred. Please try again later.");
    }
  };

  return (
    <div className="container mt-5">
      <div className="login-card">
        <h1 className="text-center">Login Page</h1>
        <form onSubmit={handleSubmit}>
          <div className="row mb-3">
            <label htmlFor="username" className="col-sm-4 col-form-label">Username</label>
            <div className="col-sm-8">
              <input
                type="text"
                className="form-control"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
              />
            </div>
          </div>
          <div className="row mb-3">
            <label htmlFor="password" className="col-sm-4 col-form-label">Password</label>
            <div className="col-sm-8">
              <input
                type="password"
                className="form-control"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>
          </div>
          <button type="submit" className="btn btn-primary w-100">Login</button>
          <div className="text-center mt-3">
            <Link to="/forgot-password">Forgot Password?</Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
