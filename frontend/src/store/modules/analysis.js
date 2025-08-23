import axios from 'axios'

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api'

const state = {
  analyses: [],
  currentAnalysis: null,
  loading: false,
  error: null,
  stats: {
    total: 0,
    sentiment: 0,
    summary: 0,
    keywords: 0
  }
}

const getters = {
  analyses: state => state.analyses,
  currentAnalysis: state => state.currentAnalysis,
  loading: state => state.loading,
  error: state => state.error,
  stats: state => state.stats
}

const mutations = {
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  },
  SET_ANALYSES(state, { analyses, total }) {
    state.analyses = analyses
    state.stats.total = total
  },
  ADD_ANALYSIS(state, analysis) {
    state.analyses.unshift(analysis)
    state.stats.total += 1
    state.stats[analysis.analysis_type] += 1
  },
  SET_CURRENT_ANALYSIS(state, analysis) {
    state.currentAnalysis = analysis
  },
  REMOVE_ANALYSIS(state, analysisId) {
    const index = state.analyses.findIndex(a => a.id === analysisId)
    if (index !== -1) {
      const analysis = state.analyses[index]
      state.analyses.splice(index, 1)
      state.stats.total -= 1
      state.stats[analysis.analysis_type] -= 1
    }
  },
  UPDATE_STATS(state, stats) {
    state.stats = { ...state.stats, ...stats }
  }
}

const actions = {
  async createAnalysis({ commit }, { text, analysisType }) {
    try {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)

      const response = await axios.post(`${API_URL}/analysis/`, {
        text,
        analysis_type: analysisType
      })

      const analysis = response.data
      commit('ADD_ANALYSIS', analysis)
      commit('SET_CURRENT_ANALYSIS', analysis)

      return { success: true, analysis }
    } catch (error) {
      const message = error.response?.data?.detail || 'Ошибка при анализе текста'
      commit('SET_ERROR', message)
      return { success: false, message }
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async fetchAnalyses({ commit }, { skip = 0, limit = 20, analysisType = null } = {}) {
    try {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)

      const params = { skip, limit }
      if (analysisType) {
        params.analysis_type = analysisType
      }

      const response = await axios.get(`${API_URL}/analysis/`, { params })
      commit('SET_ANALYSES', response.data)

      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Ошибка при загрузке анализов'
      commit('SET_ERROR', message)
      return { success: false, message }
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async fetchAnalysis({ commit }, analysisId) {
    try {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)

      const response = await axios.get(`${API_URL}/analysis/${analysisId}`)
      commit('SET_CURRENT_ANALYSIS', response.data)

      return { success: true, analysis: response.data }
    } catch (error) {
      const message = error.response?.data?.detail || 'Ошибка при загрузке анализа'
      commit('SET_ERROR', message)
      return { success: false, message }
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async deleteAnalysis({ commit }, analysisId) {
    try {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)

      await axios.delete(`${API_URL}/analysis/${analysisId}`)
      commit('REMOVE_ANALYSIS', analysisId)

      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Ошибка при удалении анализа'
      commit('SET_ERROR', message)
      return { success: false, message }
    } finally {
      commit('SET_LOADING', false)
    }
  },

  clearError({ commit }) {
    commit('SET_ERROR', null)
  },

  clearCurrentAnalysis({ commit }) {
    commit('SET_CURRENT_ANALYSIS', null)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
