<template>
  <div class="dashboard">
    <div class="page-container">
      <!-- Заголовок -->
      <div class="dashboard-header">
        <h1>Панель управления</h1>
        <p>Добро пожаловать, {{ currentUser?.username }}! Анализируйте контент с помощью ИИ.</p>
      </div>

      <!-- Статистика -->
      <div class="stats-section mb-30">
        <el-row :gutter="20">
          <el-col :xs="12" :sm="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-icon sentiment">
                  <el-icon><ChatDotRound /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-number">{{ stats.sentiment || 0 }}</div>
                  <div class="stat-label">Анализ тональности</div>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :xs="12" :sm="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-icon summary">
                  <el-icon><Document /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-number">{{ stats.summary || 0 }}</div>
                  <div class="stat-label">Выжимки</div>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :xs="12" :sm="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-icon keywords">
                  <el-icon><Key /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-number">{{ stats.keywords || 0 }}</div>
                  <div class="stat-label">Ключевые слова</div>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :xs="12" :sm="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-icon total">
                  <el-icon><DataAnalysis /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-number">{{ stats.total || 0 }}</div>
                  <div class="stat-label">Всего анализов</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- Быстрые действия -->
      <div class="quick-actions mb-30">
        <h2>Быстрые действия</h2>
        <el-row :gutter="20">
          <el-col :xs="24" :sm="8">
            <el-card class="action-card" shadow="hover" @click="$router.push('/analysis')">
              <div class="action-content">
                <el-icon class="action-icon"><EditPen /></el-icon>
                <h3>Новый анализ</h3>
                <p>Анализируйте текст с помощью ИИ</p>
              </div>
            </el-card>
          </el-col>
          
          <el-col :xs="24" :sm="8">
            <el-card class="action-card" shadow="hover" @click="$router.push('/history')">
              <div class="action-content">
                <el-icon class="action-icon"><Clock /></el-icon>
                <h3>История</h3>
                <p>Просмотрите предыдущие анализы</p>
              </div>
            </el-card>
          </el-col>
          
          <el-col :xs="24" :sm="8">
            <el-card class="action-card" shadow="hover" @click="openTelegramInfo">
              <div class="action-content">
                <el-icon class="action-icon"><ChatLineRound /></el-icon>
                <h3>Telegram бот</h3>
                <p>Подключите бота для быстрого доступа</p>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- Последние анализы -->
      <div class="recent-analyses">
        <div class="section-header">
          <h2>Последние анализы</h2>
          <el-button type="primary" @click="$router.push('/history')">
            Посмотреть все
          </el-button>
        </div>
        
        <div v-if="loading" class="loading-spinner">
          <el-icon class="is-loading"><Loading /></el-icon>
          <span>Загрузка анализов...</span>
        </div>
        
        <div v-else-if="recentAnalyses.length === 0" class="empty-state">
          <el-empty description="Пока нет анализов">
            <el-button type="primary" @click="$router.push('/analysis')">
              Создать первый анализ
            </el-button>
          </el-empty>
        </div>
        
        <div v-else class="analyses-list">
          <el-card 
            v-for="analysis in recentAnalyses" 
            :key="analysis.id"
            class="analysis-card"
            shadow="hover"
          >
            <div class="analysis-header">
              <div class="analysis-type">
                <el-tag 
                  :type="getAnalysisTypeColor(analysis.analysis_type)"
                  size="small"
                >
                  {{ getAnalysisTypeName(analysis.analysis_type) }}
                </el-tag>
              </div>
              <div class="analysis-date">
                {{ formatDate(analysis.created_at) }}
              </div>
            </div>
            
            <div class="analysis-text">
              {{ truncateText(analysis.original_text, 100) }}
            </div>
            
            <div class="analysis-result">
              {{ truncateText(analysis.result, 150) }}
            </div>
            
            <div class="analysis-footer">
              <div class="analysis-meta">
                <span v-if="analysis.confidence_score" class="confidence">
                  Уверенность: {{ analysis.confidence_score }}
                </span>
                <span v-if="analysis.processing_time" class="processing-time">
                  {{ analysis.processing_time }}
                </span>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>

    <!-- Диалог информации о Telegram боте -->
    <el-dialog
      v-model="telegramDialogVisible"
      title="Telegram бот"
      width="500px"
    >
      <div class="telegram-info">
        <p>Для подключения Telegram бота:</p>
        <ol>
          <li>Найдите бота <strong>@AIContentCuratorBot</strong> в Telegram</li>
          <li>Отправьте команду <code>/start</code></li>
          <li>Следуйте инструкциям для привязки аккаунта</li>
        </ol>
        <p>После подключения вы сможете анализировать тексты прямо из Telegram!</p>
      </div>
      <template #footer>
        <el-button @click="telegramDialogVisible = false">Понятно</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { 
  ChatDotRound, 
  Document, 
  Key, 
  DataAnalysis,
  EditPen,
  Clock,
  ChatLineRound,
  Loading
} from '@element-plus/icons-vue'

