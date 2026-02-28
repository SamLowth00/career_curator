<template>
  <div class="min-h-screen bg-stone-50 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Profile</h1>
        <p class="mt-2 text-gray-600">View and manage your account information</p>
      </div>

      <UserInfoCard />
      <AccountStatusCard />
      <UserSkillsCard />
    </div>
  </div>
</template>

<script setup>
import UserInfoCard from '@/components/user-info-card.vue'
import AccountStatusCard from '@/components/account-status-card.vue'
import UserSkillsCard from '@/components/user-skills-card.vue'
</script>
