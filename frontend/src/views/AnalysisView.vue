<template>
  <div class="analysis-page">
    <div class="page-container">
      <!-- Заголовок -->
      <div class="page-header">
        <h1>Анализ контента</h1>
        <p>Анализируйте текст с помощью искусственного интеллекта Gemini</p>
      </div>

      <el-row :gutter="30">
        <!-- Форма анализа -->
        <el-col :xs="24" :lg="12">
          <el-card class="analysis-form-card" shadow="always">
            <template #header>
              <div class="card-header">
                <el-icon><EditPen /></el-icon>
                <span>Новый анализ</span>
              </div>
            </template>

            <el-form
              ref="analysisFormRef"
              :model="analysisForm"
              :rules="analysisRules"
              label-width="0"
              @submit.prevent="handleAnalysis"
            >
              <el-form-item prop="text">
                <el-input
                  v-model="analysisForm.text"
                  type="textarea"
                  :rows="8"
                  placeholder="Введите текст для анализа..."
                  :disabled="loading"
                  show-word-limit
                  :maxlength="5000"
                />
              </el-form-item>

              <el-form-item prop="analysisType">
                <el-select
                  v-model="analysisForm.analysisType"
                  placeholder="Выберите тип анализа"
                  :disabled="loading"
                  style="width: 100%"
                >
                  <el-option
                    value="sentiment"
                    label="Анализ тональности"
                  >
                    <div class="option-content">
                      <el-icon><ChatDotRound /></el-icon>
                      <span>Анализ тональности</span>
                    </div>
                  </el-option>
                  <el-option
                    value="summary"
                    label="Краткая выжимка"
                  >
                    <div class="option-content">
                      <el-icon><Document /></el-icon>
                      <span>Краткая выжимка</span>
                    </div>
                  </el-option>
                  <el-option
                    value="keywords"
                    label="Ключевые слова"
                  >
                    <div class="option-content">
                      <el-icon><Key /></el-icon>
                      <span>Ключевые слова</span>
                    </div>
                  </el-option>
                </el-select>
              </el-form-item>

              <el-form-item>
                <el-button
                  type="primary"
                  :loading="loading"
                  @click="handleAnalysis"
                  :disabled="!analysisForm.text || !analysisForm.analysisType"
                  size="large"
                  style="width: 100%"
                >
                  <el-icon v-if="!loading"><Magic /></el-icon>
                  <span v-if="!loading">Анализировать</span>
                  <span v-else>Анализирую...</span>
                </el-button>
              </el-form-item>
            </el-form>

            <!-- Быстрые примеры -->
            <div class="quick-examples">
              <h4>Быстрые примеры:</h4>
              <div class="examples-list">
                <el-tag
                  v-for="example in quickExamples"
                  :key="example.text"
                  @click="setExample(example)"
                  class="example-tag"
                  type="info"
                >
                  {{ example.label }}
                </el-tag>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- Результат анализа -->
        <el-col :xs="24" :lg="12">
          <el-card class="result-card" shadow="always">
            <template #header>
              <div class="card-header">
                <el-icon><DataAnalysis /></el-icon>
                <span>Результат анализа</span>
              </div>
            </template>

            <div v-if="loading" class="loading-state">
              <el-icon class="is-loading loading-icon"><Loading /></el-icon>
              <p>Анализирую текст с помощью ИИ...</p>
              <el-progress :percentage="progress" :show-text="false" />
            </div>

            <div v-else-if="currentAnalysis" class="analysis-result">
              <div class="result-header">
                <el-tag 
                  :type="getAnalysisTypeColor(currentAnalysis.analysis_type)"
                  size="large"
                >
                  {{ getAnalysisTypeName(currentAnalysis.analysis_type) }}
                </el-tag>
                <div class="result-meta">
                  <span v-if="currentAnalysis.confidence_score" class="confidence">
                    Уверенность: {{ currentAnalysis.confidence_score }}
                  </span>
                  <span v-if="currentAnalysis.processing_time" class="processing-time">
                    {{ currentAnalysis.processing_time }}
                  </span>
                </div>
              </div>

              <div class="original-text">
                <h4>Исходный текст:</h4>
                <div class="text-content">
                  {{ currentAnalysis.original_text }}
                </div>
              </div>

              <div class="analysis-output">
                <h4>Результат:</h4>
                <div class="result-content">
                  {{ currentAnalysis.result }}
                </div>
              </div>

              <div class="result-actions">
                <el-button @click="copyResult" size="small">
                  <el-icon><CopyDocument /></el-icon>
                  Копировать
                </el-button>
                <el-button @click="saveAnalysis" type="primary" size="small">
                  <el-icon><Check /></el-icon>
                  Сохранено
                </el-button>
              </div>
            </div>

            <div v-else-if="error" class="error-state">
              <el-icon class="error-icon"><Warning /></el-icon>
              <p>{{ error }}</p>
              <el-button @click="clearError" type="primary">Попробовать снова</el-button>
            </div>

            <div v-else class="empty-state">
              <el-icon class="empty-icon"><Magic /></el-icon>
              <p>Введите текст и выберите тип анализа</p>
              <p class="empty-subtitle">Результат появится здесь</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import {
  EditPen,
  DataAnalysis,
  ChatDotRound,
  Document,
  Key,
  Magic,
  Loading,
  CopyDocument,
  Check,
  Warning
} from '@element-plus/icons-vue'

