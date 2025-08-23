<template>
  <div class="home">
    <!-- Главный баннер -->
    <section class="hero-section">
      <div class="page-container">
        <div class="hero-content">
          <h1 class="hero-title">
            <span class="text-gradient">AI Content Curator</span>
          </h1>
          <p class="hero-subtitle">
            Анализируй контент с помощью искусственного интеллекта
          </p>
          <p class="hero-description">
            Получай анализ тональности, краткие выжимки и ключевые слова из любого текста 
            с помощью передовых технологий Gemini AI
          </p>
          <div class="hero-actions">
            <el-button 
              type="primary" 
              size="large" 
              @click="handleGetStarted"
              class="cta-button"
            >
              <el-icon><Promotion /></el-icon>
              Начать анализ
            </el-button>
            <el-button 
              size="large" 
              @click="scrollToFeatures"
              class="learn-more-button"
            >
              Узнать больше
            </el-button>
          </div>
        </div>
        <div class="hero-image">
          <div class="floating-cards">
            <div class="demo-card sentiment">
              <el-icon class="card-icon"><ChatDotRound /></el-icon>
              <span>Анализ тональности</span>
            </div>
            <div class="demo-card summary">
              <el-icon class="card-icon"><Document /></el-icon>
              <span>Краткие выжимки</span>
            </div>
            <div class="demo-card keywords">
              <el-icon class="card-icon"><Key /></el-icon>
              <span>Ключевые слова</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Функции -->
    <section class="features-section" ref="featuresSection">
      <div class="page-container">
        <h2 class="section-title">Возможности платформы</h2>
        <div class="features-grid">
          <el-card class="feature-card" shadow="hover">
            <template #header>
              <div class="feature-header">
                <el-icon class="feature-icon sentiment-color"><ChatDotRound /></el-icon>
                <h3>Анализ тональности</h3>
              </div>
            </template>
            <p>Определяй эмоциональную окраску текста: позитивная, негативная или нейтральная тональность с оценкой уверенности.</p>
          </el-card>

          <el-card class="feature-card" shadow="hover">
            <template #header>
              <div class="feature-header">
                <el-icon class="feature-icon summary-color"><Document /></el-icon>
                <h3>Краткие выжимки</h3>
              </div>
            </template>
            <p>Получай сжатые версии больших текстов, сохраняя все ключевые моменты и основные идеи.</p>
          </el-card>

          <el-card class="feature-card" shadow="hover">
            <template #header>
              <div class="feature-header">
                <el-icon class="feature-icon keywords-color"><Key /></el-icon>
                <h3>Ключевые слова</h3>
              </div>
            </template>
            <p>Извлекай наиболее важные термины и темы, которые отражают суть анализируемого контента.</p>
          </el-card>

          <el-card class="feature-card" shadow="hover">
            <template #header>
              <div class="feature-header">
                <el-icon class="feature-icon telegram-color"><ChatLineRound /></el-icon>
                <h3>Telegram бот</h3>
              </div>
            </template>
            <p>Анализируй тексты прямо из Telegram без необходимости заходить на сайт. Быстро и удобно.</p>
          </el-card>

          <el-card class="feature-card" shadow="hover">
            <template #header>
              <div class="feature-header">
                <el-icon class="feature-icon history-color"><Clock /></el-icon>
                <h3>История анализов</h3>
              </div>
            </template>
            <p>Сохраняй все свои анализы и возвращайся к ним в любое время. Экспортируй результаты.</p>
          </el-card>

          <el-card class="feature-card" shadow="hover">
            <template #header>
              <div class="feature-header">
                <el-icon class="feature-icon api-color"><Connection /></el-icon>
                <h3>API доступ</h3>
              </div>
            </template>
            <p>Интегрируй анализ контента в свои приложения через простой и понятный REST API.</p>
          </el-card>
        </div>
      </div>
    </section>

    <!-- Статистика -->
    <section class="stats-section">
      <div class="page-container">
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-number">1000+</div>
            <div class="stat-label">Анализов выполнено</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">99%</div>
            <div class="stat-label">Точность анализа</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">< 2с</div>
            <div class="stat-label">Время обработки</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Доступность</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA секция -->
    <section class="cta-section">
      <div class="page-container">
        <div class="cta-content">
          <h2>Готов начать анализировать контент?</h2>
          <p>Присоединяйся к сообществу пользователей, которые уже используют ИИ для анализа текстов</p>
          <div class="cta-actions">
            <el-button 
              type="primary" 
              size="large" 
              @click="handleGetStarted"
              class="cta-button"
            >
              Начать бесплатно
            </el-button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { 
  Promotion, 
  ChatDotRound, 
  Document, 
  Key, 
  ChatLineRound, 
  Clock, 
  Connection 
} from '@element-plus/icons-vue'

