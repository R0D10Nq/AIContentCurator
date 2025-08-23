<template>
  <div class="not-found-page">
    <div class="not-found-container">
      <div class="not-found-content">
        <div class="error-code">404</div>
        <h1>Страница не найдена</h1>
        <p>Извините, но запрашиваемая страница не существует или была перемещена.</p>
        
        <div class="error-actions">
          <el-button type="primary" size="large" @click="$router.push('/')">
            <el-icon><House /></el-icon>
            На главную
          </el-button>
          <el-button size="large" @click="$router.go(-1)">
            <el-icon><Back /></el-icon>
            Назад
          </el-button>
        </div>
      </div>
      
      <div class="error-illustration">
        <el-icon class="illustration-icon"><QuestionFilled /></el-icon>
      </div>
    </div>
  </div>
</template>

<script>
import { House, Back, QuestionFilled } from '@element-plus/icons-vue'

export default {
  name: 'NotFoundView',
  components: {
    House,
    Back,
    QuestionFilled
  }
}
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.not-found-container {
  display: flex;
  align-items: center;
  gap: 60px;
  max-width: 800px;
  padding: 40px;
}

.not-found-content {
  flex: 1;
}

.error-code {
  font-size: 8rem;
  font-weight: bold;
  line-height: 1;
  margin-bottom: 20px;
  opacity: 0.8;
}

.not-found-content h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
  font-weight: 600;
}

.not-found-content p {
  font-size: 1.2rem;
  margin-bottom: 40px;
  opacity: 0.9;
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.error-actions .el-button {
  background: rgba(255, 255, 255, 0.2) !important;
  border: 2px solid rgba(255, 255, 255, 0.5) !important;
  color: white !important;
  backdrop-filter: blur(10px);
}

.error-actions .el-button:hover {
  background: rgba(255, 255, 255, 0.3) !important;
  border-color: white !important;
}

.error-actions .el-button--primary {
  background: rgba(255, 255, 255, 0.2) !important;
  border-color: white !important;
}

.error-actions .el-button--primary:hover {
  background: white !important;
  color: #667eea !important;
}

.error-illustration {
  flex: 1;
  text-align: center;
}

.illustration-icon {
  font-size: 12rem;
  opacity: 0.3;
}

@media (max-width: 768px) {
  .not-found-container {
    flex-direction: column;
    text-align: center;
    gap: 40px;
    padding: 20px;
  }
  
  .error-code {
    font-size: 6rem;
  }
  
  .not-found-content h1 {
    font-size: 2rem;
  }
  
  .not-found-content p {
    font-size: 1rem;
  }
  
  .illustration-icon {
    font-size: 8rem;
  }
  
  .error-actions {
    justify-content: center;
  }
}
</style>
