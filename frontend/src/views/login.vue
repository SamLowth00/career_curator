<template>
    <div class="login-container">
      <h2 class="bg-primary">Login</h2>
      <form @submit.prevent="loginMethod">
        <div>
          <label>Email:</label>
          <input v-model="email" type="email" required />
        </div>
        <div>
          <label>Password:</label>
          <input v-model="password" type="password" required />
        </div>
        <button type="submit">Login</button>
        <div v-if="error" class="error">{{ error }}</div>
      </form>
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