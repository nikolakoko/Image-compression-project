import { createApp } from 'vue'
import App from './App.vue'

// Import Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// Import Font Awesome
import '@fortawesome/fontawesome-free/css/all.min.css'

// Import custom global styles
import './style.css'

createApp(App).mount('#app')