export default {
  name: 'HomeView',
  components: {
    Promotion,
    ChatDotRound,
    Document,
    Key,
    ChatLineRound,
    Clock,
    Connection
  },
  setup() {
    const store = useStore()
    const router = useRouter()

    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated'])

    const handleGetStarted = () => {
      if (isAuthenticated.value) {
        router.push('/analysis')
      } else {
        router.push('/register')
      }
    }

    const scrollToFeatures = () => {
      const element = document.querySelector('.features-section')
      element?.scrollIntoView({ behavior: 'smooth' })
    }

    return {
      handleGetStarted,
      scrollToFeatures
    }
  }
}
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 0;
  min-height: 70vh;
  display: flex;
  align-items: center;
}

.hero-content {
  flex: 1;
  max-width: 600px;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: bold;
  margin-bottom: 20px;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 20px;
  opacity: 0.9;
}

.hero-description {
  font-size: 1.1rem;
  margin-bottom: 40px;
  opacity: 0.8;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.cta-button {
  background: rgba(255, 255, 255, 0.2) !important;
  border: 2px solid white !important;
  color: white !important;
  backdrop-filter: blur(10px);
}

.cta-button:hover {
  background: white !important;
  color: #667eea !important;
}

.learn-more-button {
  background: transparent !important;
  border: 2px solid rgba(255, 255, 255, 0.5) !important;
  color: white !important;
}

.learn-more-button:hover {
  border-color: white !important;
  background: rgba(255, 255, 255, 0.1) !important;
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.floating-cards {
  position: relative;
  width: 300px;
  height: 300px;
}

.demo-card {
  position: absolute;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: white;
  font-weight: 500;
  animation: float 6s ease-in-out infinite;
}

.demo-card.sentiment {
  top: 20px;
  left: 20px;
  animation-delay: 0s;
}

.demo-card.summary {
  top: 120px;
  right: 20px;
  animation-delay: 2s;
}

.demo-card.keywords {
  bottom: 20px;
  left: 50px;
  animation-delay: 4s;
}

.card-icon {
  font-size: 20px;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

.features-section {
  padding: 80px 0;
  background: white;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 60px;
  color: #2c3e50;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
}

.feature-card {
  height: 100%;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-header {
  display: flex;
  align-items: center;
  gap: 15px;
}

.feature-icon {
  font-size: 24px;
}

.sentiment-color { color: #52c41a; }
.summary-color { color: #1890ff; }
.keywords-color { color: #fa8c16; }
.telegram-color { color: #0088cc; }
.history-color { color: #722ed1; }
.api-color { color: #eb2f96; }

.stats-section {
  background: #f8f9fa;
  padding: 60px 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
  text-align: center;
}

.stat-number {
  font-size: 3rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 1.1rem;
  color: #666;
}

.cta-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 0;
  text-align: center;
}

.cta-content h2 {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.cta-content p {
  font-size: 1.2rem;
  margin-bottom: 40px;
  opacity: 0.9;
}

@media (max-width: 768px) {
  .hero-section {
    padding: 40px 0;
    text-align: center;
  }
  
  .hero-content {
    max-width: 100%;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-image {
    display: none;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
