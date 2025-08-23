<template>
  <div class="profile-page">
    <div class="page-container">
      <!-- Заголовок -->
      <div class="page-header">
        <h1>Профиль пользователя</h1>
        <p>Управляйте своими данными и настройками</p>
      </div>

      <el-row :gutter="30">
        <!-- Информация о пользователе -->
        <el-col :xs="24" :lg="8">
          <el-card class="profile-card" shadow="always">
            <template #header>
              <div class="card-header">
                <el-icon><User /></el-icon>
                <span>Информация о пользователе</span>
              </div>
            </template>

            <div class="profile-info">
              <div class="avatar-section">
                <el-avatar :size="80" class="profile-avatar">
                  <el-icon><UserFilled /></el-icon>
                </el-avatar>
                <h3>{{ currentUser?.username }}</h3>
                <p>{{ currentUser?.email }}</p>
              </div>

              <div class="profile-stats">
                <div class="stat-item">
                  <div class="stat-number">{{ stats.total || 0 }}</div>
                  <div class="stat-label">Всего анализов</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ formatDate(currentUser?.created_at) }}</div>
                  <div class="stat-label">Дата регистрации</div>
                </div>
              </div>
            </div>
          </el-card>

          <!-- Telegram интеграция -->
          <el-card class="telegram-card mt-20" shadow="always">
            <template #header>
              <div class="card-header">
                <el-icon><ChatLineRound /></el-icon>
                <span>Telegram интеграция</span>
              </div>
            </template>

            <div class="telegram-status">
              <div v-if="currentUser?.telegram_id" class="connected">
                <el-icon class="status-icon success"><SuccessFilled /></el-icon>
                <div class="status-text">
                  <h4>Подключено</h4>
                  <p>Telegram ID: {{ currentUser.telegram_id }}</p>
                </div>
                <el-button type="danger" size="small" @click="disconnectTelegram">
                  Отключить
                </el-button>
              </div>
              <div v-else class="not-connected">
                <el-icon class="status-icon warning"><WarningFilled /></el-icon>
                <div class="status-text">
                  <h4>Не подключено</h4>
                  <p>Подключите Telegram бота для быстрого доступа</p>
                </div>
                <el-button type="primary" @click="showTelegramInstructions">
                  Подключить
                </el-button>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- Редактирование профиля -->
        <el-col :xs="24" :lg="16">
          <el-card class="edit-profile-card" shadow="always">
            <template #header>
              <div class="card-header">
                <el-icon><Edit /></el-icon>
                <span>Редактировать профиль</span>
              </div>
            </template>

            <el-form
              ref="profileFormRef"
              :model="profileForm"
              :rules="profileRules"
              label-width="120px"
              size="large"
            >
              <el-form-item label="Имя пользователя" prop="username">
                <el-input
                  v-model="profileForm.username"
                  :disabled="loading"
                  placeholder="Введите имя пользователя"
                />
              </el-form-item>

              <el-form-item label="Email" prop="email">
                <el-input
                  v-model="profileForm.email"
                  type="email"
                  :disabled="loading"
                  placeholder="Введите email"
                />
              </el-form-item>

              <el-form-item>
                <el-button
                  type="primary"
                  :loading="loading"
                  @click="updateProfile"
                >
                  Сохранить изменения
                </el-button>
                <el-button @click="resetForm">
                  Отменить
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>

          <!-- Смена пароля -->
          <el-card class="password-card mt-20" shadow="always">
            <template #header>
              <div class="card-header">
                <el-icon><Lock /></el-icon>
                <span>Смена пароля</span>
              </div>
            </template>

            <el-form
              ref="passwordFormRef"
              :model="passwordForm"
              :rules="passwordRules"
              label-width="120px"
              size="large"
            >
              <el-form-item label="Текущий пароль" prop="currentPassword">
                <el-input
                  v-model="passwordForm.currentPassword"
                  type="password"
                  :disabled="loading"
                  show-password
                  placeholder="Введите текущий пароль"
                />
              </el-form-item>

              <el-form-item label="Новый пароль" prop="newPassword">
                <el-input
                  v-model="passwordForm.newPassword"
                  type="password"
                  :disabled="loading"
                  show-password
                  placeholder="Введите новый пароль"
                />
              </el-form-item>

              <el-form-item label="Подтвердите пароль" prop="confirmPassword">
                <el-input
                  v-model="passwordForm.confirmPassword"
                  type="password"
                  :disabled="loading"
                  show-password
                  placeholder="Подтвердите новый пароль"
                />
              </el-form-item>

              <el-form-item>
                <el-button
                  type="primary"
                  :loading="loading"
                  @click="changePassword"
                >
                  Изменить пароль
                </el-button>
                <el-button @click="resetPasswordForm">
                  Очистить
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>

          <!-- Статистика активности -->
          <el-card class="activity-card mt-20" shadow="always">
            <template #header>
              <div class="card-header">
                <el-icon><TrendCharts /></el-icon>
                <span>Статистика активности</span>
              </div>
            </template>

            <div class="activity-stats">
              <el-row :gutter="20">
                <el-col :xs="12" :sm="6">
                  <div class="activity-item sentiment">
                    <el-icon class="activity-icon"><ChatDotRound /></el-icon>
                    <div class="activity-info">
                      <div class="activity-number">{{ stats.sentiment || 0 }}</div>
                      <div class="activity-label">Анализ тональности</div>
                    </div>
                  </div>
                </el-col>
                <el-col :xs="12" :sm="6">
                  <div class="activity-item summary">
                    <el-icon class="activity-icon"><Document /></el-icon>
                    <div class="activity-info">
                      <div class="activity-number">{{ stats.summary || 0 }}</div>
                      <div class="activity-label">Выжимки</div>
                    </div>
                  </div>
                </el-col>
                <el-col :xs="12" :sm="6">
                  <div class="activity-item keywords">
                    <el-icon class="activity-icon"><Key /></el-icon>
                    <div class="activity-info">
                      <div class="activity-number">{{ stats.keywords || 0 }}</div>
                      <div class="activity-label">Ключевые слова</div>
                    </div>
                  </div>
                </el-col>
                <el-col :xs="12" :sm="6">
                  <div class="activity-item total">
                    <el-icon class="activity-icon"><DataAnalysis /></el-icon>
                    <div class="activity-info">
                      <div class="activity-number">{{ stats.total || 0 }}</div>
                      <div class="activity-label">Всего</div>
                    </div>
                  </div>
                </el-col>
              </el-row>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- Диалог инструкций Telegram -->
    <el-dialog
      v-model="telegramDialogVisible"
      title="Подключение Telegram бота"
      width="500px"
    >
      <div class="telegram-instructions">
        <p><strong>Для подключения Telegram бота выполните следующие шаги:</strong></p>
        <ol>
          <li>Найдите бота <code>@AIContentCuratorBot</code> в Telegram</li>
          <li>Отправьте команду <code>/start</code></li>
          <li>Отправьте команду <code>/connect {{ currentUser?.username }}</code></li>
          <li>Следуйте дальнейшим инструкциям бота</li>
        </ol>
        <el-alert
          title="Важно!"
          description="После успешного подключения обновите страницу, чтобы увидеть изменения в профиле."
          type="info"
          :closable="false"
        />
      </div>
      <template #footer>
        <el-button @click="telegramDialogVisible = false">Понятно</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import {
  User,
  UserFilled,
  ChatLineRound,
  SuccessFilled,
  WarningFilled,
  Edit,
  Lock,
  TrendCharts,
  ChatDotRound,
  Document,
  Key,
  DataAnalysis
} from '@element-plus/icons-vue'

