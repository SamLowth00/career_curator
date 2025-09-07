<template>
  <div class="chat">
    <div class="messages">
      <div v-for="m in messages" :key="m.id">
        <strong>{{ m.role }}:</strong> {{ m.content }}
      </div>
    </div>

    <form @submit.prevent="onSend">
      <input v-model="text" :disabled="loading" placeholder="Type a message..." />
      <button :disabled="loading || !text.trim()">Send</button>
    </form>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onBeforeUnmount } from 'vue'
import { agentChat, clearAgent } from '@/api/api'
import { v4 as uuidv4 } from 'uuid';
const messages = ref([]) // full history shown
const text = ref('')
const loading = ref(false)

async function onSend() {
  const content = text.value.trim()
  if (!content) return

  // optimistic local append for responsiveness
  const tempId = uuidv4();
  messages.value.push({ id: tempId, role: 'user', content })
  text.value = ''
  loading.value = true

  try {
    const res = await agentChat({message: content});

    messages.value = (res.conversation_history || []).map(message => {
      const id = uuidv4()
      return {
        id: id,
        role: message.role,
        content: message.content
      }
    })
    
  } catch (e) {
    console.log(e);
  } finally {
    loading.value = false
    await nextTick()
    // scrollToBottom() if needed
  }
}

const clearChat = async () => {
  console.log("CLEARING CHAT");
  await clearAgent();
  console.log("CLEARED");
}
onMounted(() => {
  window.addEventListener("beforeunload", clearChat);
})
onBeforeUnmount(() => {
  clearAgent();
  window.removeEventListener("beforeunload", clearChat);

})
</script>

<style>

</style>