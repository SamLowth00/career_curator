<template>
  <Transition name="fade">
    <div v-if="visible" class="fixed inset-0 z-50 flex flex-col items-center justify-center bg-white/80 backdrop-blur-sm">
      <div class="flex flex-col items-center gap-6">
        <div class="relative w-16 h-16">
          <div class="absolute inset-0 rounded-full border-4 border-teal-100"></div>
          <div class="absolute inset-0 rounded-full border-4 border-t-teal-600 animate-spin"></div>
        </div>
        <div class="text-center">
          <p class="text-lg font-semibold text-gray-800">{{ currentMessage }}</p>
          <div class="flex justify-center gap-1 mt-2">
            <span v-for="i in 3" :key="i" class="w-1.5 h-1.5 rounded-full bg-teal-500 animate-bounce" :style="{ animationDelay: `${(i - 1) * 0.15}s` }"></span>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    required: true,
  },
  messages: {
    type: Array,
    default: () => ['Loading...'],
  },
})

const currentMessage = ref(props.messages[0])
let messageInterval = null

watch(() => props.visible, (val) => {
  if (val) {
    currentMessage.value = props.messages[0]
    let i = 0
    messageInterval = setInterval(() => {
      i = (i + 1) % props.messages.length
      currentMessage.value = props.messages[i]
    }, 2000)
  } else {
    clearInterval(messageInterval)
    currentMessage.value = props.messages[0]
  }
})
</script>
