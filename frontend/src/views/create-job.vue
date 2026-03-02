<template>
  <div class="relative">
    <!-- Loading overlay -->
    <Transition name="fade">
      <div v-if="loading" class="fixed inset-0 z-50 flex flex-col items-center justify-center bg-white/80 backdrop-blur-sm">
        <div class="flex flex-col items-center gap-6">
          <!-- Animated ring -->
          <div class="relative w-16 h-16">
            <div class="absolute inset-0 rounded-full border-4 border-teal-100"></div>
            <div class="absolute inset-0 rounded-full border-4 border-t-teal-600 animate-spin"></div>
          </div>
          <!-- Cycling message -->
          <div class="text-center">
            <p class="text-lg font-semibold text-gray-800">{{ currentMessage }}</p>
            <div class="flex justify-center gap-1 mt-2">
              <span v-for="i in 3" :key="i" class="w-1.5 h-1.5 rounded-full bg-teal-500 animate-bounce" :style="{ animationDelay: `${(i - 1) * 0.15}s` }"></span>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <form @submit.prevent="submitForm" class="max-w-4xl mx-auto mt-10 p-8 bg-white rounded-2xl shadow-md border border-stone-200">
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
import { ref } from 'vue'
import { createJob } from '@/api/api.js'
import { useRouter } from 'vue-router'

const title = ref('')
const description = ref('')
const salary = ref(null)
const link = ref('')
const router = useRouter()
const loading = ref(false)

const messages = [
  'Parsing job description...',
  'Extracting required skills...',
  'Analysing the role...',
  'Almost there...',
]
const currentMessage = ref(messages[0])
let messageInterval = null

function startMessages() {
  let i = 0
  messageInterval = setInterval(() => {
    i = (i + 1) % messages.length
    currentMessage.value = messages[i]
  }, 2000)
}

function stopMessages() {
  clearInterval(messageInterval)
  currentMessage.value = messages[0]
}

async function submitForm() {
  loading.value = true
  startMessages()
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
    stopMessages()
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
