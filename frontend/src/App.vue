<template>
    <div div class="bg-gradient-to-b from-white to-blue-200 h-[100vh]">
        <Navbar  v-if="userStore.email"/>
        <router-view />
    </div>
</template>

<script setup>
import Navbar from './components/navbar.vue';
import { useUserStore } from '@/stores/user';
import { useRoute } from 'vue-router';

const route = useRoute();
const userStore = useUserStore();

</script>

<style>

</style>