import { createStore } from 'vuex'
import auth from './modules/auth'
import analysis from './modules/analysis'

export default createStore({
  modules: {
    auth,
    analysis
  }
})
