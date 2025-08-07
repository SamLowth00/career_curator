<template>
  <div class="p-6">
    <div v-if="loading" class="flex justify-center items-center h-40">
      <span class="text-blue-600 text-lg font-semibold">Loading jobs...</span>
    </div>
    <div v-else>
      <table class="min-w-full bg-white border border-gray-200 rounded-lg shadow">
        <thead>
          <tr class="bg-blue-100 text-left">
            <th class="py-2 px-4 border-b">Job Title</th>
            <th class="py-2 px-4 border-b">Job Summary</th>
            <th class="py-2 px-4 border-b">Job Description</th>
            <th class="py-2 px-4 border-b">Job Salary</th>
            <th class="py-2 px-4 border-b">Job Link</th>
            <th class="py-2 px-4 border-b">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in jobs" :key="job.id" class="hover:bg-blue-50">
            <td class="py-2 px-4 border-b">{{ job.title }}</td>
            <td class="py-2 px-4 border-b"><span class="line-clamp-6">{{ job.summary }}</span></td>
            <td class="py-2 px-4 border-b"><span class="line-clamp-6 h-[100%]">{{ job.description }}</span></td>
            <td class="py-2 px-4 border-b">{{ job.salary }}</td>
            <td class="py-2 px-4 border-b">
              <a :href="job.link" target="_blank" class="text-blue-600 underline">View</a>
            </td>
            <td class="py-2 px-4 border-b text-center" >
              <button @click="handleDelete(job.id)" class="text-red-500 hover:text-red-700 cursor-pointer" title="Delete">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </td>
          </tr>
          <tr v-if="jobs.length === 0">
            <td colspan="6" class="text-center py-4 text-gray-500">No jobs found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getJobs, deleteJob } from '@/api/api';
const jobs = ref([]);
const loading = ref(true);

async function fetchJobs() {
  loading.value = true;
  try {
    const response = await getJobs();
    console.log(response);
    jobs.value = response.map(({id,raw_title, job_summary, raw_description, job_salary, link}) => {
        return {
            id: id,
            title: raw_title,
            summary: job_summary,
            description: raw_description,
            salary: job_salary,
            link: link
        }
    })
  } catch (error) {
    console.error(error);
    jobs.value = [];
  } finally {
    loading.value = false;
  }
}

async function handleDelete(id) {
    await deleteJob({id});
    jobs.value = jobs.value.filter(job => job.id !== id);

}

onMounted(fetchJobs);
</script>