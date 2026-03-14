<template>
  <div class="relative">
    <LoadingOverlay :visible="loading" :messages="submitMessages" />
    <LoadingOverlay :visible="importing" :messages="importMessages" />

    <form @submit.prevent="submitForm" class="max-w-4xl mx-auto mt-10 p-8 bg-white rounded-2xl shadow-md border border-stone-200">
      <!-- Import from URL -->
      <div class="mb-6">
        <button
          type="button"
          @click="showUrlImport = !showUrlImport"
          class="flex items-center gap-2 text-sm font-semibold text-teal-600 hover:text-teal-700 transition-colors duration-200"
        >
          <span class="text-lg">{{ showUrlImport ? '−' : '+' }}</span>
          Import from URL
        </button>
        <Transition name="fade">
          <div v-if="showUrlImport" class="mt-3">
            <div class="flex gap-2">
              <input
                v-model="importUrl"
                type="url"
                class="flex-1 px-3 py-2 border rounded"
                placeholder="Paste job posting URL..."
              />
              <button
                type="button"
                :disabled="!importUrl || importing || isLinkedInUrl"
                @click="handleImport"
                class="px-4 py-2 bg-teal-600 hover:bg-teal-700 disabled:opacity-50 text-white font-semibold rounded-lg transition-colors duration-200"
              >
                Import
              </button>
            </div>
            <p v-if="isLinkedInUrl" class="mt-1.5 text-sm text-red-500">We do not support LinkedIn URLs</p>
          </div>
        </Transition>
      </div>

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
      <button type="submit" :disabled="loading" class="w-full bg-teal-600 hover:bg-teal-700 disabled:opacity-50 text-white font-semibold py-2.5 px-4 rounded-lg transition-colors duration-200">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { createJob, importJobFromUrl } from '@/api/api.js'
import { useRouter } from 'vue-router'
import LoadingOverlay from '@/components/loading-overlay.vue'

const title = ref('')
const description = ref('')
const salary = ref(null)
const link = ref('')
const router = useRouter()
const loading = ref(false)

const showUrlImport = ref(false)
const importUrl = ref('')
const importing = ref(false)
const isLinkedInUrl = computed(() => importUrl.value.includes('linkedin.com'))

const submitMessages = [
  'Parsing job description...',
  'Extracting required skills...',
  'Analysing the role...',
  'Almost there...',
]

const importMessages = [
  'Fetching job posting...',
  'Extracting details...',
  'Almost there...',
]

async function handleImport() {
  importing.value = true
  try {
    const response = await importJobFromUrl(importUrl.value)
    title.value = response.title || ''
    description.value = response.description || ''
    salary.value = response.salary || null
    link.value = importUrl.value
  } catch (err) {
    console.log(err)
  } finally {
    importing.value = false
  }
}

async function submitForm() {
  loading.value = true
  try {
    const response = await createJob({
      rawTitle: title.value,
      rawDescription: description.value,
      jobSalary: salary.value,
      link: link.value
    })
    console.log(response)
    router.push('/jobs-list')
  } catch (err) {
    console.log(err)
  } finally {
    loading.value = false
  }
}
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