export default {
  name: 'AnalysisView',
  components: {
    EditPen,
    DataAnalysis,
    ChatDotRound,
    Document,
    Key,
    Magic,
    Loading,
    CopyDocument,
    Check,
    Warning
  },
  setup() {
    const store = useStore()
    const analysisFormRef = ref()
    const progress = ref(0)

    const analysisForm = ref({
      text: '',
      analysisType: ''
    })

    const analysisRules = {
      text: [
        { required: true, message: 'Введите текст для анализа', trigger: 'blur' },
        { min: 10, message: 'Текст должен содержать минимум 10 символов', trigger: 'blur' }
      ],
      analysisType: [
        { required: true, message: 'Выберите тип анализа', trigger: 'change' }
      ]
    }

    const quickExamples = [
      {
        label: 'Позитивный отзыв',
        text: 'Отличный продукт! Очень доволен покупкой. Рекомендую всем друзьям.',
        type: 'sentiment'
      },
      {
        label: 'Новостная статья',
        text: 'Сегодня в городе прошла важная конференция по вопросам экологии. Участники обсудили актуальные проблемы загрязнения окружающей среды и предложили конкретные решения.',
        type: 'summary'
      },
      {
        label: 'Техническое описание',
        text: 'Искусственный интеллект представляет собой область компьютерных наук, которая занимается созданием интеллектуальных машин, способных работать и реагировать как люди.',
        type: 'keywords'
      }
    ]

    const loading = computed(() => store.getters['analysis/loading'])
    const error = computed(() => store.getters['analysis/error'])
    const currentAnalysis = computed(() => store.getters['analysis/currentAnalysis'])

    const getAnalysisTypeName = (type) => {
      const names = {
        sentiment: 'Анализ тональности',
        summary: 'Краткая выжимка',
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

    const setExample = (example) => {
      analysisForm.value.text = example.text
      analysisForm.value.analysisType = example.type
    }

    const handleAnalysis = async () => {
      if (!analysisFormRef.value) return

      try {
        const valid = await analysisFormRef.value.validate()
        if (!valid) return

        // Запускаем прогресс-бар
        progress.value = 0
        const progressInterval = setInterval(() => {
          if (progress.value < 90) {
            progress.value += Math.random() * 20
          }
        }, 200)

        const result = await store.dispatch('analysis/createAnalysis', {
          text: analysisForm.value.text,
          analysisType: analysisForm.value.analysisType
        })

        clearInterval(progressInterval)
        progress.value = 100

        if (result.success) {
          ElMessage.success('Анализ успешно выполнен!')
        } else {
          ElMessage.error(result.message || 'Ошибка при анализе')
        }
      } catch (error) {
        console.error('Ошибка при анализе:', error)
      }
    }

    const copyResult = async () => {
      if (!currentAnalysis.value) return

      try {
        await navigator.clipboard.writeText(currentAnalysis.value.result)
        ElMessage.success('Результат скопирован в буфер обмена')
      } catch (error) {
        ElMessage.error('Не удалось скопировать результат')
      }
    }

    const saveAnalysis = () => {
      ElMessage.success('Анализ уже сохранен в истории')
    }

    const clearError = () => {
      store.dispatch('analysis/clearError')
    }

    // Очищаем текущий анализ при изменении формы
    watch(() => [analysisForm.value.text, analysisForm.value.analysisType], () => {
      if (currentAnalysis.value) {
        store.dispatch('analysis/clearCurrentAnalysis')
      }
    })

    return {
      analysisForm,
      analysisRules,
      analysisFormRef,
      quickExamples,
      loading,
      error,
      currentAnalysis,
      progress,
      getAnalysisTypeName,
      getAnalysisTypeColor,
      setExample,
      handleAnalysis,
      copyResult,
      saveAnalysis,
      clearError
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

.analysis-form-card,
.result-card {
  height: fit-content;
}

.option-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.quick-examples {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.quick-examples h4 {
  margin: 0 0 15px 0;
  color: #666;
  font-size: 0.9rem;
}

.examples-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.example-tag {
  cursor: pointer;
  transition: all 0.3s ease;
}

.example-tag:hover {
  background-color: #667eea;
  color: white;
}

.loading-state {
  text-align: center;
  padding: 40px 20px;
}

.loading-icon {
  font-size: 48px;
  color: #667eea;
  margin-bottom: 20px;
}

.loading-state p {
  margin-bottom: 20px;
  color: #666;
}

.analysis-result {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.result-meta {
  display: flex;
  gap: 15px;
  font-size: 0.85rem;
  color: #999;
}

.original-text,
.analysis-output {
  margin-bottom: 20px;
}

.original-text h4,
.analysis-output h4 {
  margin: 0 0 10px 0;
  color: #2c3e50;
  font-size: 1rem;
}

.text-content {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #e9ecef;
  font-size: 0.9rem;
  line-height: 1.5;
  color: #555;
}

.result-content {
  background: #f0f9ff;
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  line-height: 1.6;
  color: #2c3e50;
}

.result-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.error-state,
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.error-icon,
.empty-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.error-icon {
  color: #f56565;
}

.empty-icon {
  color: #cbd5e0;
}

.error-state p,
.empty-state p {
  margin-bottom: 10px;
  color: #666;
}

.empty-subtitle {
  font-size: 0.9rem;
  color: #999 !important;
}

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 2rem;
  }
  
  .result-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .result-actions {
    justify-content: center;
  }
  
  .examples-list {
    justify-content: center;
  }
}
</style>
