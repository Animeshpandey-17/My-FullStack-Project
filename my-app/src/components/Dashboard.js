import React, { useState, useEffect } from 'react';

const Dashboard = () => {
  // States to hold the fetched data, loading state, and error state
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Get the token from localStorage to pass in the request header for authorization
    const token = localStorage.getItem('token');
    
    if (token) {
      // Make the API request to fetch user data
      fetch('http://127.0.0.1:8000/api/fetch-data/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,  // Include the token for authentication
        },
      })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          setError(data.error);
        } else {
          setUserData(data);  // Save fetched user data to state
        }
      })
      .catch(err => {
        setError('An error occurred while fetching data.');
      })
      .finally(() => {
        setLoading(false);  // Stop loading after the request completes
      });
    } else {
      setError('No token found. Please log in.');
      setLoading(false);
    }
  }, []);

  return (
    <div className="container mt-5">
      <h1>Welcome to the Dashboard!</h1>
      <p>This is your dashboard where you can manage your settings and view your profile.</p>

      {loading && <p>Loading...</p>} {/* Show loading message while fetching data */}
      {error && <p style={{ color: 'red' }}>{error}</p>} {/* Show error message if there's an issue */}
      
      {userData && (
        <div>
          <h3>User Profile</h3>
          <ul>
            <li><strong>Username:</strong> {userData.username}</li>
            <li><strong>Email:</strong> {userData.email}</li>
            <li><strong>First Name:</strong> {userData.first_name}</li>
            <li><strong>Last Name:</strong> {userData.last_name}</li>
            {/* Add more fields as per the data structure from the backend */}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
