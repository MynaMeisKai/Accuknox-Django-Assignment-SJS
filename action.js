
// URLs
const baseURL = "http://127.0.0.1:8000/api/";

const loginURL = `${baseURL}login/`;
const signupURL = `${baseURL}signup/`;
const searchURL = `${baseURL}search/`;
const requestURL = `${baseURL}friend-requests/`;
const requestPendingURL = `${baseURL}friend-requests/pending/`;

let authToken ; 

// Function to login and retrieve token
async function login(username, password) {
    const response = await fetch(loginURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    if (response.ok) {
        const data = await response.json();
        authToken = data.token; // Save token for future requests
        console.log('Login successful. Token:', authToken);
    } else {
        console.error('Login failed:', response.statusText);
    }
}

// Function to sign up a new user
async function signup(username, email, password) {
    const response = await fetch(signupURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, email, password })
    });

    if (response.ok) {
        const data = await response.json();
        console.log('Signup successful:', data);
    } else {
        console.error('Signup failed:', response.statusText);
    }
}

// Function to search users
async function searchUsers(keyword) {
    const response = await fetch(`${searchURL}?q=${encodeURIComponent(keyword)}`, {
        method: 'GET',
        headers: {
            'Authorization': `Token ${authToken}`
        }
    });

    if (response.ok) {
        const data = await response.json();
        console.log('Search results:', data);
    } else {
        console.error('Search failed:', response.statusText);
    }
}

// Function to send a friend request
async function sendFriendRequest(userId) {
    const response = await fetch(requestURL, {
        method: 'POST',
        headers: {
            'Authorization': `Token ${authToken}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: userId })
    });

    if (response.ok) {
        const data = await response.json();
        console.log('Friend request sent:', data);
    } else {
        console.error('Failed to send friend request:', response.statusText);
    }
}

// Function to get pending friend requests
async function getPendingRequests() {
    const response = await fetch(requestPendingURL, {
        method: 'GET',
        headers: {
            'Authorization': `Tok ${authToken}`
        }
    });

    if (response.ok) {
        const data = await response.json();
        console.log('Pending friend requests:', data);
    } else {
        console.error('Failed to get pending friend requests:', response.statusText);
    }
}

// Example usage
(async () => {
    await login('your-username', 'your-password');  // Replace with actual credentials
    await searchUsers('John Doe');
    await sendFriendRequest(123); // Replace with actual user ID
    await getPendingRequests();
})();
