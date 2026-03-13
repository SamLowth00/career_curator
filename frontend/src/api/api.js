import axiosApi from "@/axios-setup";

export async function login(username, password) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    const response = await axiosApi.post('/auth/jwt/login', params, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    return response.data;
}

export async function getCurrentUser() {
    const response = await axiosApi.get('/users/me');
    return response.data;
}

export async function importJobFromUrl(url) {
    const response = await axiosApi.post('/jobs/import', { url }, {
        headers: { 'Content-Type': 'application/json' }
    });
    return response.data;
}

export async function createJob({rawTitle, rawDescription, jobSalary, link}) {
    const payload = {
        raw_title: rawTitle,
        raw_description: rawDescription,
        ...(jobSalary ? {job_salary: jobSalary}: {}),
        ...(link ? { link } : {})
    }

    const response = await axiosApi.post('/jobs', payload, { headers: {
        'Content-Type': 'application/json'
    }});
    
    return response.data;
}
export async function getJobs() {
    const response = await axiosApi.get('/jobs');
    return response.data;
}

export async function deleteJob({id}) {
    const response = await axiosApi.delete(`/jobs/${id}`)
    return response.data
}

export async function generatePlan () {
    const response = await axiosApi.post('/plan/generate-plan');
    return response.data
}

export async function getSkills() {
    const response = await axiosApi.get('/skill/list');
    return response.data
}

export async function getAverageSalary() {
    const response = await axiosApi.get('/salary/average')
    return response.data
}

export async function agentChat (payload) {
    const response = await axiosApi.post('/chat/chat', payload, { headers: {
        'Content-Type': 'application/json'
    }});
    return response.data
} 

export async function clearAgent() {
    const response = await axiosApi.post('/chat/clear');
    return response.data
}

export async function getSavedPlan() {
    const response = await axiosApi.get('/plan/saved-plan');
    return response.data;  // will be the markdown string, or null
}

export async function getUserSkills() {
    const response = await axiosApi.get('/user-skills/');
    return response.data;
}

export async function createUserSkill({ name, description, level }) {
    const response = await axiosApi.post('/user-skills/', { name, description, level });
    return response.data;
}

export async function updateUserSkill(id, { name, description, level }) {
    const response = await axiosApi.put(`/user-skills/${id}`, { name, description, level });
    return response.data;
}

export async function deleteUserSkill(id) {
    const response = await axiosApi.delete(`/user-skills/${id}`);
    return response.data;
}
