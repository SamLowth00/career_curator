<template>
  <form @submit.prevent="submitForm" class="max-w-md mx-auto p-4 bg-white rounded shadow">
    <div class="mb-4">
      <label for="title" class="block text-gray-700 font-bold mb-2">Job Title<span class="text-red-500">*</span></label>
      <input
        id="title"
        v-model="title"
        type="text"
        required
        class="w-full px-3 py-2 border rounded"
        placeholder="Enter job title"
      />
    </div>
    <div class="mb-4">
      <label for="description" class="block text-gray-700 font-bold mb-2">Job Description<span class="text-red-500">*</span></label>
      <textarea
        id="description"
        v-model="description"
        required
        class="w-full px-3 py-2 border rounded"
        placeholder="Enter job description"
        rows="5"
      ></textarea>
    </div>
    <div class="mb-4">
      <label for="salary" class="block text-gray-700 font-bold mb-2">Salary</label>
      <input
        id="salary"
        v-model.number="salary"
        type="number"
        min="0"
        class="w-full px-3 py-2 border rounded"
        placeholder="Enter salary (optional)"
      />
    </div>
    <div class="mb-4">
      <label for="link" class="block text-gray-700 font-bold mb-2">Link</label>
      <input
        id="link"
        v-model="link"
        type="url"
        class="w-full px-3 py-2 border rounded"
        placeholder="Enter job link (optional)"
      />
    </div>
    <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">Submit</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { createJob } from '@/api/api.js'
const title = ref('')
const description = ref('')
const salary = ref(null)
const link = ref('')

async function submitForm() {
  // For now, just log the form data
  console.log({
    title: title.value,
    description: description.value,
    salary: salary.value,
    link: link.value,
  })

  const response = await createJob({
    rawTitle: title.value,
    rawDescription: description.value,
    jobSalary: salary.value,
    link: link.value
  })
  console.log(response);

}
</script>

<style>
/* Optional: Add some margin to the form for better appearance */
</style>