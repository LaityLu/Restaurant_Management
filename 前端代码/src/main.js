import Vue from "vue";
import App from "./App.vue";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import router from "./router";
import Cookies from "js-cookie";
import store from "./store"
import "./api/mock"

Vue.config.productionTip = false;

//全局引入E-UI
Vue.use(ElementUI);
//添加全局前置导航守卫 
router.beforeEach((to, from, next) => {
  //判断 token 存不存在
  const token = Cookies.get('token')
  const radio = Cookies.get('radio')
  if(!token && to.name !== 'login' && to.name !== 'register'){//用户未登录,跳转至登录界面，并防止死循环
    next({name:'login'})
  }else if(token && (to.name === 'login'|| to.name === 'register')){//用户已登录，将跳转至首页
    next({name:'home'})  
  }else{next()}
})


new Vue({
  router,//注入路由
  store,
  render: (h) => h(App),
  created() {
    store.commit('addMenu', router)
    // store.commit('defaultTag',Cookies.get(radio))
  }
}).$mount("#app");
