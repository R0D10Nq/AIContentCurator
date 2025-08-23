<template>
  <div id="app">
    <el-container class="app-container">
      <!-- Хедер -->
      <el-header class="app-header">
        <div class="header-content">
          <div class="logo">
            <el-icon class="logo-icon"><Brain /></el-icon>
            <span class="logo-text">AI Content Curator</span>
          </div>
          
          <div class="header-actions" v-if="isAuthenticated">
            <el-dropdown @command="handleUserMenu">
              <span class="user-info">
                <el-icon><User /></el-icon>
                {{ currentUser.username }}
                <el-icon class="el-icon--right"><arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">Профиль</el-dropdown-item>
                  <el-dropdown-item command="logout" divided>Выйти</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          
          <div class="auth-buttons" v-else>
            <el-button type="primary" @click="$router.push('/login')">Войти</el-button>
            <el-button @click="$router.push('/register')">Регистрация</el-button>
          </div>
        </div>
      </el-header>

      <!-- Основной контент -->
      <el-main class="app-main">
        <router-view />
      </el-main>

      <!-- Футер -->
      <el-footer class="app-footer">
        <div class="footer-content">
          <p>&copy; 2024 AI Content Curator. Анализ контента с помощью ИИ.</p>
          <div class="footer-links">
            <a href="https://github.com" target="_blank">GitHub</a>
            <span>|</span>
            <a href="/docs" target="_blank">API Docs</a>
          </div>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { Brain, User, ArrowDown } from '@element-plus/icons-vue'

export default {
  name: 'App',
  components: {
    Brain,
    User,
    ArrowDown
  },
  setup() {
    const store = useStore()
    const router = useRouter()

    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated'])
    const currentUser = computed(() => store.getters['auth/currentUser'])

    const handleUserMenu = (command) => {
      if (command === 'logout') {
        store.dispatch('auth/logout')
        router.push('/login')
      } else if (command === 'profile') {
        router.push('/profile')
      }
    }

    // Проверяем токен при загрузке приложения
    store.dispatch('auth/checkAuth')

    return {
      isAuthenticated,
      currentUser,
      handleUserMenu
    }
  }
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
}

.logo-icon {
  font-size: 24px;
  margin-right: 10px;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: white;
}

.user-info:hover {
  color: #f0f0f0;
}

.auth-buttons {
  display: flex;
  gap: 10px;
}

.app-main {
  background-color: #f5f7fa;
  min-height: calc(100vh - 120px);
  padding: 20px;
}

.app-footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 20px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-links {
  display: flex;
  gap: 10px;
  align-items: center;
}

.footer-links a {
  color: #bdc3c7;
  text-decoration: none;
}

.footer-links a:hover {
  color: white;
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 10px;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 10px;
  }
  
  .logo-text {
    display: none;
  }
}
</style>
