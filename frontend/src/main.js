import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
import VueAxios from 'vue-axios'

import App from './App.vue'
import router from './router'

Vue.config.productionTip = false

Vue.use(ElementUI)
Vue.use(VueAxios, axios)

new Vue({
  router,
  render: h => h(App),
  el: '#app',
  template: '<App/>',
  components: { App }
}).$mount('#app')
