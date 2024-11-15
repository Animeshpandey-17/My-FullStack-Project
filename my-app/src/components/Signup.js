// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// import './Signup.css';

// const Signup = ({ onLogin }) => { // Accept onLogin as a prop
//   const navigate = useNavigate();
//   const [formData, setFormData] = useState({
//     username: '',
//     email: '',
//     password: '',
//     confirmPassword: '',
//   });

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setFormData({ ...formData, [name]: value });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     // Basic validation
//     if (formData.password !== formData.confirmPassword) {
//       alert("Passwords do not match!");
//       return;
//     }

//     try {
//       const response = await fetch('http://127.0.0.1:8000/api/signup/', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           username: formData.username,
//           email: formData.email,
//           password: formData.password,
//           confirm_password: formData.confirmPassword,
//         }),
//       });

//       if (response.ok) {
//         const data = await response.json();
//         console.log("Signup successful:", data);
        
//         // Call the onLogin function to update the authentication state
//         onLogin();
        
//         // Redirect to the dashboard
//         navigate('/dashboard');
//       } else {
//         const errorData = await response.json();
//         console.error("Signup error:", errorData);
//         alert(errorData.error || "Signup failed. Please try again.");
//       }
//     } catch (error) {
//       console.error("Error during signup:", error);
//       alert("An error occurred. Please try again later.");
//     }
//   };

//   return (
//     <div className="container mt-5">
//       <div className="signup-card">
//         <h1 className="text-center">Signup Page</h1>
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
//             <label htmlFor="email" className="col-sm-4 col-form-label">Email</label>
//             <div className="col-sm-8">
//               <input
//                 type="email"
//                 className="form-control"
//                 id="email"
//                 name="email"
//                 value={formData.email}
//                 onChange={handleChange}
//                 placeholder="Enter your email"
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
//             <label htmlFor="confirmPassword" className="col-sm-4 col-form-label">Confirm Password</label>
//             <div className="col-sm-8">
//               <input
//                 type="password"
//                 className="form-control"
//                 id="confirmPassword"
//                 name="confirmPassword"
//                 value={formData.confirmPassword}
//                 onChange={handleChange}
//                 placeholder="Confirm your password"
//                 required
//               />
//             </div>
//           </div>
//           <div className="row mb-3">
//             <div className="col-sm-10 offset-sm-2">
//               <button type="submit" className="btn btn-primary w-100">Signup</button>
//             </div>
//           </div>
//         </form>
//       </div>
//     </div>
//   );
// };

// export default Signup;


import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Signup.css';

const Signup = ({ onLogin }) => { // Accept onLogin as a prop
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // const handleSubmit = async (e) => {
  //   e.preventDefault();

  //   // Basic validation
  //   if (formData.password !== formData.confirmPassword) {
  //     alert("Passwords do not match!");
  //     return;
  //   }

  //   try {
  //     const response = await fetch('http://127.0.0.1:8000/api/signup/', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //       body: JSON.stringify({
  //         username: formData.username,
  //         email: formData.email,
  //         password: formData.password,
  //         confirm_password: formData.confirmPassword,
  //       }),
  //     });

  //     if (response.ok) {
  //       const data = await response.json();
  //       console.log("Signup successful:", data);
        
  //       // Save the token to localStorage (if you use token-based authentication)
  //       localStorage.setItem('token', data.token);

  //       // Call the onLogin function to update the authentication state
  //       onLogin();
        
  //       // Redirect to the dashboard after successful signup
  //       navigate('/dashboard');
  //     } else {
  //       const errorData = await response.json();
  //       console.error("Signup error:", errorData);
  //       alert(errorData.error || "Signup failed. Please try again.");
  //     }
  //   } catch (error) {
  //     console.error("Error during signup:", error);
  //     alert("An error occurred. Please try again later.");
  //   }
  // };



  const handleSubmit = async (e) => {
    e.preventDefault();
  
    // Basic validation
    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
  
    try {
      // Step 1: Sign up the user
      const signupResponse = await fetch('http://127.0.0.1:8000/api/signup/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password,
          confirm_password: formData.confirmPassword,
        }),
      });
  
      if (signupResponse.ok) {
        const signupData = await signupResponse.json();
        console.log("Signup successful:", signupData);
  
        // Step 2: Automatically log in the user to get the token
        const loginResponse = await fetch('http://127.0.0.1:8000/api/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: formData.username,
            password: formData.password,
          }),
        });
  
        if (loginResponse.ok) {
          const loginData = await loginResponse.json();
          console.log("Login successful:", loginData);
  
          // Save the token to localStorage
          localStorage.setItem('token', loginData.token);
  
          // Call the onLogin function to update the authentication state
          onLogin();
  
          // Redirect to the dashboard
          navigate('/dashboard');
        } else {
          const loginErrorData = await loginResponse.json();
          console.error("Login error:", loginErrorData);
          alert("Login failed after signup. Please try to log in manually.");
        }
      } else {
        const signupErrorData = await signupResponse.json();
        console.error("Signup error:", signupErrorData);
        alert(signupErrorData.error || "Signup failed. Please try again.");
      }
    } catch (error) {
      console.error("Error during signup/login:", error);
      alert("An error occurred. Please try again later.");
    }
  };
  

  return (
    <div className="container mt-5">
      <div className="signup-card">
        <h1 className="text-center">Signup Page</h1>
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
                placeholder="Enter your username"
                required
              />
            </div>
          </div>
          <div className="row mb-3">
            <label htmlFor="email" className="col-sm-4 col-form-label">Email</label>
            <div className="col-sm-8">
              <input
                type="email"
                className="form-control"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Enter your email"
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
                placeholder="Enter your password"
                required
              />
            </div>
          </div>
          <div className="row mb-3">
            <label htmlFor="confirmPassword" className="col-sm-4 col-form-label">Confirm Password</label>
            <div className="col-sm-8">
              <input
                type="password"
                className="form-control"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="Confirm your password"
                required
              />
            </div>
          </div>
          <div className="row mb-3">
            <div className="col-sm-10 offset-sm-2">
              <button type="submit" className="btn btn-primary w-100">Signup</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Signup;
