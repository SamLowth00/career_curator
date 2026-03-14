<template>
  <dialog ref="dialogEl" class="rounded-xl shadow-xl p-0 backdrop:bg-black/40 w-full max-w-sm m-auto">
    <div class="p-6 flex flex-col gap-4">
      <template v-if="!deleting">
        <h2 class="text-lg font-semibold text-gray-800">Delete Job</h2>
        <p class="text-gray-600 text-sm">Are you sure you want to delete this job? This action cannot be undone.</p>
        <div class="flex justify-end gap-3 mt-2">
          <button @click="cancel" class="px-4 py-2 rounded-lg text-sm text-gray-700 border border-stone-200 hover:bg-stone-50 cursor-pointer">
            Cancel
          </button>
          <button @click="confirm" class="px-4 py-2 rounded-lg text-sm text-white bg-red-500 hover:bg-red-600 cursor-pointer">
            Delete
          </button>
        </div>
      </template>
      <template v-else>
        <div class="flex flex-col items-center gap-4 py-2">
          <div class="relative w-10 h-10">
            <div class="absolute inset-0 rounded-full border-4 border-teal-100"></div>
            <div class="absolute inset-0 rounded-full border-4 border-t-teal-600 animate-spin"></div>
          </div>
          <p class="text-sm font-medium text-gray-700">Deleting job...</p>
        </div>
      </template>
    </div>
  </dialog>
</template>

<script setup>
import { ref } from 'vue'

const dialogEl = ref(null)
const deleting = ref(false)

const emit = defineEmits(['confirm', 'cancel'])

function open() {
  deleting.value = false
  dialogEl.value.showModal()
}

function cancel() {
  dialogEl.value.close()
  emit('cancel')
}

function confirm() {
  deleting.value = true
  emit('confirm')
}

function close() {
  dialogEl.value.close()
}

defineExpose({ open, close })
</script>