export default {
  name: 'DashboardView',
  components: {
    ChatDotRound,
    Document,
    Key,
    DataAnalysis,
    EditPen,
    Clock,
    ChatLineRound,
    Loading
  },
  setup() {
    const store = useStore()
    const telegramDialogVisible = ref(false)

    const currentUser = computed(() => store.getters['auth/currentUser'])
    const stats = computed(() => store.getters['analysis/stats'])
    const loading = computed(() => store.getters['analysis/loading'])
    const analyses = computed(() => store.getters['analysis/analyses'])

    const recentAnalyses = computed(() => analyses.value.slice(0, 5))

    const getAnalysisTypeName = (type) => {
      const names = {
        sentiment: 'Тональность',
        summary: 'Выжимка',
        keywords: 'Ключевые слова'
      }
      return names[type] || type
    }

    const getAnalysisTypeColor = (type) => {
      const colors = {
        sentiment: 'success',
        summary: 'primary',
        keywords: 'warning'
      }
      return colors[type] || 'info'
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const truncateText = (text, maxLength) => {
      if (text.length <= maxLength) return text
      return text.substring(0, maxLength) + '...'
    }

    const openTelegramInfo = () => {
      telegramDialogVisible.value = true
    }

    onMounted(() => {
      store.dispatch('analysis/fetchAnalyses', { limit: 10 })
    })

    return {
      currentUser,
      stats,
      loading,
      recentAnalyses,
      telegramDialogVisible,
      getAnalysisTypeName,
      getAnalysisTypeColor,
      formatDate,
      truncateText,
      openTelegramInfo
    }
  }
}
</script>

<style scoped>
.dashboard-header {
  text-align: center;
  margin-bottom: 40px;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.dashboard-header p {
  font-size: 1.1rem;
  color: #666;
}

.stat-card {
  height: 100px;
  cursor: default;
}

.stat-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 24px;
  color: white;
}

.stat-icon.sentiment { background: linear-gradient(135deg, #52c41a, #389e0d); }
.stat-icon.summary { background: linear-gradient(135deg, #1890ff, #096dd9); }
.stat-icon.keywords { background: linear-gradient(135deg, #fa8c16, #d48806); }
.stat-icon.total { background: linear-gradient(135deg, #722ed1, #531dab); }

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  line-height: 1;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
  margin-top: 5px;
}

.quick-actions h2 {
  margin-bottom: 20px;
  color: #2c3e50;
}

.action-card {
  height: 140px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.action-card:hover {
  transform: translateY(-5px);
}

.action-content {
  text-align: center;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.action-icon {
  font-size: 32px;
  color: #667eea;
  margin-bottom: 10px;
}

.action-content h3 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 1.1rem;
}

.action-content p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.recent-analyses {
  margin-top: 40px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0;
  color: #2c3e50;
}

.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #666;
  gap: 10px;
}

.empty-state {
  text-align: center;
  padding: 40px;
}

.analyses-list {
  display: grid;
  gap: 15px;
}

.analysis-card {
  transition: transform 0.2s ease;
}

.analysis-card:hover {
  transform: translateY(-2px);
}

.analysis-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.analysis-date {
  color: #999;
  font-size: 0.85rem;
}

.analysis-text {
  background: #f8f9fa;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 10px;
  font-size: 0.9rem;
  color: #555;
}

.analysis-result {
  color: #2c3e50;
  line-height: 1.5;
  margin-bottom: 10px;
}

.analysis-footer {
  border-top: 1px solid #eee;
  padding-top: 10px;
}

.analysis-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #999;
}

.telegram-info {
  line-height: 1.6;
}

.telegram-info code {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
}

@media (max-width: 768px) {
  .dashboard-header h1 {
    font-size: 2rem;
  }
  
  .section-header {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }
  
  .stat-content {
    flex-direction: column;
    text-align: center;
  }
  
  .stat-icon {
    margin-right: 0;
    margin-bottom: 10px;
  }
}
</style>
