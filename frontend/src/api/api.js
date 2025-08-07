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