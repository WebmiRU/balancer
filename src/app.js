// import Vue from 'vue';
// //import Alert from './Alert.vue';
//
// new Vue({
//     el: '#app',
// //    components: { Alert }
// });

import {createApp} from 'vue'
import Alert from './Alert'


createApp({
    components: {
        Alert,
    }
}).mount('#app')