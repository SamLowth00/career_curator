<template>
  <div class="flex flex-col h-[calc(100vh-73px)] bg-stone-50">
    <!-- Header -->
    <div class="bg-white border-b border-stone-200 px-6 py-4 flex items-center gap-3">
      <div class="w-9 h-9 rounded-full bg-teal-600 flex items-center justify-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
      </div>
      <div>
        <h2 class="text-lg font-semibold text-gray-800">Career Agent</h2>
        <p class="text-xs text-gray-500">Powered by GPT-4</p>
      </div>
    </div>

    <!-- Messages -->
    <div ref="messagesEl" class="flex-1 overflow-y-auto px-6 py-6 space-y-4">
      <!-- Empty state -->
      <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-full text-center gap-3 text-gray-400">
        <div class="w-16 h-16 rounded-full bg-teal-50 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-teal-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </div>
        <div>
          <p class="font-medium text-gray-500">Ask me anything about your career</p>
          <p class="text-sm mt-1">Interview prep, skill gaps, job strategies and more.</p>
        </div>
      </div>

      <!-- Message bubbles -->
      <div
        v-for="m in messages"
        :key="m.id"
        class="flex"
        :class="m.role === 'user' ? 'justify-end' : 'justify-start'"
      >
        <!-- Assistant avatar -->
        <div v-if="m.role !== 'user'" class="w-7 h-7 rounded-full bg-teal-600 flex items-center justify-center flex-shrink-0 mr-2 mt-1">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>

        <div
          class="max-w-[70%] px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap"
          :class="m.role === 'user'
            ? 'bg-teal-600 text-white rounded-br-sm'
            : 'bg-white text-gray-800 border border-stone-200 rounded-bl-sm shadow-sm'"
        >
          {{ m.content }}
        </div>
      </div>

      <!-- Typing indicator -->
      <div v-if="loading" class="flex justify-start">
        <div class="w-7 h-7 rounded-full bg-teal-600 flex items-center justify-center flex-shrink-0 mr-2 mt-1">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <div class="bg-white border border-stone-200 rounded-2xl rounded-bl-sm shadow-sm px-4 py-3 flex items-center gap-1">
          <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
          <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
          <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
        </div>
      </div>
    </div>

    <!-- Input area -->
    <div class="bg-white border-t border-stone-200 px-6 py-4">
      <form @submit.prevent="onSend" class="flex items-end gap-3">
        <textarea
          v-model="text"
          :disabled="loading"
          @keydown.enter.exact.prevent="onSend"
          placeholder="Ask about your career..."
          rows="1"
          class="flex-1 resize-none rounded-xl border border-stone-300 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent disabled:bg-stone-50 disabled:text-stone-400 transition"
          style="max-height: 140px; overflow-y: auto;"
          @input="autoResize"
          ref="textareaEl"
        />
        <button
          :disabled="loading || !text.trim()"
          class="flex-shrink-0 w-10 h-10 rounded-xl bg-teal-600 text-white flex items-center justify-center hover:bg-teal-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </form>
      <p class="text-xs text-gray-400 mt-2">Press Enter to send · Shift+Enter for new line</p>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onBeforeUnmount } from 'vue'
import { agentChat, clearAgent } from '@/api/api'
import { v4 as uuidv4 } from 'uuid';

const messages = ref([])
const text = ref('')
const loading = ref(false)
const messagesEl = ref(null)
const textareaEl = ref(null)

function autoResize() {
  const el = textareaEl.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = Math.min(el.scrollHeight, 140) + 'px'
}

function scrollToBottom() {
  if (messagesEl.value) {
    messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  }
}

async function onSend() {
  const content = text.value.trim()
  if (!content || loading.value) return

  const tempId = uuidv4()
  messages.value.push({ id: tempId, role: 'user', content })
  text.value = ''
  loading.value = true
  await nextTick()
  scrollToBottom()
  if (textareaEl.value) {
    textareaEl.value.style.height = 'auto'
  }

  try {
    const res = await agentChat({ message: content })
    messages.value = (res.conversation_history || []).map(message => ({
      id: uuidv4(),
      role: message.role,
      content: message.content
    }))
  } catch (e) {
    console.log(e)
  } finally {
    loading.value = false
    await nextTick()
    scrollToBottom()
  }
}

const clearChat = async () => {
  await clearAgent()
}

onMounted(() => {
  window.addEventListener('beforeunload', clearChat)
})

onBeforeUnmount(() => {
  clearAgent()
  window.removeEventListener('beforeunload', clearChat)
})
</script>
