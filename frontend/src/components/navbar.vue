<template>
    <nav class="bg-white shadow-md border-b border-gray-200 px-6 py-4">
    <div class="flex justify-between items-center">
      <!-- Left side - Brand name -->
      <div class="flex items-center">
        <h1 class="text-2xl font-bold text-blue-600">SkillCompass</h1>
      </div>
      
      <!-- Right side - Navigation and user info -->
      <div class="flex items-center space-x-4">
        <!-- AI Agent icon button -->
        <router-link 
          to="/agent" 
          class="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-colors duration-200"
          title="AI Agent"
        >
          <img src="@/icons/sparkle-icon.svg" alt="AI Agent" class="w-6 h-6" />
        </router-link>
        
        <!-- List icon button -->
        <router-link 
          to="/jobs-list" 
          class="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-colors duration-200"
          title="View Jobs"
        >
          <img src="@/icons/list-bullets.svg" alt="Jobs List" class="w-6 h-6" />
        </router-link>
        
        <!-- Plus circle icon button -->
        <router-link 
          to="/create-job" 
          class="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-colors duration-200"
          title="Create Job"
        >
          <img src="@/icons/plus-circle-black.svg" alt="Create Job" class="w-6 h-6" />
        </router-link>
        
        <!-- User greeting -->
        <router-link 
          to="/user" 
          class="text-gray-700 font-medium hover:text-blue-600 hover:underline transition-colors duration-200 cursor-pointer"
        >
          Hello {{ userStore.email }}
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useUserStore } from '@/stores/user';

// Access the user store to get the current user's email
const userStore = useUserStore();
</script>