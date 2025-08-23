<template>
  <div class="login-page">
    <div class="login-container">
      <el-card class="login-card" shadow="always">
        <template #header>
          <div class="login-header">
            <el-icon class="login-icon"><User /></el-icon>
            <h2>Вход в систему</h2>
            <p>Войдите в свой аккаунт AI Content Curator</p>
          </div>
        </template>

        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          label-width="0"
          size="large"
          @submit.prevent="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="Имя пользователя"
              prefix-icon="User"
              :disabled="loading"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="Пароль"
              prefix-icon="Lock"
              show-password
              :disabled="loading"
              @keyup.enter="handleLogin"
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              class="login-button"
              :loading="loading"
              @click="handleLogin"
              native-type="submit"
            >
              <span v-if="!loading">Войти</span>
              <span v-else>Вход...</span>
            </el-button>
          </el-form-item>
        </el-form>

        <div class="login-footer">
          <p>Нет аккаунта? 
            <router-link to="/register" class="register-link">
              Зарегистрироваться
            </router-link>
          </p>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User } from '@element-plus/icons-vue'

export default {
  name: 'LoginView',
  components: {
    User
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const loginFormRef = ref()

    const loginForm = ref({
      username: '',
      password: ''
    })

    const loginRules = {
      username: [
        { required: true, message: 'Введите имя пользователя', trigger: 'blur' },
        { min: 3, max: 50, message: 'Длина должна быть от 3 до 50 символов', trigger: 'blur' }
      ],
      password: [
        { required: true, message: 'Введите пароль', trigger: 'blur' },
        { min: 6, message: 'Пароль должен содержать минимум 6 символов', trigger: 'blur' }
      ]
    }

    const loading = computed(() => store.getters['auth/loading'])
    const error = computed(() => store.getters['auth/error'])

    const handleLogin = async () => {
      if (!loginFormRef.value) return

      try {
        const valid = await loginFormRef.value.validate()
        if (!valid) return

        const result = await store.dispatch('auth/login', loginForm.value)
        
        if (result.success) {
          ElMessage.success('Успешный вход в систему!')
          router.push('/dashboard')
        } else {
          ElMessage.error(result.message || 'Ошибка при входе')
        }
      } catch (error) {
        console.error('Ошибка валидации:', error)
      }
    }

    return {
      loginForm,
      loginRules,
      loginFormRef,
      loading,
      error,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 400px;
}

.login-card {
  border-radius: 16px;
  overflow: hidden;
}

.login-header {
  text-align: center;
  padding: 20px 0;
}

.login-icon {
  font-size: 48px;
  color: #667eea;
  margin-bottom: 20px;
}

.login-header h2 {
  margin: 0 0 10px 0;
  color: #2c3e50;
  font-size: 24px;
}

.login-header p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.login-button:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
}

.login-footer {
  text-align: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.login-footer p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.register-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.register-link:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .login-page {
    padding: 10px;
  }
  
  .login-container {
    max-width: 100%;
  }
}
</style>
