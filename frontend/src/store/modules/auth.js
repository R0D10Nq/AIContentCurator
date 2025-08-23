import axios from 'axios'

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api'

const state = {
  token: localStorage.getItem('token') || null,
  user: JSON.parse(localStorage.getItem('user')) || null,
  loading: false,
  error: null
}

const getters = {
  isAuthenticated: state => !!state.token,
  currentUser: state => state.user,
  loading: state => state.loading,
  error: state => state.error
}

const mutations = {
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  },
  SET_TOKEN(state, token) {
    state.token = token
    if (token) {
      localStorage.setItem('token', token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    } else {
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    }
  },
  SET_USER(state, user) {
    state.user = user
    if (user) {
      localStorage.setItem('user', JSON.stringify(user))
    } else {
      localStorage.removeItem('user')
    }
  },
  CLEAR_AUTH(state) {
    state.token = null
    state.user = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    delete axios.defaults.headers.common['Authorization']
  }
}

const actions = {
  async login({ commit }, credentials) {
    try {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)

      const formData = new FormData()
      formData.append('username', credentials.username)
      formData.append('password', credentials.password)

      const response = await axios.post(`${API_URL}/auth/token`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      const { access_token } = response.data
      commit('SET_TOKEN', access_token)

      // Получаем информацию о пользователе
      const userResponse = await axios.get(`${API_URL}/auth/me`)
      commit('SET_USER', userResponse.data)

      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Ошибка при входе'
      commit('SET_ERROR', message)
      return { success: false, message }
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async register({ commit }, userData) {
    try {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)

      await axios.post(`${API_URL}/auth/register`, userData)
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Ошибка при регистрации'
      commit('SET_ERROR', message)
      return { success: false, message }
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async checkAuth({ commit, state }) {
    if (state.token) {
      try {
        axios.defaults.headers.common['Authorization'] = `Bearer ${state.token}`
        const response = await axios.get(`${API_URL}/auth/me`)
        commit('SET_USER', response.data)
      } catch (error) {
        commit('CLEAR_AUTH')
      }
    }
  },

  logout({ commit }) {
    commit('CLEAR_AUTH')
  },

  clearError({ commit }) {
    commit('SET_ERROR', null)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
