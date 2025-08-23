<template>
  <div class="register-page">
    <div class="register-container">
      <el-card class="register-card" shadow="always">
        <template #header>
          <div class="register-header">
            <el-icon class="register-icon"><UserFilled /></el-icon>
            <h2>Регистрация</h2>
            <p>Создайте аккаунт AI Content Curator</p>
          </div>
        </template>

        <el-form
          ref="registerFormRef"
          :model="registerForm"
          :rules="registerRules"
          label-width="0"
          size="large"
          @submit.prevent="handleRegister"
        >
          <el-form-item prop="username">
            <el-input
              v-model="registerForm.username"
              placeholder="Имя пользователя"
              prefix-icon="User"
              :disabled="loading"
            />
          </el-form-item>

          <el-form-item prop="email">
            <el-input
              v-model="registerForm.email"
              type="email"
              placeholder="Email"
              prefix-icon="Message"
              :disabled="loading"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="Пароль"
              prefix-icon="Lock"
              show-password
              :disabled="loading"
            />
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="Подтвердите пароль"
              prefix-icon="Lock"
              show-password
              :disabled="loading"
              @keyup.enter="handleRegister"
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              class="register-button"
              :loading="loading"
              @click="handleRegister"
              native-type="submit"
            >
              <span v-if="!loading">Зарегистрироваться</span>
              <span v-else>Регистрация...</span>
            </el-button>
          </el-form-item>
        </el-form>

        <div class="register-footer">
          <p>Уже есть аккаунт? 
            <router-link to="/login" class="login-link">
              Войти
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
import { UserFilled } from '@element-plus/icons-vue'

export default {
  name: 'RegisterView',
  components: {
    UserFilled
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const registerFormRef = ref()

    const registerForm = ref({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })

    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== registerForm.value.password) {
        callback(new Error('Пароли не совпадают'))
      } else {
        callback()
      }
    }

    const registerRules = {
      username: [
        { required: true, message: 'Введите имя пользователя', trigger: 'blur' },
        { min: 3, max: 50, message: 'Длина должна быть от 3 до 50 символов', trigger: 'blur' },
        { pattern: /^[a-zA-Z0-9_]+$/, message: 'Только латинские буквы, цифры и _', trigger: 'blur' }
      ],
      email: [
        { required: true, message: 'Введите email', trigger: 'blur' },
        { type: 'email', message: 'Некорректный формат email', trigger: 'blur' }
      ],
      password: [
        { required: true, message: 'Введите пароль', trigger: 'blur' },
        { min: 6, message: 'Пароль должен содержать минимум 6 символов', trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, message: 'Подтвердите пароль', trigger: 'blur' },
        { validator: validateConfirmPassword, trigger: 'blur' }
      ]
    }

    const loading = computed(() => store.getters['auth/loading'])

    const handleRegister = async () => {
      if (!registerFormRef.value) return

      try {
        const valid = await registerFormRef.value.validate()
        if (!valid) return

        const { confirmPassword, ...userData } = registerForm.value
        const result = await store.dispatch('auth/register', userData)
        
        if (result.success) {
          ElMessage.success('Регистрация успешна! Теперь вы можете войти в систему.')
          router.push('/login')
        } else {
          ElMessage.error(result.message || 'Ошибка при регистрации')
        }
      } catch (error) {
        console.error('Ошибка валидации:', error)
      }
    }

    return {
      registerForm,
      registerRules,
      registerFormRef,
      loading,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.register-container {
  width: 100%;
  max-width: 400px;
}

.register-card {
  border-radius: 16px;
  overflow: hidden;
}

.register-header {
  text-align: center;
  padding: 20px 0;
}

.register-icon {
  font-size: 48px;
  color: #667eea;
  margin-bottom: 20px;
}

.register-header h2 {
  margin: 0 0 10px 0;
  color: #2c3e50;
  font-size: 24px;
}

.register-header p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.register-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.register-button:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
}

.register-footer {
  text-align: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.register-footer p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.login-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.login-link:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .register-page {
    padding: 10px;
  }
  
  .register-container {
    max-width: 100%;
  }
}
</style>