export default {
  name: 'ProfileView',
  components: {
    User,
    UserFilled,
    ChatLineRound,
    SuccessFilled,
    WarningFilled,
    Edit,
    Lock,
    TrendCharts,
    ChatDotRound,
    Document,
    Key,
    DataAnalysis
  },
  setup() {
    const store = useStore()
    const profileFormRef = ref()
    const passwordFormRef = ref()
    const telegramDialogVisible = ref(false)

    const profileForm = ref({
      username: '',
      email: ''
    })

    const passwordForm = ref({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    })

    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== passwordForm.value.newPassword) {
        callback(new Error('Пароли не совпадают'))
      } else {
        callback()
      }
    }

    const profileRules = {
      username: [
        { required: true, message: 'Введите имя пользователя', trigger: 'blur' },
        { min: 3, max: 50, message: 'Длина должна быть от 3 до 50 символов', trigger: 'blur' }
      ],
      email: [
        { required: true, message: 'Введите email', trigger: 'blur' },
        { type: 'email', message: 'Некорректный формат email', trigger: 'blur' }
      ]
    }

    const passwordRules = {
      currentPassword: [
        { required: true, message: 'Введите текущий пароль', trigger: 'blur' }
      ],
      newPassword: [
        { required: true, message: 'Введите новый пароль', trigger: 'blur' },
        { min: 6, message: 'Пароль должен содержать минимум 6 символов', trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, message: 'Подтвердите пароль', trigger: 'blur' },
        { validator: validateConfirmPassword, trigger: 'blur' }
      ]
    }

    const currentUser = computed(() => store.getters['auth/currentUser'])
    const loading = computed(() => store.getters['auth/loading'])
    const stats = computed(() => store.getters['analysis/stats'])

    const formatDate = (dateString) => {
      if (!dateString) return 'Не указано'
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    }

    const updateProfile = async () => {
      if (!profileFormRef.value) return

      try {
        const valid = await profileFormRef.value.validate()
        if (!valid) return

        // Здесь должен быть запрос к API для обновления профиля
        // Пока что просто показываем сообщение
        ElMessage.success('Профиль обновлен!')
      } catch (error) {
        console.error('Ошибка валидации:', error)
      }
    }

    const changePassword = async () => {
      if (!passwordFormRef.value) return

      try {
        const valid = await passwordFormRef.value.validate()
        if (!valid) return

        // Здесь должен быть запрос к API для смены пароля
        // Пока что просто показываем сообщение
        ElMessage.success('Пароль изменен!')
        resetPasswordForm()
      } catch (error) {
        console.error('Ошибка валидации:', error)
      }
    }

    const resetForm = () => {
      if (currentUser.value) {
        profileForm.value.username = currentUser.value.username
        profileForm.value.email = currentUser.value.email
      }
    }

    const resetPasswordForm = () => {
      passwordForm.value.currentPassword = ''
      passwordForm.value.newPassword = ''
      passwordForm.value.confirmPassword = ''
      if (passwordFormRef.value) {
        passwordFormRef.value.clearValidate()
      }
    }

    const showTelegramInstructions = () => {
      telegramDialogVisible.value = true
    }

    const disconnectTelegram = () => {
      ElMessage.success('Telegram отключен')
      // Здесь должен быть запрос к API для отключения Telegram
    }

    // Инициализация формы при загрузке пользователя
    watch(currentUser, (user) => {
      if (user) {
        profileForm.value.username = user.username
        profileForm.value.email = user.email
      }
    }, { immediate: true })

    onMounted(() => {
      store.dispatch('analysis/fetchAnalyses', { limit: 100 })
    })

    return {
      profileForm,
      passwordForm,
      profileRules,
      passwordRules,
      profileFormRef,
      passwordFormRef,
      telegramDialogVisible,
      currentUser,
      loading,
      stats,
      formatDate,
      updateProfile,
      changePassword,
      resetForm,
      resetPasswordForm,
      showTelegramInstructions,
      disconnectTelegram
    }
  }
}
</script>

