import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    { 
      path: '/dashboard', 
      name: 'dashboard', 
      component: DashboardView,
      meta: { requiresAuth: true } // Metadaten für geschützte Route
    } 
  ]
})

// Navigation Guard (Globaler Schutz)
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  
  // Wenn die Route Authentifizierung erfordert und kein Token da ist -> Login
  if (to.meta.requiresAuth && !token) {
    next('/login');
  } else {
    next(); // Sonst weiter
  }
});

export default router
