<template>
    <div class="min-h-screen flex items-center justify-center px-4">
      <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg border border-stone-200 p-8">
        <div class="mb-8 text-center">
          <h1 class="text-2xl font-bold text-stone-900 tracking-tight">SkillCompass</h1>
          <p class="mt-1 text-sm text-stone-500">Sign in to your account</p>
        </div>
        <form @submit.prevent="loginMethod" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-stone-700 mb-1.5">Email</label>
            <input v-model="email" type="email" required class="w-full px-3.5 py-2.5 text-sm rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition" placeholder="you@example.com" />
          </div>
          <div>
            <label class="block text-sm font-medium text-stone-700 mb-1.5">Password</label>
            <input v-model="password" type="password" required class="w-full px-3.5 py-2.5 text-sm rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition" placeholder="••••••••" />
          </div>
          <div v-if="error" class="text-sm text-red-500 text-center">{{ error }}</div>
          <button type="submit" class="w-full py-2.5 px-4 bg-teal-600 hover:bg-teal-700 text-white text-sm font-semibold rounded-lg transition-colors duration-200">
            Sign in
          </button>
        </form>
      </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router';
import { login, getCurrentUser } from '@/api/api';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();

const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter();

const loginMethod = async () => {
    error.value = '';
    try {
        await login(email.value, password.value)
        // const user = await getCurrentUser();
        // const { userEmail, first_name, last_name, id } = user;
        // console.log('userEmail', userEmail);
        // console.log('first_name', first_name);
        // console.log('last_name', last_name);
        // console.log('id', id);
        // userStore.setUser({ email: userEmail, first_name, last_name, id });
        router.push('/');
    }
    catch (err) {
        console.warn('err', err);
    }
}
</script>