<style scoped>
.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.page-header p {
  font-size: 1.1rem;
  color: #666;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  color: #2c3e50;
}

.profile-info {
  text-align: center;
}

.avatar-section {
  margin-bottom: 30px;
}

.profile-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  margin-bottom: 15px;
}

.avatar-section h3 {
  margin: 0 0 5px 0;
  color: #2c3e50;
  font-size: 1.3rem;
}

.avatar-section p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.profile-stats {
  display: flex;
  justify-content: space-around;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.8rem;
  color: #999;
}

.telegram-status {
  display: flex;
  align-items: center;
  gap: 15px;
}

.status-icon {
  font-size: 24px;
}

.status-icon.success {
  color: #52c41a;
}

.status-icon.warning {
  color: #fa8c16;
}

.status-text {
  flex: 1;
}

.status-text h4 {
  margin: 0 0 5px 0;
  color: #2c3e50;
  font-size: 1rem;
}

.status-text p {
  margin: 0;
  color: #666;
  font-size: 0.85rem;
}

.activity-stats {
  padding: 10px 0;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border-radius: 8px;
  background: #f8f9fa;
  margin-bottom: 10px;
}

.activity-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.activity-item.sentiment .activity-icon {
  background: linear-gradient(135deg, #52c41a, #389e0d);
}

.activity-item.summary .activity-icon {
  background: linear-gradient(135deg, #1890ff, #096dd9);
}

.activity-item.keywords .activity-icon {
  background: linear-gradient(135deg, #fa8c16, #d48806);
}

.activity-item.total .activity-icon {
  background: linear-gradient(135deg, #722ed1, #531dab);
}

.activity-info {
  flex: 1;
}

.activity-number {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
  line-height: 1;
}

.activity-label {
  color: #666;
  font-size: 0.85rem;
  margin-top: 2px;
}

.telegram-instructions {
  line-height: 1.6;
}

.telegram-instructions code {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  color: #e83e8c;
}

.telegram-instructions ol {
  margin: 20px 0;
  padding-left: 20px;
}

.telegram-instructions li {
  margin-bottom: 8px;
}

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 2rem;
  }
  
  .profile-stats {
    flex-direction: column;
    gap: 15px;
  }
  
  .telegram-status {
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }
  
  .activity-item {
    justify-content: center;
    text-align: center;
  }
}
</style>
