import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/css/global.css'
import './assets/css/auth.css'
import './assets/css/dashboard.css'

createApp(App).use(router).mount('#app')