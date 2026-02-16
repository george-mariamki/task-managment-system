import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  // history: يستخدم لتغيير الرابط في المتصفح دون إعادة تحميل الصفحة
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',      // الرابط الأساسي
      name: 'home',   // اسم داخلي نستخدمه في الكود
      component: HomeView // المكون الذي سيعرض عند زيارة هذا الرابط
    }
  ]
})

export default router
