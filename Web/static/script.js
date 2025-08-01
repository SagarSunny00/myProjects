// Global Variables
let authToken = sessionStorage.getItem('authToken') || null;
let currentUserId = null;
let selectedClientId = null;
const API_BASE_URL = 'https://your-api-url.com'; // Replace with your actual API URL

// DOM Elements
const authSection = document.getElementById('authSection');
const loginForm = document.getElementById('loginForm');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const authError = document.getElementById('authError');
const dashboard = document.getElementById('dashboard');
const loginBtn = document.getElementById('loginBtn');
const logoutBtn = document.getElementById('logoutBtn');
const loggedInUserSpan = document.getElementById('loggedInUser');

const clientForm = document.getElementById('clientForm');
const clientNameInput = document.getElementById('clientName');
const clientError = document.getElementById('clientError');
const clientItemsList = document.getElementById('clientItems');

const selectedClientNameSpan = document.getElementById('selectedClientName');
const projectForm = document.getElementById('projectForm');
const projectNameInput = document.getElementById('projectName');
const projectUsersInput = document.getElementById('projectUsers');
const projectError = document.getElementById('projectError');
const clientProjectItemsList = document.getElementById('clientProjectItems');

const myProjectItemsList = document.getElementById('myProjectItems');

// --- Utility Functions ---
function showMessage(element, message, isError = true) {
    element.textContent = message;
    element.style.color = isError ? '#d9534f' : '#28a745';
    element.style.display = 'block';
    setTimeout(() => element.style.display = 'none', 5000);
}

function clearMessages() {
    authError.textContent = '';
    clientError.textContent = '';
    projectError.textContent = '';
}

function getAuthHeaders() {
    if (authToken) {
        return {
            'Content-Type': 'application/json',
            'Authorization': `Token ${authToken}`
        };
    }
    return { 'Content-Type': 'application/json' };
}

// --- Authentication ---
async function login(e) {
    e.preventDefault();
    clearMessages();

    const username = usernameInput.value;
    const password = passwordInput.value;

    try {
        const response = await fetch(`${API_BASE_URL}/api-token-auth/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(
                errorData.non_field_errors
                    ? errorData.non_field_errors[0]
                    : 'Login failed'
            );
        }

        const data = await response.json();
        authToken = data.token;
        sessionStorage.setItem('authToken', authToken);
        await fetchUserDetails(); // Fetch user details after login to get ID and username
        updateUIForAuth();
        loadAllClients();
        loadMyProjects();
    } catch (error) {
        showMessage(authError, error.message || 'An unexpected error occurred during login.');
    }
}

async function fetchUserDetails() {
    try {
        const response = await fetch(`${API_BASE_URL}/users/me/`, {
            headers: getAuthHeaders()
        });
        if (response.ok) {
            const user = await response.json();
            loggedInUserSpan.textContent = `Logged in as: ${user.username}`;
            currentUserId = user.id;
        } else {
            console.error("Failed to fetch user details:", response.status);
        }
    } catch (error) {
        console.error("Error fetching user details:", error);
    }
}

function logout() {
    authToken = null;
    sessionStorage.removeItem('authToken');
    currentUserId = null;
    updateUIForAuth();
    clientItemsList.innerHTML = '';
    clientProjectItemsList.innerHTML = '';
    myProjectItemsList.innerHTML = '';
    selectedClientId = null;
    selectedClientNameSpan.textContent = 'Select a client to view/add projects.';
    projectForm.style.display = 'none';
    usernameInput.value = '';
    passwordInput.value = '';
}

function updateUIForAuth() {
    if (authToken) {
        authSection.style.display = 'none';
        dashboard.style.display = 'block';
        loginBtn.style.display = 'none';
        logoutBtn.style.display = 'inline-block';
        loggedInUserSpan.style.display = 'inline-block';
        // Fetch user details immediately on UI update if token exists
        if (!loggedInUserSpan.textContent) { // Only fetch if not already set
            fetchUserDetails();
        }
    } else {
        authSection.style.display = 'block';
        dashboard.style.display = 'none';
        loginBtn.style.display = 'inline-block';
        logoutBtn.style.display = 'none';
        loggedInUserSpan.style.display = 'none';
        loggedInUserSpan.textContent = '';
    }
}

// --- Client Management ---
async function loadAllClients() {
    clearMessages();
    clientItemsList.innerHTML = '<li>Loading clients...</li>';
    try {
        const response = await fetch(`${API_BASE_URL}/clients/`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) {
            throw new Error(`Error fetching clients: ${response.statusText}`);
        }

        const clients = await response.json();
        renderClients(clients);
    } catch (error) {
        showMessage(clientError, error.message || 'Failed to load clients.');
        clientItemsList.innerHTML = '<li>Failed to load clients. Please log in.</li>';
    }
}

function renderClients(clients) {
    clientItemsList.innerHTML = '';
    if (clients.length === 0) {
        clientItemsList.innerHTML = '<li>No clients found.</li>';
        return;
    }
    clients.forEach(client => {
        const li = document.createElement('li');
        li.setAttribute('data-client-id', client.id);
        li.innerHTML = `
            <span><strong>ID:</strong> ${client.id}</span>
            <span><strong>Name:</strong> ${client.client_name}</span>
            <span><strong>Created By:</strong> ${client.created_by || 'N/A'}</span>
            <span><strong>Created At:</strong> ${new Date(client.created_at).toLocaleDateString()}</span>
            <div class="actions">
                <button class="view-btn" data-id="${client.id}">View Projects</button>
                <button class="edit-btn" data-id="${client.id}">Edit</button>
                <button class="delete-btn" data-id="${client.id}">Delete</button>
            </div>
        `;
        clientItemsList.appendChild(li);
    });
}

async function addClient(e) {
    e.preventDefault();
    clearMessages();
    const clientName = clientNameInput.value.trim();
    if (!clientName) {
        showMessage(clientError, 'Client name cannot be empty.');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/clients/`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ client_name: clientName })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.client_name ? errorData.client_name[0] : 'Failed to add client.');
        }

        clientNameInput.value = '';
        showMessage(clientError, 'Client added successfully!', false);
        loadAllClients(); // Reload clients to show new one
    } catch (error) {
        showMessage(clientError, error.message || 'An error occurred while adding client.');
    }
}

