// authService.ts for handling internaluser loginning in, logging out and etc.

export const handleInternalUserLogin = async (username: string, password: string) => {
    // Your login logic here...
};

export const handleInternalUserLogout = async () => {
    // Your logout logic here...
    try {
        // Call the backend API to log out
        const response = await fetch('/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Add any authentication headers if required
            },
        });

        if (response.ok) {
            // Once logged out, clear any local storage or state 
            // For example, clear the user's data from local storage:
            localStorage.removeItem('username');
            localStorage.removeItem('expiry');

            // Redirect to the login page or homepage
            window.location.href = '/';
        } else {
            console.error('Failed to log out');
        }
    } catch (error) {
        console.error('There was an error logging out', error);
    }
};

