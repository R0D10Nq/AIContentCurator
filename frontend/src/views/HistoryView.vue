<template>
  <div class="history-page">
    <div class="page-container">
      <!-- Заголовок -->
      <div class="page-header">
        <h1>История анализов</h1>
        <p>Просматривайте и управляйте всеми вашими анализами</p>
      </div>

      <!-- Фильтры -->
      <el-card class="filters-card mb-20" shadow="never">
        <el-row :gutter="20" align="middle">
          <el-col :xs="24" :sm="8">
            <el-select
              v-model="filters.analysisType"
              placeholder="Тип анализа"
              clearable
              @change="handleFilterChange"
              style="width: 100%"
            >
              <el-option value="sentiment" label="Анализ тональности" />
              <el-option value="summary" label="Краткая выжимка" />
              <el-option value="keywords" label="Ключевые слова" />
            </el-select>
          </el-col>
          <el-col :xs="24" :sm="8">
            <el-input
              v-model="filters.search"
              placeholder="Поиск по тексту..."
              prefix-icon="Search"
              clearable
              @input="handleSearchChange"
            />
          </el-col>
          <el-col :xs="24" :sm="8">
            <div class="filter-actions">
              <el-button @click="clearFilters">Очистить</el-button>
              <el-button type="primary" @click="exportAnalyses">
                <el-icon><Download /></el-icon>
                Экспорт
              </el-button>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- Статистика -->
      <el-row :gutter="20" class="mb-20">
        <el-col :xs="24" :sm="6">
          <el-statistic
            title="Всего анализов"
            :value="stats.total"
            class="stat-item"
          />
        </el-col>
        <el-col :xs="24" :sm="6">
          <el-statistic
            title="Анализ тональности"
            :value="stats.sentiment"
            class="stat-item"
          />
        </el-col>
        <el-col :xs="24" :sm="6">
          <el-statistic
            title="Выжимки"
            :value="stats.summary"
            class="stat-item"
          />
        </el-col>
        <el-col :xs="24" :sm="6">
          <el-statistic
            title="Ключевые слова"
            :value="stats.keywords"
            class="stat-item"
          />
        </el-col>
      </el-row>

      <!-- Список анализов -->
      <div v-if="loading" class="loading-state">
        <el-skeleton :rows="5" animated />
      </div>

      <div v-else-if="filteredAnalyses.length === 0" class="empty-state">
        <el-empty description="Анализы не найдены">
          <el-button type="primary" @click="$router.push('/analysis')">
            Создать анализ
          </el-button>
        </el-empty>
      </div>

      <div v-else class="analyses-grid">
        <el-card
          v-for="analysis in paginatedAnalyses"
          :key="analysis.id"
          class="analysis-card"
          shadow="hover"
        >
          <template #header>
            <div class="analysis-card-header">
              <el-tag 
                :type="getAnalysisTypeColor(analysis.analysis_type)"
                size="small"
              >
                {{ getAnalysisTypeName(analysis.analysis_type) }}
              </el-tag>
              <div class="card-actions">
                <el-button
                  type="text"
                  size="small"
                  @click="viewAnalysis(analysis)"
                >
                  <el-icon><View /></el-icon>
                </el-button>
                <el-button
                  type="text"
                  size="small"
                  @click="copyAnalysis(analysis)"
                >
                  <el-icon><CopyDocument /></el-icon>
                </el-button>
                <el-popconfirm
                  title="Удалить этот анализ?"
                  @confirm="deleteAnalysis(analysis.id)"
                >
                  <template #reference>
                    <el-button
                      type="text"
                      size="small"
                      class="delete-btn"
                    >
                      <el-icon><Delete /></el-icon>
                    </el-button>
                  </template>
                </el-popconfirm>
              </div>
            </div>
          </template>

          <div class="analysis-content">
            <div class="original-text">
              <h4>Исходный текст:</h4>
              <p>{{ truncateText(analysis.original_text, 120) }}</p>
            </div>

            <div class="analysis-result">
              <h4>Результат:</h4>
              <p>{{ truncateText(analysis.result, 150) }}</p>
            </div>

            <div class="analysis-meta">
              <div class="meta-item">
                <el-icon><Clock /></el-icon>
                <span>{{ formatDate(analysis.created_at) }}</span>
              </div>
              <div v-if="analysis.confidence_score" class="meta-item">
                <el-icon><TrendCharts /></el-icon>
                <span>{{ analysis.confidence_score }}</span>
              </div>
              <div v-if="analysis.processing_time" class="meta-item">
                <el-icon><Timer /></el-icon>
                <span>{{ analysis.processing_time }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </div>

      <!-- Пагинация -->
      <div v-if="filteredAnalyses.length > pageSize" class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="filteredAnalyses.length"
          layout="prev, pager, next, jumper"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- Диалог просмотра анализа -->
    <el-dialog
      v-model="viewDialogVisible"
      :title="selectedAnalysis ? getAnalysisTypeName(selectedAnalysis.analysis_type) : ''"
      width="70%"
      top="5vh"
    >
      <div v-if="selectedAnalysis" class="analysis-detail">
        <div class="detail-section">
          <h3>Исходный текст</h3>
          <div class="text-content">
            {{ selectedAnalysis.original_text }}
          </div>
        </div>

        <div class="detail-section">
          <h3>Результат анализа</h3>
          <div class="result-content">
            {{ selectedAnalysis.result }}
          </div>
        </div>

        <div class="detail-meta">
          <div class="meta-grid">
            <div class="meta-item">
              <strong>Тип анализа:</strong>
              <el-tag :type="getAnalysisTypeColor(selectedAnalysis.analysis_type)">
                {{ getAnalysisTypeName(selectedAnalysis.analysis_type) }}
              </el-tag>
            </div>
            <div class="meta-item">
              <strong>Дата создания:</strong>
              <span>{{ formatDate(selectedAnalysis.created_at) }}</span>
            </div>
            <div v-if="selectedAnalysis.confidence_score" class="meta-item">
              <strong>Уверенность:</strong>
              <span>{{ selectedAnalysis.confidence_score }}</span>
            </div>
            <div v-if="selectedAnalysis.processing_time" class="meta-item">
              <strong>Время обработки:</strong>
              <span>{{ selectedAnalysis.processing_time }}</span>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="viewDialogVisible = false">Закрыть</el-button>
          <el-button type="primary" @click="copyAnalysisResult">
            <el-icon><CopyDocument /></el-icon>
            Копировать результат
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import {
  Download,
  View,
  CopyDocument,
  Delete,
  Clock,
  TrendCharts,
  Timer,
  Search
} from '@element-plus/icons-vue'

export default {
  name: 'HistoryView',
  components: {
    Download,
    View,
    CopyDocument,
    Delete,
    Clock,
    TrendCharts,
    Timer,
    Search
  },
  setup() {
    const store = useStore()
    
    const filters = ref({
      analysisType: '',
      search: ''
    })
    
    const currentPage = ref(1)
    const pageSize = ref(12)
    const viewDialogVisible = ref(false)
    const selectedAnalysis = ref(null)
    const searchTimeout = ref(null)

    const loading = computed(() => store.getters['analysis/loading'])
    const analyses = computed(() => store.getters['analysis/analyses'])
    const stats = computed(() => store.getters['analysis/stats'])

    const filteredAnalyses = computed(() => {
      let result = [...analyses.value]

      if (filters.value.analysisType) {
        result = result.filter(a => a.analysis_type === filters.value.analysisType)
      }

      if (filters.value.search) {
        const searchTerm = filters.value.search.toLowerCase()
        result = result.filter(a => 
          a.original_text.toLowerCase().includes(searchTerm) ||
          a.result.toLowerCase().includes(searchTerm)
        )
      }

      return result
    })

    const paginatedAnalyses = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      return filteredAnalyses.value.slice(start, end)
    })

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

    const handleFilterChange = () => {
      currentPage.value = 1
    }

    const handleSearchChange = () => {
      if (searchTimeout.value) {
        clearTimeout(searchTimeout.value)
      }
      
      searchTimeout.value = setTimeout(() => {
        currentPage.value = 1
      }, 300)
    }

    const clearFilters = () => {
      filters.value.analysisType = ''
      filters.value.search = ''
      currentPage.value = 1
    }

    const handlePageChange = (page) => {
      currentPage.value = page
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    const viewAnalysis = (analysis) => {
      selectedAnalysis.value = analysis
      viewDialogVisible.value = true
    }

    const copyAnalysis = async (analysis) => {
      try {
        const text = `Тип: ${getAnalysisTypeName(analysis.analysis_type)}\n\nИсходный текст:\n${analysis.original_text}\n\nРезультат:\n${analysis.result}`
        await navigator.clipboard.writeText(text)
        ElMessage.success('Анализ скопирован в буфер обмена')
      } catch (error) {
        ElMessage.error('Не удалось скопировать анализ')
      }
    }

    const copyAnalysisResult = async () => {
      if (!selectedAnalysis.value) return
      
      try {
        await navigator.clipboard.writeText(selectedAnalysis.value.result)
        ElMessage.success('Результат скопирован в буфер обмена')
      } catch (error) {
        ElMessage.error('Не удалось скопировать результат')
      }
    }

    const deleteAnalysis = async (analysisId) => {
      const result = await store.dispatch('analysis/deleteAnalysis', analysisId)
      
      if (result.success) {
        ElMessage.success('Анализ удален')
      } else {
        ElMessage.error(result.message || 'Ошибка при удалении')
      }
    }

    const exportAnalyses = () => {
      try {
        const data = filteredAnalyses.value.map(analysis => ({
          id: analysis.id,
          type: getAnalysisTypeName(analysis.analysis_type),
          original_text: analysis.original_text,
          result: analysis.result,
          confidence: analysis.confidence_score,
          processing_time: analysis.processing_time,
          created_at: formatDate(analysis.created_at)
        }))

        const json = JSON.stringify(data, null, 2)
        const blob = new Blob([json], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        
        const link = document.createElement('a')
        link.href = url
        link.download = `analyses_${new Date().toISOString().split('T')[0]}.json`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        URL.revokeObjectURL(url)

        ElMessage.success('Анализы экспортированы')
      } catch (error) {
        ElMessage.error('Ошибка при экспорте')
      }
    }

    onMounted(() => {
      store.dispatch('analysis/fetchAnalyses', { limit: 100 })
    })

    return {
      filters,
      currentPage,
      pageSize,
      viewDialogVisible,
      selectedAnalysis,
      loading,
      filteredAnalyses,
      paginatedAnalyses,
      stats,
      getAnalysisTypeName,
      getAnalysisTypeColor,
      formatDate,
      truncateText,
      handleFilterChange,
      handleSearchChange,
      clearFilters,
      handlePageChange,
      viewAnalysis,
      copyAnalysis,
      copyAnalysisResult,
      deleteAnalysis,
      exportAnalyses
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

.filters-card {
  border: 1px solid #e4e7ed;
}

.filter-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.loading-state {
  padding: 20px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.analyses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.analysis-card {
  height: fit-content;
  transition: transform 0.2s ease;
}

.analysis-card:hover {
  transform: translateY(-2px);
}

.analysis-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-actions {
  display: flex;
  gap: 5px;
}

.delete-btn {
  color: #f56565;
}

.delete-btn:hover {
  color: #e53e3e;
}

.analysis-content h4 {
  margin: 0 0 8px 0;
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
}

.analysis-content p {
  margin: 0 0 15px 0;
  line-height: 1.5;
  color: #2c3e50;
}

.original-text {
  margin-bottom: 15px;
}

.original-text p {
  background: #f8f9fa;
  padding: 10px;
  border-radius: 6px;
  font-size: 0.85rem;
  color: #555;
}

.analysis-result p {
  background: #f0f9ff;
  padding: 10px;
  border-radius: 6px;
  border-left: 3px solid #667eea;
}

.analysis-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
  font-size: 0.8rem;
  color: #999;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.analysis-detail {
  max-height: 70vh;
  overflow-y: auto;
}

.detail-section {
  margin-bottom: 30px;
}

.detail-section h3 {
  margin: 0 0 15px 0;
  color: #2c3e50;
  font-size: 1.1rem;
}

.text-content {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  line-height: 1.6;
  color: #555;
}

.result-content {
  background: #f0f9ff;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  line-height: 1.6;
  color: #2c3e50;
}

.detail-meta {
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.meta-grid .meta-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 2rem;
  }
  
  .analyses-grid {
    grid-template-columns: 1fr;
  }
  
  .filter-actions {
    justify-content: center;
    margin-top: 10px;
  }
  
  .analysis-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .meta-grid {
    grid-template-columns: 1fr;
  }
}
</style>