async function editClient(clientId, newName) {
    clearMessages();
    try {
        const response = await fetch(`${API_BASE_URL}/clients/${clientId}/`, {
            method: 'PUT', // Or PATCH for partial updates
            headers: getAuthHeaders(),
            body: JSON.stringify({ client_name: newName })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.client_name ? errorData.client_name[0] : 'Failed to update client.');
        }

        showMessage(clientError, 'Client updated successfully!', false);
        loadAllClients();
    } catch (error) {
        showMessage(clientError, error.message || 'An error occurred while updating client.');
    }
}

async function deleteClient(clientId) {
    clearMessages();
    if (!confirm('Are you sure you want to delete this client?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/clients/${clientId}/`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });

        if (response.status === 204) {
            showMessage(clientError, 'Client deleted successfully!', false);
            loadAllClients();
            // Clear selected client projects if the deleted client was selected
            if (selectedClientId === clientId) {
                selectedClientId = null;
                selectedClientNameSpan.textContent = 'Select a client to view/add projects.';
                projectForm.style.display = 'none';
                clientProjectItemsList.innerHTML = '';
            }
        } else {
            throw new Error(`Failed to delete client: ${response.statusText}`);
        }
    } catch (error) {
        showMessage(clientError, error.message || 'An error occurred while deleting client.');
    }
}

// --- Project Management for a Specific Client ---
async function loadClientDetailsAndProjects(clientId) {
    clearMessages();
    clientProjectItemsList.innerHTML = '<li>Loading projects...</li>';
    selectedClientNameSpan.textContent = 'Loading client details...';
    projectForm.style.display = 'none'; // Hide form while loading

    try {
        const response = await fetch(`${API_BASE_URL}/clients/${clientId}/`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) {
            throw new Error(`Error fetching client projects: ${response.statusText}`);
        }

        const clientData = await response.json();
        selectedClientId = clientData.id;
        selectedClientNameSpan.textContent = `Projects for: ${clientData.client_name}`;
        projectForm.style.display = 'flex'; // Show project form

        renderClientProjects(clientData.projects);
    } catch (error) {
        showMessage(projectError, error.message || 'Failed to load client projects.');
        clientProjectItemsList.innerHTML = '<li>Failed to load projects.</li>';
        selectedClientNameSpan.textContent = 'Error loading client details.';
        projectForm.style.display = 'none';
    }
}

function renderClientProjects(projects) {
    clientProjectItemsList.innerHTML = '';
    if (projects.length === 0) {
        clientProjectItemsList.innerHTML = '<li>No projects found for this client.</li>';
        return;
    }
    projects.forEach(project => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span><strong>ID:</strong> ${project.id}</span>
            <span><strong>Name:</strong> ${project.name}</span>
            <!-- Add more project details if available in the /clients/:id response -->
        `;
        clientProjectItemsList.appendChild(li);
    });
}

async function addProjectToClient(e) {
    e.preventDefault();
    clearMessages();
    if (!selectedClientId) {
        showMessage(projectError, 'Please select a client first.');
        return;
    }

    const projectName = projectNameInput.value.trim();
    if (!projectName) {
        showMessage(projectError, 'Project name cannot be empty.');
        return;
    }

    const usersInput = projectUsersInput.value.trim();
    let users = [];
    if (usersInput) {
        try {
            // Parse comma-separated IDs into an array of objects
            users = usersInput.split(',').map(id => ({ id: parseInt(id.trim()) }));
            if (users.some(user => isNaN(user.id))) {
                throw new Error('Invalid user ID format. Use comma-separated numbers.');
            }
        } catch (error) {
            showMessage(projectError, error.message);
            return;
        }
    }

    try {
        const response = await fetch(`${API_BASE_URL}/clients/${selectedClientId}/projects/`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({
                project_name: projectName, // Matches serializer field
                users: users
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            // Check for specific error messages from DRF
            const errorMessage = errorData.project_name ? errorData.project_name[0] :
                                 errorData.users ? errorData.users[0].id[0] : // For user ID validation errors
                                 JSON.stringify(errorData); // Fallback for general errors
            throw new Error(`Failed to add project: ${errorMessage}`);
        }

        projectNameInput.value = '';
        projectUsersInput.value = '';
        showMessage(projectError, 'Project added successfully!', false);
        loadClientDetailsAndProjects(selectedClientId); // Reload projects for this client
        loadMyProjects(); // Also reload my projects as new project might be assigned to me
    } catch (error) {
        showMessage(projectError, error.message || 'An error occurred while adding project.');
    }
}

// --- My Assigned Projects ---
async function loadMyProjects() {
    clearMessages();
    myProjectItemsList.innerHTML = '<li>Loading your projects...</li>';
    try {
        const response = await fetch(`${API_BASE_URL}/projects/`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) {
            throw new Error(`Error fetching your projects: ${response.statusText}`);
        }

        const projects = await response.json();
        renderMyProjects(projects);
    } catch (error) {
        showMessage(projectError, error.message || 'Failed to load your projects.');
        myProjectItemsList.innerHTML = '<li>Failed to load your projects. Please log in.</li>';
    }
}

function renderMyProjects(projects) {
    myProjectItemsList.innerHTML = '';
    if (projects.length === 0) {
        myProjectItemsList.innerHTML = '<li>No projects assigned to you.</li>';
        return;
    }
    projects.forEach(project => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span><strong>ID:</strong> ${project.id}</span>
            <span><strong>Project Name:</strong> ${project.project_name}</span>
            <span><strong>Client:</strong> ${project.client || 'N/A'}</span>
            <span><strong>Created By:</strong> ${project.created_by || 'N/A'}</span>
            <span><strong>Created At:</strong> ${new Date(project.created_at).toLocaleDateString()}</span>
        `;
        myProjectItemsList.appendChild(li);
    });
}

// --- Event Listeners ---
loginForm.addEventListener('submit', login);
logoutBtn.addEventListener('click', logout);
loginBtn.addEventListener('click', () => { // If login button is visible, show login form
    authSection.style.display = 'block';
    dashboard.style.display = 'none';
});

clientForm.addEventListener('submit', addClient);
projectForm.addEventListener('submit', addProjectToClient);

clientItemsList.addEventListener('click', (e) => {
    const clientId = e.target.dataset.id;
    if (clientId) {
        if (e.target.classList.contains('view-btn')) {
            loadClientDetailsAndProjects(clientId);
        } else if (e.target.classList.contains('edit-btn')) {
            const newName = prompt('Enter new client name:', e.target.closest('li').querySelector('span:nth-child(2)').textContent.replace('Name: ', ''));
            if (newName) {
                editClient(clientId, newName);
            }
        } else if (e.target.classList.contains('delete-btn')) {
            deleteClient(clientId);
        }
    }
});

// --- Initial Load ---
updateUIForAuth(); // Check for existing token on page load
if (authToken) {
    loadAllClients();
    loadMyProjects();
}