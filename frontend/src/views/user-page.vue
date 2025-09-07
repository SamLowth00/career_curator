<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Profile</h1>
        <p class="mt-2 text-gray-600">View and manage your account information</p>
      </div>

      <!-- User Information Card -->
      <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        <!-- Card Header -->
        <div class="bg-gradient-to-r from-primary to-primary-hover px-6 py-4">
          <h2 class="text-xl font-semibold text-white">Personal Information</h2>
        </div>

        <!-- Card Content -->
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- First Name -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">First Name</label>
              <div class="flex items-center p-3 bg-gray-50 rounded-lg border border-gray-200">
                <img src="@/icons/user-icon.svg" class="w-5 h-5 text-gray-400 mr-3" />
                <span class="text-gray-900 font-medium">{{ userStore.firstName || 'Not provided' }}</span>
              </div>
            </div>

            <!-- Last Name -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">Last Name</label>
              <div class="flex items-center p-3 bg-gray-50 rounded-lg border border-gray-200">
                <img src="@/icons/user-icon.svg" class="w-5 h-5 text-gray-400 mr-3" />
                <span class="text-gray-900 font-medium">{{ userStore.lastName || 'Not provided' }}</span>
              </div>
            </div>

            <!-- Email Address -->
            <div class="space-y-2 md:col-span-2">
              <label class="block text-sm font-medium text-gray-700">Email Address</label>
              <div class="flex items-center p-3 bg-gray-50 rounded-lg border border-gray-200">
                <img src="@/icons/email-logo.svg" class="w-5 h-5 text-gray-400 mr-3" />
                <span class="text-gray-900 font-medium">{{ userStore.email || 'Not provided' }}</span>
              </div>
            </div>
          </div>

          <!-- User ID (for debugging/development) -->
          <div class="mt-6 pt-6 border-t border-gray-200">
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-500">User ID</label>
              <div class="flex items-center p-3 bg-gray-100 rounded-lg">
                <img src="@/icons/tag-icon.svg" class="w-5 h-5 text-gray-400 mr-3" />
                <span class="text-gray-600 text-sm font-mono">{{ userStore.id || 'Not available' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Additional Info Card -->
      <div class="mt-6 bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Account Status</h3>
        </div>
        <div class="p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-3 h-3 bg-green-400 rounded-full"></div>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-gray-900">Account Active</p>
              <p class="text-sm text-gray-500">Your account is in good standing</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user.js'

// Get the user store instance
const userStore = useUserStore()
</script>

<style scoped>
/* Custom styles if needed */
</style>