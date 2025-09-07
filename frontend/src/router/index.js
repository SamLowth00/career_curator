import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/home-page.vue'
import UserPage from '@/views/user-page.vue'
import Login from '@/views/login.vue'
import { getCurrentUser } from '@/api/api'
import { useUserStore } from '@/stores/user';
import CreateJob from '@/views/create-job.vue';
import JobsList from '@/views/jobs-list.vue';
import JobAgent from '@/views/job-agent.vue';
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/',
      name: 'Home',
      component: HomePage,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/user',
      name: 'User',
      component: UserPage,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/create-job',
      name: 'CreateJob',
      component: CreateJob,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/jobs-list',
      name: 'JobsList',
      component: JobsList,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/agent',
      name: 'Agent',
      component: JobAgent,
      meta: {
        requiresAuth: true
      }
    }
  ],
})

router.beforeEach(async (to, from, next) => {
  console.log('test');
  if (to.meta.requiresAuth) {
    try {
    console.log('try');
      const userStore = useUserStore();
      const user = await getCurrentUser();
      console.log(user);
      userStore.setUser(user);
      next()
    } catch {
      console.log('login');
      next({ name: 'Login' })
    }
  } else {
    next()
  }
})

export default router
