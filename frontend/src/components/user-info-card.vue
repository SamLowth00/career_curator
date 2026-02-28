<template>
  <div class="bg-white rounded-xl shadow-lg border border-stone-200 overflow-hidden">
    <div class="bg-gradient-to-r from-primary to-primary-hover px-6 py-4">
      <h2 class="text-xl font-semibold text-white">Personal Information</h2>
    </div>

    <div class="p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700">First Name</label>
          <div class="flex items-center p-3 bg-stone-50 rounded-lg border border-stone-200">
            <img src="@/icons/user-icon.svg" class="w-5 h-5 text-gray-400 mr-3" />
            <span class="text-gray-900 font-medium">{{ userStore.firstName || 'Not provided' }}</span>
          </div>
        </div>

        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700">Last Name</label>
          <div class="flex items-center p-3 bg-stone-50 rounded-lg border border-stone-200">
            <img src="@/icons/user-icon.svg" class="w-5 h-5 text-gray-400 mr-3" />
            <span class="text-gray-900 font-medium">{{ userStore.lastName || 'Not provided' }}</span>
          </div>
        </div>

        <div class="space-y-2 md:col-span-2">
          <label class="block text-sm font-medium text-gray-700">Email Address</label>
          <div class="flex items-center p-3 bg-stone-50 rounded-lg border border-stone-200">
            <img src="@/icons/email-logo.svg" class="w-5 h-5 text-gray-400 mr-3" />
            <span class="text-gray-900 font-medium">{{ userStore.email || 'Not provided' }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user.js'

const userStore = useUserStore()
</script>
