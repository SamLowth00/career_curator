import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
    state: () => ({
        id: null,
        email: null,
        firstName: '',
        lastName: '',
    }),
    actions: {
        setUser(user) {
            console.log('setting user', user);
            this.id = user.id;
            this.email = user.email;
            this.firstName = user.first_name;
            this.lastName = user.last_name;
        },
        clearUser() {
            this.id = null;
            this.email = null;
            this.firstName = '';
            this.lastName = '';
        }
    }
})