import { createApp } from 'vue'
import { Quasar } from 'quasar'
import App from './App.vue'
// import App from './AppResearch.vue'
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'
import './index.css'

import SmartTable from 'vuejs-smart-table'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import { aliases, mdi } from 'vuetify/iconsets/mdi'
import { fa } from 'vuetify/iconsets/fa'
import '@mdi/font/css/materialdesignicons.css'
import '@fortawesome/fontawesome-free/css/all.css'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'dark'
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
      fa
    }
  }
})

createApp(App).use(Quasar, { plugins: {} }).use(vuetify).use(SmartTable).mount('#app')
